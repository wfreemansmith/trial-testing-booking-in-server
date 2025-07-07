import pytest
import os
from testing.test_data.uploads import upload_preview_expected_res, upload_refresh_inputs, upload_refresh_expected_responses, complete_upload_json, duplicate_response, upload_fileupload_data
from src.dao import UploadDAO, StagedFileDAO
from src.models import StagedFile
from src.config import STAGING_DIR
from src.utils import construct_upload_path, construct_upload_filename
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
    async def test_preview_POST_200(self, async_client, filename, centre_id, expected_candidates, expected_batches, expected_errors):
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
    async def test_preview_POST_415(self, async_client, filename, ext, mime_type):
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
    async def test_preview_POST_400_data(self, async_client, filename, centre_id, marking_window_id):
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

        ## ASSERT
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

    FILE_UPLOAD_TEST_DATA = [
        (
            entry.get("filename"),
            entry.get("centre_id"),
            entry.get("marking_window_id"),
            entry.get("batch"),
            entry.get("candidates"),
            entry.get("expected_destination_folder"),
            entry.get("expected_destination_filename")
        ) for entry in upload_fileupload_data
    ]
    FILE_UPLOAD_TEST_IDS = [ entry.get("filename") for entry in upload_fileupload_data]
    @pytest.mark.parametrize("filename, centre_id, marking_window_id, batch, candidates, expected_destination_folder, expected_destination_filename", FILE_UPLOAD_TEST_DATA, ids=FILE_UPLOAD_TEST_IDS)
    async def test_file_upload_POST_200(self, db_session, async_client, filename, centre_id, marking_window_id, batch, candidates, expected_destination_folder, expected_destination_filename):
        """
        POST upload/file_upload 200:
        Tests a single file upload to the staging area and to the database
        """

        ## ARRANGE
        filename = filename = f"{filename}.pdf"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        formdata = {
            "token": "dummy-token",
            "data": json.dumps(
                {
                    "centre_id": centre_id,
                    "marking_window_id": marking_window_id,
                    "batch": batch,
                    "candidates": candidates
                }
            )
        }
        files = {"file": (filename, open(filepath, "rb"), "application/pdf")}

        ## ACT
        response = await async_client.post("/upload/file_upload", data=formdata, files=files)
        content = response.json()
        dao = StagedFileDAO(session=db_session)
        staged_db_entry = dao.select_one(centre_id=centre_id)

        ## ASSERT
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code} with error message: {content['message']}"
        )

        assert content['data']['filename'] == expected_destination_filename, (
            f"Did not received the expected response from the API, expected {expected_destination_filename} and received {content['data']['filename']}"
        )

        # check staging entry has been created on db
        assert isinstance(staged_db_entry, StagedFile), (
            f"Staged file type is not 'StagedFile' class, is instead {type(staged_db_entry)}"
        )

        assert staged_db_entry.centre_id == centre_id, (
            f"Staged file property incorrect, expected {centre_id} received {staged_db_entry.centre_id}"
        )

        assert staged_db_entry.marking_window_id == marking_window_id, (
            f"Staged file property incorrect, expected {marking_window_id} received {staged_db_entry.marking_window_id}"
        )

        assert staged_db_entry.marking_window_id == marking_window_id, (
            f"Staged file property incorrect, expected {marking_window_id} received {staged_db_entry.marking_window_id}"
        )

        assert staged_db_entry.version_id == batch.get("version_id"), (
            f"Staged file property incorrect, expected {batch.get("version_id")} received {staged_db_entry.version_id}"
        )

        assert staged_db_entry.destination_folder == expected_destination_folder, (
            f"Staged file property incorrect, expected {expected_destination_folder} received {staged_db_entry.destination_folder}"
        )

        assert staged_db_entry.destination_filename == expected_destination_filename, (
            f"Staged file property incorrect, expected {expected_destination_filename} received {staged_db_entry.destination_filename}"
        )

        # check file has been created locally
        assert os.path.exists(staged_db_entry.temp_path), (
            f"Looked for temp file at path {staged_db_entry.temp_path} and could not find it"
        )