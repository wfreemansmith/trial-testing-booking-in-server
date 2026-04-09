import pytest
import copy
from testing.test_data.uploads import upload_preview_expected_res, complete_upload_json
from src.dao.upload_dao import UploadDAO

DAO_STRIP_KEYS = ('token')


def for_dao(data: dict) -> dict:
    """Strip route-layer keys before passing to DAO/model."""
    return {k: v for k, v in data.items() if k not in DAO_STRIP_KEYS}


class TestUnitUploadDAO:
    COMPLETE_UPLOAD_TEST_DATA = [
        (copy.deepcopy(entry),
         entry.get('marking_window_id'),
         entry.get('centre_id'),
         entry.get('batches'),
         entry.get('candidates'))
        for entry in complete_upload_json
    ]
    COMPLETE_UPLOAD_TEST_IDS = [f"{entry.get('marking_window_id','XXX')}_{entry.get('centre_id', 'XXX')}" for entry in complete_upload_json]

    @pytest.mark.parametrize("input_data, marking_window_id, centre_id, batches, candidates", COMPLETE_UPLOAD_TEST_DATA, ids=COMPLETE_UPLOAD_TEST_IDS)
    def test_succesful_create_upload_object(self, db_session, input_data, marking_window_id, centre_id, batches, candidates):
        dao = UploadDAO(session=db_session)
        upload_object = dao.create_upload_object(data=for_dao(input_data), marking_window_id=marking_window_id, centre_id=centre_id)
        
        expected_part_delivery = "A"
        assert upload_object.part_delivery == expected_part_delivery, (
            f"Part delivery not created correctly, expected '{expected_part_delivery}' received '{upload_object.part_delivery}'"
        )

        expected_upload_id = f"{marking_window_id}_{centre_id}_{expected_part_delivery}"
        assert upload_object.upload_id == expected_upload_id, (
            f"Upload ID not initialised correctly, expected '{expected_upload_id}', received '{upload_object.upload_id}'"
        )

        expected_batch_ids = [f"{expected_upload_id}_{batch['version_id']}" for batch in batches]
        for expected_batch_id in expected_batch_ids:
            match = sum(batch.batch_id == expected_batch_id for batch in upload_object.batches)
            assert match == 1, (
                f"Unique Batch IDs not initalised correctly, expected '{expected_batch_id}' but test found {match} results with that name"
            )

        expected_candidate_ids = [f"{expected_upload_id}_{str(candidate['candidate_number']).zfill(4)}" for candidate in candidates]
        for expected_candidate_id in expected_candidate_ids:
            match = sum(candidate.candidate_id == expected_candidate_id for candidate in upload_object.candidates)
            assert match == 1, (
                f"Unique Candidate IDs not initalised correctly, expected '{expected_candidate_id}' but test found {match} results with that name"
            )
