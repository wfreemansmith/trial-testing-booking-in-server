import pytest
import os
from testing.test_data.uploads import upload_preview_expected_res, upload_refresh_inputs, upload_refresh_expected_responses, complete_upload_json, duplicate_response, upload_fileupload_data
from src.dao import UploadDAO, StagedFileDAO
from src.models import StagedFile
from src.config import STAGING_DIR
from src.utils import construct_upload_path, construct_upload_filename
import json
from unittest.mock import patch
import copy
from unittest.mock import patch


TEST_REGISTER_LOCATION = "./testing/test_documents/"

# Keys that exist in test data for routing purposes but are not valid Upload model fields
DAO_STRIP_KEYS = ('token', 'filename')


def for_dao(data: dict) -> dict:
    """Strip route-layer keys before passing to DAO/model."""
    return {k: v for k, v in data.items() if k not in DAO_STRIP_KEYS}


class TestUploadPreview:
    PREVIEW_TEST_DATA = [
        (f"{entry.get('filename')}.xlsx",
        entry.get('token'),
        entry.get('candidates'),
        entry.get('batches'),
        entry.get('errors'))
        for entry in upload_preview_expected_res
        ]
    PREVIEW_TEST_IDS = [entry.get('filename') for entry in upload_preview_expected_res]

    @pytest.mark.parametrize(
            "filename, token, expected_candidates, expected_batches, expected_errors",
            PREVIEW_TEST_DATA, ids=PREVIEW_TEST_IDS)
    async def test_preview_POST_200(self, db_session, async_client, filename, token, expected_candidates, expected_batches, expected_errors):
        """POST upload/preview 200: successful upload of Excel sheet"""
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        response = await async_client.post(f"/upload/preview?q={token}", files=files)
        content = response.json()
        
        assert response.status_code == 200, (
            f"Expected 200, received {response.status_code} with error message '{content['message']}'"
        )
        assert content['data']['candidates'] == expected_candidates, "Expected candidates were not correctly returned"
        assert content['data']['batches'] == expected_batches, "Expected batches were not correctly returned"
        assert content['data']['errors'] == expected_errors, "Expected errors were not returned"
    
    DUPLICATE_TEST_CASES = [
        (
            f"{entry.get('filename')}.xlsx",
            entry.get('token'),
            entry.get('centre_id'),
            entry.get('marking_window_id'),
            copy.deepcopy(complete_upload_json[i]),
            copy.deepcopy(entry)
        )
        for i, entry in enumerate(duplicate_response)
    ]
    DUPLICATE_TEST_IDS = [entry.get('TEST_ID') for entry in duplicate_response]

    @pytest.mark.parametrize("filename, token, centre_id, marking_window_id, data_to_preload, expected_data", DUPLICATE_TEST_CASES, ids=DUPLICATE_TEST_IDS)
    async def test_preview_duplicates_POST_200(self, db_session, async_client, filename, token, centre_id, marking_window_id, data_to_preload, expected_data):
        """POST upload/preview 200: duplicate candidate detection"""
        upload_dao = UploadDAO(session=db_session)
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        
        upload_dao.insert_upload(data=for_dao(data_to_preload), marking_window_id=marking_window_id, centre_id=centre_id)
        response = await async_client.post(f"/upload/preview?q={token}", files=files)
        content = response.json()

        assert response.status_code == 200, (
            f"Expected 200, received {response.status_code} with error message '{content['message']}'"
        )
        assert content['data']['candidates'] == expected_data['candidates'], "Expected candidates were not correctly returned"
        assert content['data']['errors'] == expected_data['errors'], "Expected errors were not returned"
        assert content['data']['batches'] == expected_data['batches'], "Expected batches were not correctly returned"

    @pytest.mark.parametrize(
            "filename, ext, mime_type",
            [
                ("test_register_1", "docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
                ("test_register_1", "pdf", "application/pdf")
            ],
            ids=["DOCX", "PDF"])
    async def test_preview_POST_415(self, db_session, async_client, filename, ext, mime_type):
        """POST upload/preview 415: unsupported file types"""
        filename = f"{filename}.{ext}"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        files = {"file": (filename, open(filepath, "rb"), mime_type)}

        response = await async_client.post("/upload/preview?q=hannah-centre", files=files)
        content = response.json()

        assert response.status_code == 415, f"Expected status 415, recevied {response.status_code}"
        expected_message = f"File type .{ext} not supported"
        assert content['message'] == expected_message, (
            f"Expected message '{expected_message}', received '{content['message']}'"
        )

    @pytest.mark.parametrize(
        "token, expected_status",
        [
            ("totally-invalid-token", 401),
            ("", 422),
        ],
        ids=["Invalid token returns 401", "Missing token returns 422"])
    async def test_preview_POST_401(self, db_session, async_client, token, expected_status):
        """POST upload/preview 401/422: invalid or missing token rejected before route logic"""
        filename = "test_register_1.xlsx"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        url = f"/upload/preview?q={token}" if token else "/upload/preview"
        response = await async_client.post(url, files=files)

        assert response.status_code == expected_status, (
            f"Expected {expected_status}, received {response.status_code}"
        )

    @pytest.mark.parametrize(
            "filename",
            [
                ("test_register_incorrect_col_names"),
                ("test_register_extra_cols"),
                ("test_register_totally_wrong")
            ])
    async def test_preview_POST_400_file(self, db_session, async_client, filename):
        """POST upload/preview 400: incorrectly formatted Excel sheets"""
        filename = f"{filename}.xlsx"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        files = {"file": (filename, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        response = await async_client.post("/upload/preview?q=hannah-centre", files=files)
        content = response.json()

        assert response.status_code == 400, f"Expected 400 status code, received {response.status_code}"
        assert content['message'] == "There was an error processing the file you uploaded. Please check that you have used the correct template and it has not been altered.", (
            f"Recieved error message: {content['message']}"
        )


class TestUploadRefresh:
    REFRESH_TEST_IDS = [entry.pop('TEST_ID') for entry in upload_refresh_inputs]
    REFRESH_TEST_DATA = [
        (upload_refresh_inputs[i].get('token'), upload_refresh_inputs[i], upload_refresh_expected_responses[i])
        for i in range(len(upload_refresh_inputs))
    ]

    @pytest.mark.parametrize("token, input, expected_output", REFRESH_TEST_DATA, ids=REFRESH_TEST_IDS)
    async def test_refresh_POST_200(self, db_session, async_client, token, input, expected_output):
        """POST upload/refresh 200: validation checks on user-submitted data"""
        data = for_dao(input)
        payload = {"data": data}

        response = await async_client.post(f"/upload/refresh?q={token}", json=payload)
        content = response.json()

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert content['data']['candidates'] == expected_output['candidates'], "Expected candidates were not correctly returned"
        assert content['data']['batches'] == expected_output['batches'], "Expected batches were not correctly returned"
        assert content['data']['errors'] == expected_output['errors'], "Expected errors were not returned"

    FILE_UPLOAD_TEST_DATA = [
        (
            entry.get("filename"),
            entry.get("token"),
            entry.get("batch"),
            entry.get("candidates"),
            entry.get("expected_destination_folder"),
            entry.get("expected_destination_filename"),
            entry.get("centre_id"),
            entry.get("marking_window_id"),
        ) for entry in upload_fileupload_data
    ]
    FILE_UPLOAD_TEST_IDS = [entry.get("filename") for entry in upload_fileupload_data]

    @pytest.mark.parametrize("filename, token, batch, candidates, expected_destination_folder, expected_destination_filename, centre_id, marking_window_id", FILE_UPLOAD_TEST_DATA, ids=FILE_UPLOAD_TEST_IDS)
    async def test_file_upload_POST_200(self, db_session, async_client, cleanup_tmp_files, filename, token, batch, candidates, expected_destination_folder, expected_destination_filename, centre_id, marking_window_id):
        """POST upload/file_upload 200: PDF staged locally and recorded in DB"""
        filename = f"{filename}.pdf"
        filepath = os.path.join(TEST_REGISTER_LOCATION, filename)
        formdata = {"data": json.dumps({"batch": batch, "candidates": candidates})}
        files = {"file": (filename, open(filepath, "rb"), "application/pdf")}

        response = await async_client.post(f"/upload/file_upload?q={token}", data=formdata, files=files)
        content = response.json()
        dao = StagedFileDAO(session=db_session)
        staged_db_entry = dao.select_one(centre_id=centre_id)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code} with error message: {content['message']}"
        )
        assert content['data']['filename'] == expected_destination_filename, (
            f"Expected {expected_destination_filename}, received {content['data']['filename']}"
        )
        assert isinstance(staged_db_entry, StagedFile), (
            f"Staged file type is not 'StagedFile' class, is instead {type(staged_db_entry)}"
        )
        assert staged_db_entry.centre_id == centre_id
        assert staged_db_entry.marking_window_id == marking_window_id
        assert staged_db_entry.version_id == batch.get("version_id")
        assert staged_db_entry.destination_folder == expected_destination_folder
        assert staged_db_entry.destination_filename == expected_destination_filename
        assert os.path.exists(staged_db_entry.temp_path), (
            f"Looked for temp file at path {staged_db_entry.temp_path} and could not find it"
        )

    SUBMIT_TEST_DATA = [
        (
            entry.get('token'),
            f"{entry.get('filename')}.xlsx",
            f"{upload_fileupload_data[0].get('filename')}.pdf"
        ) for entry in upload_preview_expected_res if not entry.get('errors')
    ]

    @pytest.mark.parametrize("token, candidate_register, pdf_filename", SUBMIT_TEST_DATA)
    async def test_submit_POST_200(self, db_session, async_client, cleanup_tmp_files, token, candidate_register, pdf_filename):
        """POST upload/submit 200: end-to-end from preview through file upload to final submit"""
        # Step 1: Preview
        filepath = os.path.join(TEST_REGISTER_LOCATION, candidate_register)
        files = {"file": (candidate_register, open(filepath, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = await async_client.post(f"/upload/preview?q={token}", files=files)
        content = response.json()
        assert response.status_code == 200, (
            f"Expected 200, received {response.status_code} with message '{content['message']}'"
        )

        candidates = content['data'].get('candidates')
        batches = content['data'].get('batches')

        # Step 2: Submit without files — expect 422
        payload = {"data": {"batches": batches, "candidates": candidates}}
        response = await async_client.post(f"/upload/submit?q={token}", json=payload)
        content = response.json()
        assert response.status_code == 422, (
            f"Expected 422, received {response.status_code} with message '{content['message']}'"
        )
        assert {"field": "batches", "message": "There was an error with one or more of the uploads."} in content['data']['errors'], (
            f"Did not receive the expected error, received {content['data']['errors']}"
        )

        # Step 3: Upload PDFs for each batch
        pdf_filepath = os.path.join(TEST_REGISTER_LOCATION, pdf_filename)
        for batch in batches:
            formdata = {"data": json.dumps({"batch": batch, "candidates": candidates})}
            files = {"file": (pdf_filename, open(pdf_filepath, "rb"), "application/pdf")}
            response = await async_client.post(f"/upload/file_upload?q={token}", data=formdata, files=files)
            assert response.status_code == 200, f"Expected 200 on file_upload, received {response.status_code}"
            batch.setdefault('file_uploads', []).append({"file_name": response.json()['data']['filename']})

        # Step 4: Submit with all files — mock Files.com upload so test works without network access
        payload = {"data": {"batches": batches, "candidates": candidates}}
        with patch('src.services.file_handling.FileHandler.upload_file'), \
             patch('src.services.file_handling.FileHandler.delete_file'):
            response = await async_client.post(f"/upload/submit?q={token}", json=payload)
        content = response.json()
        assert response.status_code == 200, (
            f"Expected 200, received {response.status_code} with message '{content['message']}'"
        )