from src.services.excel_register_processing import process_register_file
from db.test_data.uploads import expected_xlsx_res_1
import pytest
import json

TEST_REGISTER_LOCATION = "./assets/test_registers/"
PROCESS_REGISTER_FILE_TEST_DATA = [
    (entry.get('filename'),
     entry.get('centre_num'),
     entry.get('candidates'),
     entry.get('batches'))
     for entry in expected_xlsx_res_1
]

@pytest.mark.parametrize("filename, centre_num, expected_candidates, expected_batches", PROCESS_REGISTER_FILE_TEST_DATA)
def test_register_reader(filename, centre_num, expected_candidates, expected_batches):
    with open(f"{TEST_REGISTER_LOCATION}{filename}.xlsx", "rb") as f:
        file = f.read()

    candidate_output, batches_output = process_register_file(centre_num=centre_num, marking_window_id=1, file=file)
    assert candidate_output == expected_candidates, "Candidate data did not match"
    assert batches_output == expected_batches, "Batch data did not match expected"