def format_version_id(paper: str, component: str, version: str) -> str:
    """Given the paper, component and version, returns a version id
    For component can accept either full string or first letter"""
    if component.upper() in ("L", "LISTENING"):
        return f"L{version}"
    else:
        return f"{paper}{component[0]}{version}".upper()

def construct_upload_path(window: str, partner: str, centre_number: str) -> str:
    """Returns full upload destination as required by Files.com"""
    from config import FILE_UPLOAD_BASE_URL
    return f"{FILE_UPLOAD_BASE_URL}/{window}/{partner}/{centre_number}/"

## Other potentially useful functions
# Getting the CCF code from a candidate reponses (e.g i=A, ii=B, etc)
# Getting the bandscore for a candidates Reading, Listening and Writing scores
# Geeting T1 and T2 scores, plus overall bandscores, for Writing scores