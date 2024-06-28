try:
    from eiptek3api.api import (
        Projects,
        Project,
        Member,
        City,
        Tag,
        api_projects_count,
        api_projects,
        api_projects_all,
    )
    from eiptek3api.stats import (
        number_status,
        number_city,
        number_status_by_city,
        number_by_type,
        number_status_by_type,
        number_status_by_tags,
        full_stats,
    )
    from eiptek3api.filter import filter_it
except ModuleNotFoundError:
    from api import (
        Projects,
        Project,
        Member,
        City,
        Tag,
        api_projects_count,
        api_projects,
        api_projects_all,
    )
    from stats import (
        number_status,
        number_city,
        number_status_by_city,
        number_by_type,
        number_status_by_type,
        number_status_by_tags,
        full_stats,
    )
    from filter import filter_it


__all__ = [
    "Projects",
    "Project",
    "Member",
    "City",
    "Tag",
    "api_projects_count",
    "api_projects",
    "api_projects_all",
    "number_status",
    "number_city",
    "number_status_by_city",
    "number_by_type",
    "number_status_by_type",
    "number_status_by_tags",
    "full_stats",
    "filter_it",
]
