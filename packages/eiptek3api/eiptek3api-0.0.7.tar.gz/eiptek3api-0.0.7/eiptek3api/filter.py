import sys

try:
    from eiptek3api.api import Project
except ModuleNotFoundError:
    from api import Project


def get_item(obj, word: str):
    res = []
    if isinstance(obj, dict) and word in obj.keys():
        res.append(obj[word])
    elif isinstance(obj, list):
        for obj_elem in obj:
            res.extend(get_item(obj_elem, word))
    return res


def check_item(obj, value: str, comparatif: str):
    if isinstance(obj, list):
        return any([check_item(elem, value, comparatif) for elem in obj])
    elif comparatif == "eq":
        return str(obj) == value
    elif comparatif == "contains":
        return value in str(obj)
    else:
        print(f"Bad comparatif('{comparatif}') / filter", file=sys.stderr)
        return False


def filter_it(projects: list[Project], filters: list[tuple[list[str], str]]):
    """
    filters a list of Project

    Parameters
    ----------
    projects : list[Project]
        list of project to filter
    filters: list[tuple[list[str], str]]
        list of tuple of
        - [0]: select the field to compare to a value, ending with __eq, or __contains (i.e.: tags__label will select the field label in the field tags)
        - [1]: the value to compare with

    Returns
    -------
    list[Project]
        list of projects matching your filters
    """
    projects_res = []
    for project in projects:
        valid = True
        for field, value in filters:
            comparatif = "eq"
            if field[-1] in ("eq", "contains"):
                comparatif = field[-1]
                field = field[:-1]
            cursors = [project.dict()]
            for word in field:
                cursors_2 = []
                for cursor in cursors:
                    cursors_2.extend(get_item(cursor, word))
                cursors = cursors_2
            if not any([check_item(obj, value, comparatif) for obj in cursors]):
                valid = False
                break
        if not valid:
            continue
        projects_res.append(project)
    return projects_res
