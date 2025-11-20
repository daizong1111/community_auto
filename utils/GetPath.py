import os
import re

def get_path(path: str = None):
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    if path:
        if "/" in path:
            path = path.split("/")
        elif "\\" in path:
            path = path.split("\\")
        else:
            path = [path]
        return os.path.join(root_path, *path)
    else:
        return root_path


def get_sub_url(url: str):
    pattern = r"(https?://)([^/]+)"
    matches = re.findall(pattern, url)
    domains = [match[1] for match in matches]
    return domains[0]