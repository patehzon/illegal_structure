from typing import Any


DEMO_BUILDINGS: list[dict[str, Any]] = [
    {
        "building_id": "PARIS-DEMO-0001",
        "address": "10 Rue de Rivoli",
        "arrondissement": 1,
        "height_m": 16.0,
        "primary_use": "residential",
        "zone_code": "R1",
        "heritage_protected": False,
    },
    {
        "building_id": "PARIS-DEMO-0002",
        "address": "12 Avenue de Clichy",
        "arrondissement": 17,
        "height_m": 22.0,
        "primary_use": "residential",
        "zone_code": "R1",
        "heritage_protected": False,
    },
    {
        "building_id": "PARIS-DEMO-0003",
        "address": "5 Rue du Chevaleret",
        "arrondissement": 13,
        "height_m": 20.0,
        "primary_use": "industrial",
        "zone_code": "C1",
        "heritage_protected": False,
    },
    {
        "building_id": "PARIS-DEMO-0004",
        "address": "3 Boulevard de Belleville",
        "arrondissement": 20,
        "height_m": None,
        "primary_use": "mixed_use",
        "zone_code": "C1",
        "heritage_protected": False,
    },
    {
        "building_id": "PARIS-DEMO-0005",
        "address": "8 Place des Vosges",
        "arrondissement": 4,
        "height_m": 17.5,
        "primary_use": "residential",
        "zone_code": "R1",
        "heritage_protected": True,
    },
]


def list_demo_buildings() -> list[dict[str, Any]]:
    return [building.copy() for building in DEMO_BUILDINGS]


def get_demo_building(building_id: str) -> dict[str, Any] | None:
    for building in DEMO_BUILDINGS:
        if building["building_id"] == building_id:
            return building.copy()
    return None
