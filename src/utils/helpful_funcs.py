from typing import List
import urllib.parse

def format_version_id(paper: str, component: str, version: str) -> str:
    """Given the paper, component and version, returns a version id
    For component can accept either full string or first letter"""
    if component.upper() in ("L", "LISTENING"):
        return f"L{version}"
    else:
        return f"{paper}{component[0]}{version}".upper()

def construct_upload_path(window: str, partner: str, centre_number: str) -> str:
    """Returns full upload destination as required by Files.com"""
    from src.config import FILE_UPLOAD_BASE_URL
    return url_contructor(FILE_UPLOAD_BASE_URL, f"IELTS Trial Testing {window}", partner, centre_number)

def construct_upload_filename(centre_id: str, version_id: str, lowest_cand: int, highest_cand: int, num_of_cands: int):
    """
    Returns filename in agreed naming convention:
    Pretest Centre Number_Version_Candidate Range_Number of Candidates
    """
    return f"{centre_id}_{version_id}_{str(lowest_cand).zfill(4)}-{str(highest_cand).zfill(4)}_{num_of_cands} candidates"

def message_editor(message: str, **kwargs) -> str:
    """Accepts message and keyword arguments, replaces keywords in message with values of argument"""
    edited_message = message
    for key, value in kwargs.items():
        print(key, value)
        edited_message = edited_message.replace("{"+key+"}", value)
    return edited_message

def url_contructor(*args: List[str]) -> str:
    """Accepts a flexible number of url elements and returns a full url"""
    url_bits = [bit + "/" if not bit.endswith("/") else bit for bit in list(args)]
    base_url = url_bits[0]

    for bit in url_bits[1:]:
        base_url = urllib.parse.urljoin(base_url, bit)
    
    return base_url

def get_candidate_range(candidate_nums: List[int]) -> str | None:
    """Accepts a list of integeres and returns a string of candidate range e.g. 0001-0049"""
    candidate_nums = [int(n) for n in candidate_nums]
    zstring = lambda n: str(n).zfill(4)
    
    if len(candidate_nums) > 1:
        return f"{zstring(min(candidate_nums))}-{zstring(max(candidate_nums))}"
    elif len(candidate_nums) == 1:
        return f"{zstring(candidate_nums[0])}"
    else:
        return None
    
def serialise_pydantic_list(list: list) -> list:
    """Turns a list of pydantic models back into list of dicts"""
    return [item.model_dump() for item in list]

## Other potentially useful functions
# Getting the CCF code from a candidate reponses (e.g i=A, ii=B, etc)
# Getting the bandscore for a candidates Reading, Listening and Writing scores
# Geeting T1 and T2 scores, plus overall bandscores, for Writing scores