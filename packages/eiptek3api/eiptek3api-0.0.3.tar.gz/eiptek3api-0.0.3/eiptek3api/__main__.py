import sys
import json
import argparse
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


def main():
    parser = argparse.ArgumentParser(
        description="CLI for https://eip-tek3.epitest.eu stats.",
        epilog="Made with 💜 by Saverio976",
    )
    parser.add_argument(
        "filters",
        type=str,
        nargs="*",
        help="`field__eq=value` or `path__to__field__eq=value` or `field__contains=value`",
    )
    args = parser.parse_args()

    bearer = get_bearer()
    print("Loading data...", file=sys.stderr)
    projects = api_projects_all(
        bearer=bearer,
        include_rejected=True,
    )
    print("Loaded data.", file=sys.stderr)

    if len(args.filters) == 0:
        print(
            json.dumps(
                full_stats(projects.results),
                indent=4,
            )
        )
        return 0

    projs = filter_projects(projects.results, sys.argv[1:])
    stats = full_stats(projs)
    stats["proj_list"] = [EIP_TEK3_URL + "projects/" + str(proj.id) for proj in projs]
    print(
        json.dumps(
            stats,
            indent=4,
        )
    )


if __name__ == "__main__":
    sys.exit(main())
