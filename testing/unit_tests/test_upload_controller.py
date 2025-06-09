# from src.controllers import upload_controller
# from testing.test_data.uploads import upload_preview_expected_res
# import pytest
# import json

## Refactor so these tests are testing the individual functions

# TEST_REGISTER_LOCATION = "./testing/test_documents/"
# PROCESS_REGISTER_FILE_TEST_DATA = [
#     (entry.get('filename'),
#      entry.get('centre_id'),
#      entry.get('candidates'),
#      entry.get('batches'),
#      entry.get('errors'))
#      for entry in upload_preview_expected_res
# ]
# PROCESS_REGISTER_TEST_IDS = [
#     entry.get('filename') for entry in upload_preview_expected_res
# ]

# @pytest.mark.parametrize("filename, centre_id, expected_candidates, expected_batches, expected_errors", PROCESS_REGISTER_FILE_TEST_DATA, ids=PROCESS_REGISTER_TEST_IDS)
# def test_register_reader(filename, centre_id, expected_candidates, expected_batches, expected_errors):
#     with open(f"{TEST_REGISTER_LOCATION}{filename}.xlsx", "rb") as f:
#         file = f.read()

#     output = upload_controller.preview(centre_id=centre_id, marking_window_id=1, file=file)
#     assert output['candidates'] == expected_candidates, "Candidate data did not match"
#     assert output['batches'] == expected_batches, "Batch data did not match expected"
#     assert output['errors'] == expected_errors, "Errors were not correct"