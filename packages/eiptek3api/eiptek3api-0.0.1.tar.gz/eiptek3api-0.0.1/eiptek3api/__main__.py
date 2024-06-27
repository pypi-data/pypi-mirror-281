import sys
import json
from api import Project, api_projects_all, EIP_TEK3_URL
from filter import filter_it
from stats import full_stats


def filter_projects(projects: list[Project], filters: list[str]):
    _filters = []
    for _filter in filters:
        split_name, split_value = _filter.split("=", maxsplit=1)
        splited_name = split_name.split("__")
        _filters.append((splited_name, split_value))
    return filter_it(projects, _filters)


def get_bearer():
    try:
        with open(".bearer", "r") as f:
            bearer = f.read().strip("\n ")
            return bearer
    except:
        bearer = input("Bearer: ")
        return bearer.strip("\n ")


bearer = get_bearer()
projects = api_projects_all(
    bearer=bearer,
    include_rejected=True,
)

if len(sys.argv) == 1:
    print(
        json.dumps(
            full_stats(projects.results),
            indent=4,
        )
    )
else:
    projs = filter_projects(projects.results, sys.argv[1:])
    for proj in projs:
        print(EIP_TEK3_URL + "projects/" + str(proj.id))
    print(
        json.dumps(
            full_stats(projs),
            indent=4,
        )
    )
