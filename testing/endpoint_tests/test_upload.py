import pytest
import os
from testing.test_data.uploads import upload_preview_expected_res, upload_refresh_inputs, upload_refresh_expected_responses, complete_upload_json, duplicate_response
from src.dao import UploadDAO
import json
import copy


TEST_REGISTER_LOCATION = "./testing/test_documents/"

class TestUploadPreview:
    # POST happy paths
    PREVIEW_TEST_DATA = [
        (f"{entry.get('filename')}.xlsx",
        entry.get('centre_id'),
        entry.get('candidates'),
        entry.get('batches'),
        entry.get('errors'))
        for entry in upload_preview_expected_res
        ]
    PREVIEW_TEST_IDS = [
        entry.get('filename') for entry in upload_preview_expected_res
        ]

    @pytest.mark.parametrize(
            "filename, centre_id, expected_candidates, expected_batches, expected_errors",
            PREVIEW_TEST_DATA,
            ids=PREVIEW_TEST_IDS)
    async def test_preview_POST_200(self, db_session, async_client, filename, centre_id, expected_candidates, expected_batches, expected_errors):
        """
        POST upload/preview 200:
        Tests happy endpoints, successful upload of Excel sheet. Includes both with no errors and with expected errors
        """
        ## ARRANGE
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
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
            "Expected candidates were not correctly returned"
        )

        assert content['data']['batches'] == expected_batches, (
            "Expected batches were not correctly returned"
        )

        assert content['data']['errors'] == expected_errors, (
            "Expected errors were not returned"
        )
    
    DUPLICATE_TEST_CASES = [
        (
            f"{entry.get('filename')}.xlsx",
            entry.get('centre_id'),
            entry.get('marking_window_id'),
            copy.deepcopy(complete_upload_json[i]),
            copy.deepcopy(entry)
        )
        for i, entry in enumerate(duplicate_response)
    ]
    DUPLICATE_TEST_IDS = [entry.get('TEST_ID') for entry in duplicate_response]
    @pytest.mark.parametrize("filename, centre_id, marking_window_id, data_to_preload, expected_data", DUPLICATE_TEST_CASES, ids=DUPLICATE_TEST_IDS)
    async def test_preview_duplicates_POST_200(self, db_session, async_client, filename, centre_id, marking_window_id, data_to_preload, expected_data):
        """
        POST upload/preview 200:
        Tests for duplicates
        """
        upload_dao = UploadDAO(session=db_session)

        # ARRANGE
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        formdata = {
            "token": "dummy-token",
            "data": json.dumps(
                {
                    "centre_id": centre_id,
                    "marking_window_id": marking_window_id
                    }
                )
            }
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        
        ## ACT
        upload_dao.insert_upload(data=data_to_preload)
        response = await async_client.post("/upload/preview", data=formdata, files=files)
        content = response.json()

        # ASSERT
        assert response.status_code == 200, (
            f"Expected 200, received {response.status_code} with error message '{content['message']}'"
        )

        assert content['data']['candidates'] == expected_data['candidates'], (
            "Expected candidates were not correctly returned"
        )

        assert content['data']['errors'] == expected_data['errors'], (
            "Expected errors were not returned"
        )
        
        assert content['data']['batches'] == expected_data['batches'], (
            "Expected batches were not correctly returned"
        )

    # POST unsupported media type e.g. .pdf, .doc
    @pytest.mark.parametrize(
            "filename, ext, mime_type",
            [
                ("test_register_1", "docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
                ("test_register_1", "pdf", "application/pdf")
            ],
            ids=[ "DOCX", "PDF" ]
            )
    async def test_preview_POST_415(self, db_session, async_client, filename, ext, mime_type):
        """
        POST upload/preview 415:
        tests upload of unsupported file types
        """

        ## ARRANGE
        filename = f"{filename}.{ext}"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        formdata = {
            "token": "dummy-token",
            "data": json.dumps(
                {
                    "centre_id": "3243",
                    "marking_window_id": 1
                    }
                )
            }
        files = {"file": (filename, open(filepath, "rb"), mime_type)}

        ## ACT
        response = await async_client.post("/upload/preview", data=formdata, files=files)
        content = response.json()

        ## ASSERT
        assert response.status_code == 415, (
            f"Expected status 415, recevied {response.status_code}"
        )

        expected_message = f"File type .{ext} not supported"
        assert content['message'] == expected_message, (
            f"Expected message '{expected_message}', received '{content['message']}'"
        )

    # POST missing or invalid data e.g. centre_id, marking_window
    @pytest.mark.parametrize(
        "filename, centre_id, marking_window_id",
        [
            ("test_register_1", None, 1),
            ("test_register_1", "3243", None),
            ("test_register_1", "Language Centre Name", 1),
            ("test_register_1", 3243, 1),
            ("test_register_1", None, None)
        ],
        ids=[
            "Missing centre_id",
            "Missing marking_window_id",
            "Centre_id string incorrect format",
            "Centre_id is an int",
            "Missing both centre_id and marking_window_id"
        ]
    )
    async def test_preview_POST_400_data(self, db_session, async_client, filename, centre_id, marking_window_id):
        """
        POST upload/preview 400
        Tests submissions of missing data
        """

        ## ARRANGE
        filename = f"{filename}.xlsx"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        formdata = {
            "token": "dummy-token",
            "data": json.dumps(
                {
                    k: v for k, v in {
                        "centre_id": centre_id,
                        "marking_window_id": marking_window_id
                    }.items() if v
                    }
                )
            }
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        ## ACT
        response = await async_client.post("/upload/preview", data=formdata, files=files)
        # content = response.json()
        # print(content['message'])

        ## ASSERT
        assert response.status_code == 400, (
            f"Expected 400 status code, received {response.status_code}"
        )

        # maybe add some more in for error messages once I know how to format them?

    # POST incorrectly formatted Excel sheet (wrong columns)
    @pytest.mark.parametrize(
            "filename",
            [
                ("test_register_incorrect_col_names"),
                ("test_register_extra_cols"),
                ("test_register_totally_wrong")
            ]
    )
    async def test_preview_POST_400_file(self, db_session, async_client, filename):
        """
        POST upload/preview 400:
        Tests upload of incorrectly formatted Excel sheets
        """

        ## ARRANGE
        filename = f"{filename}.xlsx"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        formdata = {
            "token": "dummy-token",
            "data": json.dumps(
                {
                    "centre_id": "3243",
                    "marking_window_id": 1
                    }
                )
            }
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        ## ACT
        response = await async_client.post("/upload/preview", data=formdata, files=files)
        content = response.json()

        ## ASSERT
        assert response.status_code == 400, (
            f"Expected 400 status code, received {response.status_code}"
        )

        assert content['message'] == "There was an error processing the file you uploaded. Please check that you have used the correct template and it has not been altered.", (
            f"Recieved error message: {content['message']}"
        )

        # Add more tests:
        # for candidates already on the database

class TestUploadRefresh:
    REFRESH_TEST_IDS = [
        entry.pop('TEST_ID') for entry in upload_refresh_inputs
    ]
    REFRESH_TEST_DATA = [
        (upload_refresh_inputs[i], upload_refresh_expected_responses[i]) for i in range(len(upload_refresh_inputs))
    ]

    @pytest.mark.parametrize("input, expected_output", REFRESH_TEST_DATA, ids=REFRESH_TEST_IDS)
    async def test_refresh_POST_200(self, async_client, input, expected_output):
        """
        POST upload/refresh 200:
        Tests happy endpoints, no errors found and expected errors found
        """
        ## ARRANGE
        payload = {
            "token": "dummy-token",
            "data": input
        }

        ## ACT
        response = await async_client.post("/upload/refresh", json=payload)
        content = response.json()

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

        assert content['data']['candidates'] == expected_output['candidates'], (
            "Expected candidates were not correctly returned"
        )

        assert content['data']['batches'] == expected_output['batches'], (
            "Expected batches were not correctly returned"
        )

        assert content['data']['errors'] == expected_output['errors'], (
            "Expected errors were not returned"
        )