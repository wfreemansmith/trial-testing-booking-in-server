from src.utils import format_version_id, get_candidate_range, url_contructor, message_editor
import pytest


@pytest.mark.parametrize(
        "paper, component, version, expected", 
        [
            ("AC", "R", "IP123", "ACRIP123"),
            ("AC", "Reading", "IP123", "ACRIP123"),
            ("GT", "W", "NP345", "GTWNP345"),
            ("GT", "Writing", "NP345", "GTWNP345"),
            ("AC", "L", "BP43", "LBP43"),
            ("AC", "Listening", "BP43", "LBP43")
        ]
    )
def test_format_version_id(paper, component, version, expected):
    output = format_version_id(paper=paper, component=component, version=version)
    assert output == expected


@pytest.mark.parametrize(
        "args, expected",
        [
            ( ["AOG/IELTS Ops/", "Trial Testing/"], "AOG/IELTS Ops/Trial Testing/" ),
            ( ["AOG", "IELTS Ops", "Trial Testing"], "AOG/IELTS Ops/Trial Testing/" )
        ]
    )
def test_url_helper(args, expected):
    result = url_contructor(*args)
    assert result == expected


@pytest.mark.parametrize(
        "candidate_nums, expected",
        [
            ([1, 2, 3, 4, 5], "0001-0005"),
            ([34, 12, 99, 102], "0012-0102"),
            ([89], "0089"),
            (["34", 32], "0032-0034"),
            ([], None)
        ]
)
def test_get_candidate_range(candidate_nums, expected):
    output = get_candidate_range(candidate_nums)
    assert output == expected


@pytest.mark.parametrize(
        "message, kwargs, expected",
        [
            ( "My name is {name}", {"name": "David"}, "My name is David" ),
            ( "David is a {blank} {noun}", {"blank": "Great", "noun": "Duck"}, "David is a Great Duck" )
        ]
    )
def test_message_editor(message, kwargs, expected):
    result = message_editor(message, **kwargs)
    assert result == expected