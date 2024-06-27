import msgspec

from lueur.platform.gcp.client import Client

__all__ = ["list_project_regions"]


async def list_project_regions(project: str) -> list[str]:
    async with Client("https://compute.googleapis.com") as c:
        response = await c.get(
            f"/compute/v1/projects/{project}/regions",
            params={"fields": "items.name"},
        )

        regions = msgspec.json.decode(response.content)

        return [r["name"] for r in regions["items"]]
