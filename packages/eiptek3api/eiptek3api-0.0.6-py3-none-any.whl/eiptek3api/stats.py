import collections
try:
    from eiptek3api.api import Project
except ModuleNotFoundError:
    from api import Project


def number_status(projects: list[Project]):
    status = {}
    for proj in projects:
        if proj.status not in status:
            status[proj.status] = 0
        status[proj.status] += 1
    return collections.OrderedDict(
        sorted(status.items(), key=lambda x: x[1], reverse=True)
    )


def number_city(projects: list[Project]):
    cities = {}
    for proj in projects:
        if proj.owner_city.name not in cities:
            cities[proj.owner_city.name] = 0
        cities[proj.owner_city.name] += 1
    return collections.OrderedDict(
        sorted(cities.items(), key=lambda x: x[1], reverse=True)
    )


def number_status_by_city(projects: list[Project]):
    cities = {}
    for proj in projects:
        if proj.owner_city.name not in cities:
            cities[proj.owner_city.name] = {}
        if proj.status not in cities[proj.owner_city.name]:
            cities[proj.owner_city.name][proj.status] = 0
        cities[proj.owner_city.name][proj.status] += 1
    return {
        city: collections.OrderedDict(
            sorted(status.items(), key=lambda x: x[1], reverse=True)
        )
        for city, status in cities.items()
    }


def number_by_type(projects: list[Project]):
    types = {}
    for proj in projects:
        if proj.envisaged_type not in types:
            types[proj.envisaged_type] = 0
        types[proj.envisaged_type] += 1
    return collections.OrderedDict(
        sorted(types.items(), key=lambda x: x[1], reverse=True)
    )


def number_status_by_type(projects: list[Project]):
    types = {}
    for proj in projects:
        if proj.envisaged_type not in types:
            types[proj.envisaged_type] = {}
        if proj.status not in types[proj.envisaged_type]:
            types[proj.envisaged_type][proj.status] = 0
        types[proj.envisaged_type][proj.status] += 1
    return {
        _type: collections.OrderedDict(
            sorted(status.items(), key=lambda x: x[1], reverse=True)
        )
        for _type, status in types.items()
    }


def number_status_by_tags(projects: list[Project]):
    tags = {}
    for proj in projects:
        for tag in proj.tags:
            if tag.label not in tags:
                tags[tag.label] = {}
            if proj.status not in tags[tag.label]:
                tags[tag.label][proj.status] = 0
            tags[tag.label][proj.status] += 1
    return {
        tag: collections.OrderedDict(
            sorted(status.items(), key=lambda x: x[1], reverse=True)
        )
        for tag, status in tags.items()
    }


def full_stats(projects: list[Project]):
    return {
        "number_of_projects": len(projects),
        "number_of_projects_by_cities": number_city(projects),
        "status_all_cities": number_status(projects),
        "status_by_cities": number_status_by_city(projects),
        "number_by_envisaged_type": number_by_type(projects),
        "status_by_envisaged_type": number_status_by_type(projects),
        "number_status_by_tags": number_status_by_tags(projects),
    }
