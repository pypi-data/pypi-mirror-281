import io
import os

import pandas as pd
import requests

from morphdb_utils.api import MorphApiError
from morphdb_utils.type import SignedUrlResponse, SqlResultResponse


def handle_morph_response(response: requests.Response):
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


def convert_sql_engine_response(
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


def convert_signed_url_response_to_dateframe(
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


def convert_filepath_to_df(abs_path: str):
    ext = os.path.splitext(os.path.basename(abs_path))[1][1:]

    content = ""
    with open(abs_path, "r") as f:
        content = f.read()

    if ext == "csv":
        chunks = []
        for chunk in pd.read_csv(
            io.StringIO(content),
            header=0,
            chunksize=1_000_000,
            encoding_errors="replace",
        ):
            chunks.append(chunk)
        return pd.concat(chunks, axis=0)
    elif ext.endswith(".xls"):
        return pd.read_excel(
            io.StringIO(content), engine="xlrd", header=0, sheet_name=0
        )
    elif ext.endswith(".xlsx"):
        return pd.read_excel(
            io.StringIO(content), engine="openpyxl", header=0, sheet_name=0
        )
    raise Exception("Unsupported file format")
