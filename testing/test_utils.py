from src.utils import format_version_id
import pytest

@pytest.mark.parametrize(
        "paper, component, version, result", 
        [
            ("AC", "R", "IP123", "ACRIP123"),
            ("AC", "Reading", "IP123", "ACRIP123"),
            ("GT", "W", "NP345", "GTWNP345"),
            ("GT", "Writing", "NP345", "GTWNP345"),
            ("AC", "L", "BP43", "LBP43"),
            ("AC", "Listening", "BP43", "LBP43")
        ]
    )
def test_format_version_id(paper, component, version, result):
    output = format_version_id(paper=paper, component=component, version=version)
    assert output == result