from __future__ import annotations

import glob
import io
import json
import os
import urllib.parse
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
import urllib3
from requests.exceptions import Timeout
from urllib3.exceptions import InsecureRequestWarning

from morphdb_utils.type import (
    ListStorageDirectoryResponse,
    LoadDataParams,
    Protocol,
    RefResponse,
    SignedUrlResponse,
    SqlResultResponse,
)
from morphdb_utils.utils.sql import SQLUtils

urllib3.disable_warnings(InsecureRequestWarning)


class MorphApiError(Exception):
    pass


def _get_presigned_url_path(file_path, team_slug, database_id):
    return "morph-storage://vm/{}/{}/{}".format(
        team_slug, database_id, file_path if not file_path.startswith("/") else file_path[1:]
    )


def _handle_morph_response(response: requests.Response):
    if response.status_code != 200:
        raise MorphApiError(response.text)
    response_json = response.json()
    if (
        "error" in response_json
        and "subCode" in response_json
        and "message" in response_json
    ):
        error_message = response_json["message"]
        if response_json["error"] == "internal_server_error":
            error_message = (
                "System internal server error occurred. Please try again later."
            )
        if response_json["error"] == "notebook_error":
            if response_json["subCode"] == 2:
                error_message = "Reference cell not found. Please check the cell name and try again."
        if response_json["error"] == "storage_error":
            if response_json["subCode"] == 4:
                error_message = "Could not find data in the reference cell. Please check if the reference cell was executed successfully and retrieved the result correctly, and try again."
        if response_json["error"] == "template_error":
            if response_json["subCode"] == 3:
                error_message = "The auth connection info not found while connecting external source. Please check if the auth has not been deleted and try again."
            if response_json["subCode"] == 4 or response_json["subCode"] == 5:
                error_message = "The auth token connecting external source has been expired. Please authorize the connector and try again."
        if response_json["error"] == "external_connection_error":
            if response_json["subCode"] == 1:
                error_message = "The connector not found. Please check if the connector exists and try again."
        raise MorphApiError(error_message)
    return response_json


def _read_configuration_from_env() -> dict[str, str]:
    config = {}
    if "MORPH_DATABASE_ID" in os.environ:
        config["database_id"] = os.environ["MORPH_DATABASE_ID"]
    if "MORPH_BASE_URL" in os.environ:
        config["base_url"] = os.environ["MORPH_BASE_URL"]
    if "MORPH_TEAM_SLUG" in os.environ:
        config["team_slug"] = os.environ["MORPH_TEAM_SLUG"]
    if "MORPH_API_KEY" in os.environ:
        config["api_key"] = os.environ["MORPH_API_KEY"]

    return config


def _canonicalize_base_url(base_url: str) -> str:
    if base_url.startswith("http"):
        return base_url
    else:
        return f"https://{base_url}"


def _convert_sql_engine_response(
    response: SqlResultResponse,
) -> pd.DataFrame:
    fields = response.headers

    def parse_value(case_type, value):
        if case_type == "nullValue":
            return None
        elif case_type == "doubleValue":
            return value[case_type]
        elif case_type == "floatValue":
            return value[case_type]
        elif case_type == "int32Value":
            return value[case_type]
        elif case_type == "int64Value":
            return int(value[case_type])
        elif case_type == "uint32Value":
            return value[case_type]
        elif case_type == "uint64Value":
            return int(value[case_type])
        elif case_type == "sint32Value":
            return value[case_type]
        elif case_type == "sint64Value":
            return int(value[case_type])
        elif case_type == "fixed32Value":
            return value[case_type]
        elif case_type == "fixed64Value":
            return int(value[case_type])
        elif case_type == "sfixed32Value":
            return value[case_type]
        elif case_type == "sfixed64Value":
            return int(value[case_type])
        elif case_type == "boolValue":
            return value[case_type]
        elif case_type == "stringValue":
            return value[case_type]
        elif case_type == "bytesValue":
            return value[case_type]
        elif case_type == "structValue":
            return value[case_type]["fields"]
        elif case_type == "listValue":
            rows = []
            for v in value[case_type]["values"]:
                rows.append(parse_value(v["kind"]["$case"], v["kind"]))
            return rows

    parsed_rows = []
    for row in response.rows:
        parsed_row = {}
        for field in fields:
            value = row["value"][field]["kind"]
            case_type = value["$case"]
            parsed_row[field] = parse_value(case_type, value)
        parsed_rows.append(parsed_row)
    return pd.DataFrame.from_dict(parsed_rows)


def _convert_signed_url_response_to_dateframe(
    response: SignedUrlResponse,
) -> pd.DataFrame:
    ext = response.url.split("?")[0].split("/")[-1].split(".")[-1]
    r = requests.get(response.url)

    if ext == "csv":
        chunks = []
        for chunk in pd.read_csv(
            io.BytesIO(r.content),
            header=0,
            chunksize=1_000_000,
            encoding_errors="replace",
        ):
            chunks.append(chunk)
        df = pd.concat(chunks, axis=0)
    else:
        if ext.endswith(".xls"):
            df = pd.read_excel(
                io.BytesIO(r.content), engine="xlrd", header=0, sheet_name=0
            )
        else:
            df = pd.read_excel(
                io.BytesIO(r.content), engine="openpyxl", header=0, sheet_name=0
            )
    return df


def _load_file_data_impl(
    filename: str | None = None,
    timestamp: int | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None,
) -> pd.DataFrame:
    config_from_env = _read_configuration_from_env()
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if api_key is None:
        api_key = config_from_env["api_key"]

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    split_url = urllib.parse.urlsplit(base_url)
    request_url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"{split_url.path}/resource/morph-storage/download-url",
    )

    query_params = {}
    if filename is not None:
        query_params["filename"] = filename
    if timestamp is not None:
        query_params["timestamp"] = timestamp
    request_url += f"?{urllib.parse.urlencode(query_params)}"

    try:
        response = requests.get(request_url, headers=headers)
    except Timeout:
        raise MorphApiError("Process Timeout while executing load_data")
    except Exception as e:
        raise MorphApiError(f"{e}")

    response_body = _handle_morph_response(response)

    try:
        structured_response_body = SignedUrlResponse(
            url=response_body["preSignedDownloadUrl"]
        )
        df = _convert_signed_url_response_to_dateframe(structured_response_body)
        return df
    except Exception as e:
        raise MorphApiError(f"load_data error: {e}")


def _execute_sql_impl(
    sql: str,
    connection_slug: str | None = None,
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None,
) -> pd.DataFrame:
    config_from_env = _read_configuration_from_env()
    if database_id is None:
        database_id = config_from_env["database_id"]
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if api_key is None:
        api_key = config_from_env["api_key"]

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    split_url = urllib.parse.urlsplit(base_url)
    url_sql = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"{split_url.path}/{database_id}/sql/python",
    )

    request = {"sql": sql}
    if connection_slug is not None:
        request["connectionSlug"] = connection_slug

    try:
        response = requests.post(url_sql, headers=headers, json=request, verify=True)
    except Timeout:
        raise MorphApiError("Process Timeout while executing SQL")
    except Exception as e:
        raise MorphApiError(f"SQL error: {e}")

    response_body = _handle_morph_response(response)
    try:
        structured_response_body = SqlResultResponse(
            headers=response_body["headers"], rows=response_body["rows"]
        )
        df = _convert_sql_engine_response(structured_response_body)
        return df
    except Exception as e:
        raise MorphApiError(f"{e}")


def _find_canvas_json(start_dir: str) -> Optional[Tuple[str, Dict]]:
    current_dir = start_dir

    while True:
        canvas_json_path = os.path.join(current_dir, "canvas.json")
        if os.path.isfile(canvas_json_path):
            with open(canvas_json_path, "r") as f:
                canvas_data = json.load(f)
            return canvas_json_path, canvas_data

        # ルートディレクトリに到達したらループを終了
        parent_dir = os.path.dirname(current_dir)
        if current_dir == parent_dir:
            break

        current_dir = parent_dir

    return None


def ref(reference: str) -> RefResponse:
    # canvas.jsonを検索・パースする
    current_dir = os.getcwd()
    canvas_json = _find_canvas_json(current_dir)
    if canvas_json is None:
        raise MorphApiError("canvas.json not found")
    canvas_json_path, canvas_json_data = canvas_json

    # 当該リファレンスファイルの情報を取得
    canvas_cell_conf = next(
        (
            cell
            for cell in canvas_json_data["cells"]
            if cell["filename"] == os.path.basename(reference)
        ),
        None,
    )
    if canvas_cell_conf is None:
        raise MorphApiError(f"Cell with filename {reference} not found")

    # 当該リファレンスファイルの内容を取得
    ref_code = None
    if not canvas_cell_conf["filename"].startswith(Protocol.S3.value):
        ref_file_path = os.path.join(
            os.path.dirname(canvas_json_path), canvas_cell_conf["filename"]
        )
        with open(ref_file_path, "r") as f:
            ref_code = f.read()

    return RefResponse(
        canvas_json_path=canvas_json_path,
        cell_type=canvas_cell_conf["cellType"],
        filename=canvas_cell_conf["filename"],
        settings=canvas_cell_conf["settings"],
        description=canvas_cell_conf["description"],
        code=ref_code,
        parent_cells=canvas_cell_conf["parentCells"],
        connection_type=canvas_cell_conf["connectionType"],
        connection_slug=canvas_cell_conf["connectionSlug"],
        storage_path=canvas_cell_conf["storagePath"]
        if "storagePath" in canvas_cell_conf
        else None,
    )


def execute_sql(*args, **kwargs) -> pd.DataFrame:
    if args and isinstance(args[0], RefResponse):
        if args[0].cell_type != "sql":
            raise MorphApiError(f"Cell {args[0].filename} is not a SQL cell")
        ref_dict = {
            "sql": args[0].code,
            "connection_slug": args[0].connection_slug,
        }
        return _execute_sql_impl(**ref_dict, **kwargs)
    else:
        return _execute_sql_impl(*args, **kwargs)


def _process_records(action: str, *args, **kwargs) -> None:
    if not args or (
        not isinstance(args[0], RefResponse) and not isinstance(args[0], pd.DataFrame)
    ):
        raise MorphApiError(
            "Invalid *args provided: RefResponse or pd.DataFrame is required."
        )
    if not kwargs.get("table_name"):
        raise MorphApiError("Invalid **kwargs provided: table_name is required.")

    table_name = kwargs.pop("table_name")
    ref_dict = {}

    if isinstance(args[0], RefResponse):
        if args[0].cell_type != "sql":
            raise MorphApiError(f"Cell {args[0].filename} is not a SQL cell")
        ref_dict = {
            "sql": args[0].code,
            "connection_slug": args[0].connection_slug,
        }
        data = _execute_sql_impl(**ref_dict)
    else:
        data = args[0]

    if not isinstance(data, pd.DataFrame):
        raise MorphApiError("Invalid data type provided. pd.DataFrame is required.")

    sql_utils = SQLUtils(data, table_name, kwargs.get("column_types"))

    if action == "create":
        sqls = sql_utils.generate_replace_sql()
        ref_dict["sql"] = sqls["drop_table_sql"]
        _execute_sql_impl(**ref_dict)
        ref_dict["sql"] = sqls["create_table_sql"]
        _execute_sql_impl(**ref_dict)
        if not data.empty:
            ref_dict["sql"] = sqls["insert_sql"]
            _execute_sql_impl(**ref_dict)
    elif action == "insert":
        ref_dict["sql"] = sql_utils.generate_insert_sql()
        _execute_sql_impl(**ref_dict)
    elif action == "update":
        if not kwargs.get("key_columns"):
            raise MorphApiError(
                "Invalid **kwargs provided: key_columns is required for update."
            )
        ref_dict["sql"] = sql_utils.generate_update_sql(kwargs["key_columns"])
        _execute_sql_impl(**ref_dict)
    else:
        raise MorphApiError("Invalid action provided.")


def create_table(*args, **kwargs) -> None:
    _process_records("create", *args, **kwargs)


def insert_records(*args, **kwargs) -> None:
    _process_records("insert", *args, **kwargs)


def update_records(*args, **kwargs) -> None:
    _process_records("update", *args, **kwargs)


def load_file_data(*args, **kwargs) -> pd.DataFrame:
    if args and isinstance(args[0], RefResponse):
        if args[0].cell_type != "file" or args[0].storage_path is None:
            raise MorphApiError(f"Cell {args[0].cell_name} is not a Sheet cell")
        ref_dict = {
            "filename": args[0].storage_path,
        }
        return _load_file_data_impl(**ref_dict, **kwargs)
    else:
        return _load_file_data_impl(*args, **kwargs)


def load_data(*args: LoadDataParams, **kwargs) -> pd.DataFrame:
    if args and isinstance(args[0], RefResponse):
        if args[0].cell_type == "sql":
            ref_dict = {
                "sql": args[0].code,
                "connection_slug": args[0].connection_slug,
            }
            return _execute_sql_impl(**ref_dict, **kwargs)
        elif args[0].cell_type == "file":
            ref_dict = {
                "filename": args[0].storage_path,
            }
            return _load_file_data_impl(**ref_dict, **kwargs)
        elif args[0].cell_type == "python":
            config_from_env = _read_configuration_from_env()
            ref_file_dir = os.path.join(
                os.path.dirname(args[0].canvas_json_path),
                os.path.join("data", "output_" + os.path.splitext(args[0].filename)[0] + "_" + os.path.splitext(args[0].filename)[1].replace(".", "")),
            )
            file_list = os.listdir(ref_file_dir)
            if len(file_list) < 1:
                raise MorphApiError(f"Cell {args[0].cell_name} has no output file")
            storage_path = _get_presigned_url_path(
                os.path.join(ref_file_dir, file_list[0]), config_from_env["team_slug"]
            )
            ref_dict = {
                "filename": storage_path,
            }
            return _load_file_data_impl(**ref_dict, **kwargs)
        else:
            raise MorphApiError(f"Cell {args[0].cell_name} is not a valid cell type")
    elif "type" in args[0]:
        if args[0]["type"] == "sql":
            omitted_args = {k: v for k, v in args[0].items() if k != "type"}
            return _execute_sql_impl(**omitted_args, **kwargs)
        elif args[0]["type"] == "sheet" or args[0]["type"] == "python":
            omitted_args = {k: v for k, v in args[0].items() if k != "type"}
            return _load_file_data_impl(**omitted_args, **kwargs)
        else:
            raise ValueError("Invalid data cell type provided.")
    else:
        raise ValueError("Invalid data cell type provided.")
    

def read_dir(
    dir_path = '/',
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None,  
) -> List[str]:
    current_dir = os.path.dirname(os.path.abspath('__file__'))
    abs_path = os.path.abspath(os.path.join(current_dir, "data", dir_path))
    dirs = os.listdir(abs_path)
    storage_dirs = __list_storage_dirs(abs_path, 1, database_id, base_url, team_slug, api_key)
    if storage_dirs is not None:
        for storage_dir in storage_dirs.directories:
            dirs.append(storage_dir.name)
        for storage_file in storage_dirs.files:
            dirs.append(storage_file.name)
    return list(set(dirs))


def get_file(
    filename: str,
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None,        
) -> str:
    config_from_env = _read_configuration_from_env()
    if database_id is None:
        database_id = config_from_env["database_id"]
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if api_key is None:
        api_key = config_from_env["api_key"]

    current_dir = os.path.dirname(os.path.abspath('__file__'))
    abs_path = os.path.abspath(os.path.join(current_dir, filename)) if not filename.startswith(current_dir) else filename
    if os.path.exists(abs_path):
        return abs_path
    return _get_presigned_url_path(abs_path, team_slug, database_id)


def get_data_path(
    filename: str,
    specific_filename: str | None = None,
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None,
) -> str:
    """
    @param filename: The name of the file or directory to be loaded (cell name).
    @param specific_filename: The specific name under the directory.
    """
    config_from_env = _read_configuration_from_env()
    if database_id is None:
        database_id = config_from_env["database_id"]
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if api_key is None:
        api_key = config_from_env["api_key"]

    current_dir = os.path.dirname(os.path.abspath('__file__'))
    _, ext = os.path.splitext(filename)
    if ext == "":
        dir_path = os.path.join(current_dir, "data", filename)
        if specific_filename is not None:
            specific_filepath = os.path.join(dir_path, specific_filename)
            if os.path.exists(specific_filepath):
                return specific_filepath
            return _get_presigned_url_path(specific_filepath, team_slug, database_id)
        latest_file = __get_latest_file(dir_path)
        if latest_file is not None:
            return latest_file
        storage_data = __list_storage_dirs(dir_path)
        if storage_data is not None and len(storage_data.files) > 0:
            return _get_presigned_url_path(storage_data.files[0].path, team_slug, database_id)
        return None
    else:
        base_file_path = os.path.basename(filename)        
        dir_path = os.path.join(current_dir, "data", "output_" + os.path.splitext(base_file_path)[0] + "_" + os.path.splitext(base_file_path)[1].replace(".", ""))
        if specific_filename is not None:
            specific_filepath = os.path.join(dir_path, specific_filename)
            if os.path.exists(specific_filepath):
                return specific_filepath
            return _get_presigned_url_path(specific_filepath, team_slug, database_id)
        latest_file = __get_latest_file(dir_path)
        if latest_file is not None:
            return latest_file
        storage_data = __list_storage_dirs(dir_path)
        if storage_data is not None and len(storage_data.files) > 0:
            return _get_presigned_url_path(storage_data.files[0].path, team_slug, database_id)
        return None


def __get_latest_file(dir_path):
    files = glob.glob(os.path.join(dir_path, '*'))
    
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)
    
    return latest_file


def __list_storage_dirs(
    prefix: str,
    depth: int = 2,
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None
):
    config_from_env = _read_configuration_from_env()
    if database_id is None:
        database_id = config_from_env["database_id"]
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if api_key is None:
        api_key = config_from_env["api_key"]    

    headers = {
        "X-Api-Key": api_key,
    }

    split_url = urllib.parse.urlsplit(base_url)
    request_url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"{split_url.path}/resource/morph-storage/directory",
    )

    query_params = {
        "databaseId": database_id,
        "depth": depth,
        "path": prefix,
    }    
    request_url += f"?{urllib.parse.urlencode(query_params)}"

    try:
        response = requests.get(request_url, headers=headers)
    except Timeout:
        raise MorphApiError("Process Timeout while executing load_data")
    except Exception as e:
        raise MorphApiError(f"{e}")

    response_body = _handle_morph_response(response)

    try:
        return ListStorageDirectoryResponse(
            **response_body
        )
    except Exception as e:
        raise MorphApiError(f"load_data error: {e}")    


def generate_report(
    refs: list[RefResponse],
    prompt: Optional[str] = None,
    language: Optional[str] = None,
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    api_key: str | None = None,
) -> str:
    config_from_env = _read_configuration_from_env()
    if database_id is None:
        database_id = config_from_env["database_id"]
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if api_key is None:
        api_key = config_from_env["api_key"]
    if not "dashboard-api" in base_url:
        base_url = base_url.replace("api", "dashboard-api")

    for ref in refs:
        if ref.cell_type != "python":
            raise MorphApiError(f"Cell {ref.cell_name} is not a Python cell")
        elif "@report" in ref.code:
            raise MorphApiError(
                f"Cell {ref.cell_name}(report cell) is not allowed to be used in report generation."
            )

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        "/agent/chat/report",
    )

    request = {
        "databaseId": database_id,
        "canvasName": refs[0].canvas_json_path,
        "fileNames": [ref.filename for ref in refs],
        "prompt": prompt,
        "language": language,
    }
    try:
        response = requests.post(url, headers=headers, json=request, verify=True)
    except Timeout:
        raise MorphApiError("Process Timeout while executing generate_report")
    except Exception as e:
        raise MorphApiError(f"generate_report error: {e}")

    response_body = _handle_morph_response(response)
    return response_body["report"]


def send_email(
    refs: list[RefResponse],
    emails: list[str],
    subject: str,
    body: str,
    database_id: str | None = None,
    base_url: str | None = None,
    team_slug: str | None = None,
    authorization: str | None = None,
    notebook_id: str | None = None,
):
    config_from_env = _read_configuration_from_env()
    if database_id is None:
        database_id = config_from_env["database_id"]
    if base_url is None:
        base_url = config_from_env["base_url"]
    if team_slug is None:
        team_slug = config_from_env["team_slug"]
    if authorization is None:
        authorization = config_from_env["authorization"]
    if notebook_id is None:
        notebook_id = config_from_env["notebook_id"]

    for ref in refs:
        if ref.cell_type != "python":
            raise MorphApiError(f"Cell {ref.cell_name} is not a Python cell")

    headers = {
        "teamSlug": team_slug,
        "Authorization": authorization,
    }

    url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"/{database_id}/python/email",
    )

    request = {
        "notebookId": notebook_id,
        "attachmentCellIds": [ref.cell_id for ref in refs],
        "emails": emails,
        "subject": subject,
        "body": body,
    }

    try:
        requests.post(url, headers=headers, json=request, verify=True)
    except Timeout:
        raise MorphApiError("Process Timeout while executing generate_report")
    except Exception as e:
        raise MorphApiError(f"generate_report error: {e}")
