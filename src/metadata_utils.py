import re
def infer_role(source):
    """
    Assign role based on document type
    """
    if "leave" in source:
        return "employee"
    if "conduct" in source:
        return "all"
    if "security" in source:
        return "all"
    if "benefits" in source:
        return "employee"
    return "all"


def extract_section(text):
    """
    Simple heuristic: extract section number if exists
    """
    
    match = re.search(r"\d+\.\d+", text)
    return match.group() if match else "general"