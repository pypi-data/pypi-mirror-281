import sys
from time import sleep
from datetime import datetime
from dataclasses import dataclass, asdict
from dateutil.parser import parse
from requests import get

EIP_TEK3_URL = "https://eip-tek3.epitest.eu/"
EIP_TEK3_API_URL = EIP_TEK3_URL + "api/"

CURRENT_SCHOLAR_YEAR = datetime.now().year
if datetime.now().month < 8:
    CURRENT_SCHOLAR_YEAR = CURRENT_SCHOLAR_YEAR - 1


def to_dict(obj):
    res = {}
    for k, v in asdict(obj).items():
        if isinstance(v, (Tag, City, Member, Project, Projects)):
            res[k] = v.dict()
        if (
            isinstance(v, list)
            and len(v) != 0
            and isinstance(v[0], (Tag, City, Member, Project))
        ):
            res[k] = [v_elem.dict for v_elem in v]
        else:
            res[k] = v
    return res


@dataclass(kw_only=True)
class Tag:
    """
    Tag of a project

    Attributes
    ----------
    id : str
        tag id
    label : str
        tag human displayable
    label_fr : str
        tag human displayable (in french)
    color : str
        hexadecimal color

    Methods
    -------
    dict()
        get the datas as python dict (recursif)
    """

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
        return to_dict(self)


@dataclass(kw_only=True)
class City:
    """
    City of an epitech campus

    Attributes
    ----------
    code : str
        Country code followed by the City code (i.e.: FR/PAR)
    name : str
        City name (i.e.: Paris)

    Methods
    -------
    dict()
        get the datas as python dict (recursif)
    """

    code: str
    name: str

    @staticmethod
    def from_js(obj: dict):
        return City(
            code=obj.get("code"),
            name=obj.get("name"),
        )

    def dict(self):
        return to_dict(self)


@dataclass(kw_only=True)
class Member:
    """
    Member in a Project

    Attributes
    ----------
    login : str
        epitech email
    accepted : bool
        whether or not the member accepted to be in the group
    lastname : str
        lastname (can contain multiple lastname, separated by space)
    firstname : str
        firstname (can contain multiple firstname, separated by space)
    city : City
        which epitech city he is

    Methods
    -------
    dict()
        get the datas as python dict (recursif)
    """

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
        return to_dict(self)


@dataclass(kw_only=True)
class Project:
    """
    Project created by students

    Attributes
    ----------
    scholar_year : int
        (i.e. for 2023/2024: 2023)
    document_uploaded : bool
        whether or not the document (slide deck) is uploaded
    video_uploaded : bool
        whether or not the video is uploaded
    id : str
        project id (you can see it in the url when you click on a project)
    name : str
        project name
    description : str
        project description
    owner : str
        login of the member owner
    members : list[Member]
        list of Member (if they have not accepted yet, they will be on the list too)
    owner_city : City
        Epitech campus of the owner
    looking_for_members : bool
        whether or not the group are looking for members
    status : str
        can be ["waiting_update", "rejected", "draft", "approved", "pending"]
    envisaged_type : str
        can be ["solution", "entrepreneurship", "technical"]
    created_at : datetime
        when the project was created
    updated_at : datetime
        when the project was updated
    tags : list[Tag]
        list of Tag
    views_count : int
        number of views on the website
    stars_count : int
        number of stars
    starred : bool
        whether or not you starred the project

    Methods
    -------
    dict()
        get the datas as python dict (recursif)
    """

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
        return to_dict(self)


@dataclass
class Projects:
    """
    Projects is the result of api_projects

    Attributes
    ----------
    results : list[Project]
        list of Project
    next : int
        next chunk available (i.e.: 20)
    total : int
        number of project for the request

    Methods
    -------
    dict()
        get the datas as python dict (recursif)
    """

    results: list[Project]
    next: int
    total: int

    @staticmethod
    def from_js(obj: dict):
        return Projects(
            results=[Project.from_js(obj) for obj in obj.get("results")],
            next=int(obj.get("next", 0)),
            total=int(obj.get("total")),
        )

    def dict(self):
        return to_dict(self)


def api_projects_count(
    bearer: str,
    scholar_year: int = CURRENT_SCHOLAR_YEAR,
    user_projects: bool = False,
    starred_projects: bool = False,
    include_rejected: bool = False,
):
    """
    Get the number of project completed the criterias in parameters

    Parameters
    ----------
    bearer : str
        bearer token (stating with "ey")
    scholar_year : int, optional
        default=CURRENT_SCHOLAR_YEAR
        (i.e. for 2023/2024: 2023)
    user_projects : bool, optional
        default=False
        whether or not only include your projects
    starred_projects : bool, optional
        default=False
        whether or not only include your starred projects
    include_rejected : bool, optional
        default=False
        whether or not include to the current projects, the projects rejected

    Returns
    -------
    int
        the number of projects completed the criterias
    """

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
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": EIP_TEK3_API_URL + "projects?scholar_year" + str(scholar_year),
        "Authorization": "Bearer " + bearer,
    }
    res = get(url, headers=headers)
    res.raise_for_status()
    return int(res.json()["count"])


def api_projects(
    bearer: str,
    scholar_year: int = CURRENT_SCHOLAR_YEAR,
    user_projects: bool = False,
    starred_projects: bool = False,
    limit: int = 20,
    offset: int = 0,
    include_rejected: bool = False,
    debug: bool = False,
):
    """
    Get a chunk of projects completed the criterias in parameters

    Parameters
    ----------
    bearer : str
        bearer token (stating with "ey")
    scholar_year : int, optional
        default=CURRENT_SCHOLAR_YEAR
        (i.e. for 2023/2024: 2023)
    user_projects : bool, optional
        default=False
        whether or not only include your projects
    starred_projects : bool, optional
        default=False
        whether or not only include your starred projects
    limit : int, optional
        default=20
        number of project to include (max is 100 per requests)
        if you want all projects matching your criterias, use the function api_projects_all
    offset : int, optional
        default=0
        where to start in the array of projects
    include_rejected : bool, optional
        default=False
        whether or not include to the current projects, the projects rejected
    debug : bool, optional
        default=False
        whether or not additional debug print are added

    Returns
    -------
    Projects
        the result of the api parsed to the class Projects, Project, Member, City, Tag
    """

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
    if debug:
        print("url=", url, file=sys.stderr)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": EIP_TEK3_API_URL + "projects?scholar_year" + str(scholar_year),
        "Authorization": "Bearer " + bearer,
    }
    res = get(url, headers=headers)
    res.raise_for_status()
    return Projects.from_js(res.json())


def api_projects_all(
    bearer: str,
    scholar_year: int = CURRENT_SCHOLAR_YEAR,
    user_projects: bool = False,
    starred_projects: bool = False,
    include_rejected: bool = False,
    debug=False,
):
    """
    Get all projects completed the criterias in parameters

    Parameters
    ----------
    bearer : str
        bearer token (stating with "ey")
    scholar_year : int, optional
        default=CURRENT_SCHOLAR_YEAR
        (i.e. for 2023/2024: 2023)
    user_projects : bool, optional
        default=False
        whether or not only include your projects
    starred_projects : bool, optional
        default=False
        whether or not only include your starred projects
    include_rejected : bool, optional
        default=False
        whether or not include to the current projects, the projects rejected
    debug : bool, optional
        default=False
        whether or not additional debug print are added

    Returns
    -------
    Projects
        the result of the api parsed to the class Projects, Project, Member, City, Tag
    """
    offset = 0
    res = Projects(results=[], next=20, total=20)
    while len(res.results) < res.total:
        res2 = api_projects(
            bearer=bearer,
            scholar_year=scholar_year,
            user_projects=user_projects,
            starred_projects=starred_projects,
            limit=20,
            offset=offset,
            include_rejected=include_rejected,
            debug=debug,
        )
        res.results.extend(res2.results)
        res.next = res2.next
        res.total = res2.total
        offset += len(res2.results)
        if debug:
            print("offset=", offset, file=sys.stderr)
    return res
