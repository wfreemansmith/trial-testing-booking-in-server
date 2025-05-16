import pytest
import os
from db.test_data.uploads import expected_xlsx_res_1
import json


## Test data setup

TEST_REGISTER_LOCATION = "./assets/test_registers/"
PREVIEW_TEST_DATA = [
    (entry.get('filename'),
     entry.get('centre_id'),
     entry.get('candidates'),
     entry.get('batches'),
     entry.get('errors'))
     for entry in expected_xlsx_res_1
    ]
PREVIEW_TEST_IDS = [
    entry.get('filename') for entry in expected_xlsx_res_1
]

class TestPreviewUpload:
    @pytest.mark.parametrize(
            "filename, centre_id, expected_candidates, expected_batches, expected_errors",
            PREVIEW_TEST_DATA,
            ids=PREVIEW_TEST_IDS)
    async def test_preview_happy_path(self, async_client, filename, centre_id, expected_candidates, expected_batches, expected_errors):

        ## ARRANGE
        filepath = f"{os.path.join(TEST_REGISTER_LOCATION, filename)}.xlsx"
        formdata = {
            "token": "dummy-token",
            "data": json.dumps(
                {
                    "centre_id": centre_id,
                    "marking_window_id": 1
                    }
                )
            }
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        ## ACT
        # call the endpoint with form data and file
        response = await async_client.post("/upload/preview", data=formdata, files=files)
        # parse JSON into a dict
        content = response.json()
        
        ## ASSERT
        assert response.status_code == 200, (
            f"Expected 200, received {response.status_code} with error message '{content['message']}'"
        )

        assert content['data']['candidates'] == expected_candidates, (
            "Expected candidates were not correctly resturned"
        )

        assert content['data']['batches'] == expected_batches, (
            "Expected batches were not correctly resturned"
        )

        assert content['data']['errors'] == expected_errors, (
            "Expected errors were not returned"
        )