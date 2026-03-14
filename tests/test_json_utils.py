from limen.utils.json_utils import extract_json_object


def test_extract_json_object_from_clean_payload():
    payload = '{"severity_score": 7, "revision_useful": true}'
    parsed = extract_json_object(payload)
    assert parsed["severity_score"] == 7
    assert parsed["revision_useful"] is True
