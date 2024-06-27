import sys
from datetime import datetime
from dataclasses import dataclass, asdict
from dateutil.parser import parse
from requests import get

EIP_TEK3_URL = "https://eip-tek3.epitest.eu/"
EIP_TEK3_API_URL = EIP_TEK3_URL + "api/"

CURRENT_SCHOLAR_YEAR = datetime.now().year
if datetime.now().month < 8:
    CURRENT_SCHOLAR_YEAR = CURRENT_SCHOLAR_YEAR - 1


@dataclass(kw_only=True)
class Tag:
    id: str
    label: str
    label_fr: str
    color: str

    @staticmethod
    def from_js(obj: dict):
        return Tag(
            id=obj.get("id"),
            label=obj.get("label"),
            label_fr=obj.get("label_fr"),
            color=obj.get("color"),
        )

    def dict(self):
        res = {}
        for k, v in asdict(self).items():
            if isinstance(v, (Tag, City, Member, Project)):
                res[k] = v.dict()
            else:
                res[k] = v
        return res


@dataclass(kw_only=True)
class City:
    code: str
    name: str

    @staticmethod
    def from_js(obj: dict):
        return City(
            code=obj.get("code"),
            name=obj.get("name"),
        )

    def dict(self):
        res = {}
        for k, v in asdict(self).items():
            if isinstance(v, (Tag, City, Member, Project)):
                res[k] = v.dict()
            else:
                res[k] = v
        return res


@dataclass(kw_only=True)
class Member:
    login: str
    accepted: bool
    lastname: str
    firstname: str
    city: City

    @staticmethod
    def from_js(obj: dict):
        return Member(
            login=obj.get("login"),
            accepted=bool(obj.get("accepted")),
            lastname=obj.get("lastname"),
            firstname=obj.get("firstname"),
            city=City.from_js(obj.get("city")),
        )

    def dict(self):
        res = {}
        for k, v in asdict(self).items():
            if isinstance(v, (Tag, City, Member, Project)):
                res[k] = v.dict()
            else:
                res[k] = v
        return res


@dataclass(kw_only=True)
class Project:
    scholar_year: int
    document_uploaded: bool
    video_uploaded: bool
    id: str
    name: str
    description: str
    owner: str
    members: list[Member]
    owner_city: City
    looking_for_members: bool
    status: str
    envisaged_type: str
    created_at: datetime
    updated_at: datetime
    tags: list[Tag]
    views_count: int
    stars_count: int
    starred: bool

    @staticmethod
    def from_js(obj: dict):
        return Project(
            scholar_year=int(obj.get("scholarYear")),
            document_uploaded=bool(obj.get("documentUploaded")),
            video_uploaded=bool(obj.get("videoUploaded")),
            id=obj.get("id"),
            name=obj.get("name"),
            description=obj.get("description"),
            owner=obj.get("owner"),
            members=[Member.from_js(x) for x in obj.get("members")],
            owner_city=City.from_js(obj.get("ownerCity")),
            looking_for_members=bool(obj.get("lookingForMembers")),
            status=obj.get("status"),
            envisaged_type=obj.get("envisagedType"),
            created_at=parse(obj.get("createdAt")),
            updated_at=parse(obj.get("createdAt")),
            tags=[Tag.from_js(x) for x in obj.get("tags")],
            views_count=int(obj.get("viewsCount")),
            stars_count=int(obj.get("starsCount")),
            starred=bool(obj.get("starred")),
        )

    def dict(self):
        res = {}
        for k, v in asdict(self).items():
            if isinstance(v, (Tag, City, Member, Project)):
                res[k] = v.dict()
            else:
                res[k] = v
        return res


@dataclass
class Projects:
    results: list[Project]
    next: int
    total: int

    @staticmethod
    def from_js(obj: dict):
        return Projects(
            results=[Project.from_js(obj) for obj in obj.get("results")],
            next=int(obj.get("next")),
            total=int(obj.get("total")),
        )


def api_projects_count(
    bearer: str,
    scholar_year: int = CURRENT_SCHOLAR_YEAR,
    user_projects: bool = False,
    starred_projects: bool = False,
    include_rejected: bool = False,
):
    _user_projects = "true" if user_projects else "false"
    _starred_projects = "true" if starred_projects else "false"
    _include_rejected = "true" if include_rejected else "false"
    url = (
        EIP_TEK3_API_URL
        + "projects/count?"
        + "scholar_year="
        + str(scholar_year)
        + "&user_projects="
        + _user_projects
        + "&starred_projects="
        + _starred_projects
        + "&limit=20"
        + "&include_rejected="
        + _include_rejected
    )
    headers = {"Authorization": "Bearer " + bearer}
    res = get(url, headers=headers)
    return int(res.json()["count"])


def api_projects(
    bearer: str,
    scholar_year: int = CURRENT_SCHOLAR_YEAR,
    user_projects: bool = False,
    starred_projects: bool = False,
    limit: int = 20,
    offset: int = 0,
    include_rejected: bool = False,
):
    _user_projects = "true" if user_projects else "false"
    _starred_projects = "true" if starred_projects else "false"
    _include_rejected = "true" if include_rejected else "false"
    url = (
        EIP_TEK3_API_URL
        + "projects?"
        + "scholar_year="
        + str(scholar_year)
        + "&user_projects="
        + _user_projects
        + "&starred_projects="
        + _starred_projects
        + "&limit="
        + str(limit)
        + "&offset="
        + str(offset)
        + "&include_rejected="
        + _include_rejected
    )
    headers = {"Authorization": "Bearer " + bearer}
    res = get(url, headers=headers)
    return Projects.from_js(res.json())


def api_projects_all(
    bearer: str,
    scholar_year: int = CURRENT_SCHOLAR_YEAR,
    user_projects: bool = False,
    starred_projects: bool = False,
    include_rejected: bool = False,
    debug=False,
):
    offset = 0
    res = Projects(results=[], next=20, total=20)
    while len(res.results) < res.total:
        res2 = api_projects(
            bearer=bearer,
            scholar_year=scholar_year,
            user_projects=user_projects,
            starred_projects=starred_projects,
            limit=20,
            offset=0,
            include_rejected=include_rejected,
        )
        res.results.extend(res2.results)
        res.next = res2.next
        res.total = res2.total
        offset += len(res2.results)
        print("offset=", offset)
    return res
