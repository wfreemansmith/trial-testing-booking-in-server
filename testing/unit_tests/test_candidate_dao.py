import pytest
from testing.test_data.uploads import upload_preview_expected_res, complete_upload_json
from src.dao import CandidateDAO, UploadDAO
import copy

class TestUnitCandidateDAO:
    DUPLICATE_TEST_CASES = [
        (
            copy.deepcopy(entry),
            entry.get('marking_window_id'),
            entry.get('centre_id'),
            [[candidate['candidate_number'], candidate['candidate_name']] for candidate in entry['candidates']]
        )
        for entry in complete_upload_json
    ]
    @pytest.mark.parametrize("input_data, marking_window_id, centre_id, candidates_to_test", DUPLICATE_TEST_CASES)
    def test_for_duplicates(self, db_session, input_data, marking_window_id, centre_id, candidates_to_test):
        # ARRANGE
        candidate_dao = CandidateDAO(session=db_session)
        upload_dao = UploadDAO(session=db_session)

        # Testing before candidates have been uploaded
        # ASSERT
        result = candidate_dao.is_duplicate_candidate(marking_window_id=marking_window_id, centre_id=centre_id, candidates=candidates_to_test)
        assert all(check == False for check in result), (
            f"Test is finding candidates where there are no candidates"
        )
        
        # Testing after candidates have been uploaded
        # ACT
        upload_dao.insert_upload(data=input_data)
        result = candidate_dao.is_duplicate_candidate(marking_window_id=marking_window_id, centre_id=centre_id, candidates=candidates_to_test)
        assert all(check == True for check in result), (
            f"Test is not picking up duplicates"
        )

        # Testing with one new candidate
        # ARRANGE
        new_cand = [len(candidates_to_test) + 1, "David Baritone"]
        new_candidate_added = candidates_to_test.copy()
        new_candidate_added.append(new_cand)
        
        # ACT
        result = candidate_dao.is_duplicate_candidate(marking_window_id=marking_window_id, centre_id=centre_id, candidates=new_candidate_added)
        
        # ASSERT
        expected_result = [True] * (len(candidates_to_test)) + [False]
        assert result == expected_result, (
            f"Test expected {expected_result}, received {result}"
        )

        # Testing when candidate numbers are duplcated but names are not
        # ARRANGE
        duplicate_numbers_not_names = [[candidate[0], "Imaginary Name"] for candidate in candidates_to_test]
        next_cand_number = max(candidate[0] for candidate in candidates_to_test) + 1

        # ACT
        result = candidate_dao.is_duplicate_candidate(marking_window_id=marking_window_id, centre_id=centre_id, candidates=duplicate_numbers_not_names)

        # ASSERT
        expected_result = [n for n in range(next_cand_number, next_cand_number + len(candidates_to_test))]
        assert result == expected_result, (
            f"Test expected {expected_result}, received {result}"
        )

        # Testing with some duplicates numbers, some new
        # ARRANGE
        some_duplicate_some_new = duplicate_numbers_not_names.copy()
        some_duplicate_some_new.append(new_cand)
        next_cand_number = new_cand[0] + 1
        expected_result = [*[n for n in range(next_cand_number, next_cand_number + len(duplicate_numbers_not_names))], False]

        # ACT
        result = candidate_dao.is_duplicate_candidate(marking_window_id=marking_window_id, centre_id=centre_id, candidates=some_duplicate_some_new)

        # ASSERT
        assert result == expected_result, (
            f"Test expected {expected_result}, received {result}"
        )