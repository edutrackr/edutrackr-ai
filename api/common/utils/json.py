import json


def try_serialize_to_json(obj) -> str | None:
    try:
        return json.dumps(obj)
    except TypeError:
        return

def try_deserialize_from_json(json_str: str) -> dict | None:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return
