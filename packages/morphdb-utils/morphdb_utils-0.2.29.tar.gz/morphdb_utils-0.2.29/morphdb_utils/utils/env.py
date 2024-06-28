import os


def read_configuration_from_env() -> dict[str, str]:
    config = {}
    if "MORPH_DATABASE_ID" in os.environ:
        config["database_id"] = os.environ["MORPH_DATABASE_ID"]
    if "MORPH_BASE_URL" in os.environ:
        config["base_url"] = os.environ["MORPH_BASE_URL"]
    if "MORPH_TEAM_SLUG" in os.environ:
        config["team_slug"] = os.environ["MORPH_TEAM_SLUG"]
    if "MORPH_API_KEY" in os.environ:
        config["api_key"] = os.environ["MORPH_API_KEY"]
    if "MORPH_CANVAS" in os.environ:
        config["canvas"] = os.environ["MORPH_CANVAS"]        

    return config