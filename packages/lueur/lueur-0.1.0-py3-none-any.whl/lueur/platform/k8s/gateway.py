# mypy: disable-error-code="call-arg,index"
import msgspec
from kubernetes import client

from lueur.make_id import make_id
from lueur.models import Meta, Resource
from lueur.platform.k8s.client import AsyncClient, Client

__all__ = ["explore_gateway"]


async def explore_gateway() -> list[Resource]:
    resources = []

    async with Client(client.CoreV1Api) as c:
        namespaces = await list_all_namespaces(c)

    async with Client(client.CustomObjectsApi) as c:
        for ns in namespaces:
            gateways = await explore_namespaced_gateways(c, ns)
            resources.extend(gateways)

    return resources


###############################################################################
# Private functions
###############################################################################
async def list_all_namespaces(c: AsyncClient) -> list[str]:
    response = await c.execute("list_namespace")

    namespaces = msgspec.json.decode(response.data)

    return [ns["metadata"]["name"] for ns in namespaces["items"]]


async def explore_namespaced_gateways(
    c: AsyncClient, ns: str
) -> list[Resource]:
    response = await c.execute(
        "list_namespaced_custom_object",
        group="gateway.networking.k8s.io",
        version="v1",
        plural="gateways",
        namespace=ns,
    )

    if response.status != 200:
        return []

    gateways = msgspec.json.decode(response.data)

    results = []
    for gw in gateways["items"]:
        meta = gw["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=Meta(name=meta["name"], kind="k8s/gateway"),
                struct=gw,
            )
        )

    return results
