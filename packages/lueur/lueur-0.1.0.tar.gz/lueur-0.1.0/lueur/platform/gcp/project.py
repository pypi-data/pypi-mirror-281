import msgspec

from lueur.make_id import make_id
from lueur.models import GCPProject
from lueur.platform.gcp.client import Client

__all__ = ["list_all_projects", "list_organization_projects"]


async def list_organization_projects(organization_id: str) -> list[str]:
    async with Client("https://cloudresourcemanager.googleapis.com") as c:
        response = await c.get(
            "/v3/projects",
            params={"parent": f"organizations/{organization_id}"},
        )

        projects = msgspec.json.decode(response.content)

        return [p["name"] for p in projects["projects"]]


async def list_all_projects() -> list[GCPProject]:
    async with Client("https://cloudresourcemanager.googleapis.com") as c:
        response = await c.get(
            "/v3/projects:search", params={"query": "state:ACTIVE"}
        )

        projects = msgspec.json.decode(response.content)

        result = []

        result.extend(
            [
                GCPProject(
                    organization=p["parent"],
                    id=make_id(p["name"]),
                    name=p["displayName"],
                )
                for p in projects["projects"]
            ]
        )

        return result
