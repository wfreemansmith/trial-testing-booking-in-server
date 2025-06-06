import pytest
from src.dao import VersionDAO

class TestUnitVersionDAO:
    def test_select_with_condition(self, db_session):
        dao = VersionDAO(session=db_session)
        results = dao.select(version_name="IP1157")
        assert len(results) == 1, (
            f"Expected 1, recieved {len(results)}"
            )
        
        assert results[0].version_name == "IP1157"
        assert results[0].version_id == "ACWIP1157"
        assert results[0].component_id == "W"
        assert results[0].paper == "AC"
    
    def test_select_without_condition(self, db_session):
        dao = VersionDAO(session=db_session)
        results = dao.select()
        assert len(results) == 8