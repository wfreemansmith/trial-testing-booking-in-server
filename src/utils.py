def format_version_id(paper: str, component: str, version: str) -> str:
    """Given the paper, component and version, returns a version id
    For component can accept either full string or first letter"""
    if component.upper() in ("L", "LISTENING"):
        return f"L{version}"
    else:
        return f"{paper}{component[0]}{version}".upper()