import httpx
from typing import List, Dict
from models.models import Dependency
from cache import SimpleCache

cache = SimpleCache(ttl=3600)

def parse_requirements(req_str: str) -> List[Dependency]:
    deps = []
    for line in req_str.strip().splitlines():
        if "==" in line:
            name, version = line.strip().split("==")
            deps.append(Dependency(name=name.lower(), version=version))
    return deps

async def check_vulnerability(dep: Dependency) -> Dependency:
    cache_key = f"{dep.name}@{dep.version}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    query = {
        "package": {
            "name": dep.name,
            "ecosystem": "PyPI"
        },
        "version": dep.version
    }

    async with httpx.AsyncClient() as client:
        r = await client.post("https://api.osv.dev/v1/query", json=query)
        result = r.json()

    dep.is_vulnerable = "vulns" in result
    dep.vulnerabilities = result.get("vulns", [])
    cache.set(cache_key, dep)
    return dep
