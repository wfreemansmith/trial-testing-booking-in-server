import pytest
from src.services.file_handling import get_folder_name, get_file_name
from src.schemas.upload_schema import parse_batch_data, parse_candidate_data
from testing.test_data.uploads import upload_preview_expected_res

TEST_FOLDER_DATA = [
    ("1179", 1, r"/AOG/Operations/IELTS Admin/IELTS Trial Testing TESTING January-March 2025/BC/1179/"),
    ("5802", 2, r"/AOG/Operations/IELTS Admin/IELTS Trial Testing TESTING May-July 2025/IDP/5802/"),
    ("1176", 3, r"/AOG/Operations/IELTS Admin/IELTS Trial Testing TESTING September-November 2025/Neither/1176/")
]
@pytest.mark.parametrize("centre_id, marking_window_id, expected", TEST_FOLDER_DATA)
def test_get_folder_name(centre_id, marking_window_id, expected):
    result = get_folder_name(centre_id, marking_window_id)
    assert result == expected, (
        f"Expected '{expected}', received '{result}'"
    )

TEST_FILENAME_DATA = [
    (
        upload_preview_expected_res[1]['centre_id'],
        parse_batch_data(batch),
        [parse_candidate_data(candidate) for candidate in upload_preview_expected_res[1]['candidates']],
        {'R': 'reading','W': 'writing','L': 'listening'}[batch['component_id']],
        upload_preview_expected_res[1]['expected_filenames'][batch['version_id']]
    ) for batch in upload_preview_expected_res[1]['batches']
]
@pytest.mark.parametrize("centre_id, batch, candidates, component, expected", TEST_FILENAME_DATA)
def test_get_file_name(centre_id, batch, candidates, component, expected):
    result = get_file_name(centre_id, batch, candidates, component)
    assert result == expected, (
        f"Expected '{expected}', received '{result}'"
    )