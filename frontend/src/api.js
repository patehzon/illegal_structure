const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

const fallbackBuildings = [
  {
    building_id: "PARIS-DEMO-0001",
    address: "10 Rue de Rivoli",
    arrondissement: 1,
    status: "legal_today",
    confidence: 0.95,
    rule_version: "2026-baseline",
  },
  {
    building_id: "PARIS-DEMO-0002",
    address: "12 Avenue de Clichy",
    arrondissement: 17,
    status: "illegal_today",
    confidence: 0.9,
    rule_version: "2026-baseline",
  },
  {
    building_id: "PARIS-DEMO-0003",
    address: "5 Rue du Chevaleret",
    arrondissement: 13,
    status: "illegal_today",
    confidence: 0.9,
    rule_version: "2026-baseline",
  },
  {
    building_id: "PARIS-DEMO-0004",
    address: "3 Boulevard de Belleville",
    arrondissement: 20,
    status: "unknown_insufficient_data",
    confidence: 0.2,
    rule_version: "2026-baseline",
  },
  {
    building_id: "PARIS-DEMO-0005",
    address: "8 Place des Vosges",
    arrondissement: 4,
    status: "unknown_insufficient_data",
    confidence: 0.45,
    rule_version: "2026-baseline",
  },
];

const fallbackDetails = {
  "PARIS-DEMO-0001": {
    building_id: "PARIS-DEMO-0001",
    address: "10 Rue de Rivoli",
    arrondissement: 1,
    status: "legal_today",
    confidence: 0.95,
    rule_version: "2026-baseline",
    missing_evidence: [],
    notes: "Evaluated with ruleset 2026-baseline.",
    violations: [],
    explanations: [
      {
        rule_code: "LAND_USE_COMPATIBILITY",
        outcome: "pass",
        message: "Use 'residential' is allowed in zone R1.",
      },
      {
        rule_code: "HEIGHT_MAX_BY_ZONE",
        outcome: "pass",
        message: "Height 16.0m is within the 18.0m limit for zone R1.",
      },
      {
        rule_code: "HERITAGE_OVERRIDE",
        outcome: "pass",
        message: "No heritage-protection flag is present in the MVP evidence bundle.",
      },
    ],
  },
  "PARIS-DEMO-0002": {
    building_id: "PARIS-DEMO-0002",
    address: "12 Avenue de Clichy",
    arrondissement: 17,
    status: "illegal_today",
    confidence: 0.9,
    rule_version: "2026-baseline",
    missing_evidence: [],
    notes: "Evaluated with ruleset 2026-baseline.",
    violations: [
      {
        rule_code: "HEIGHT_MAX_BY_ZONE",
        severity: "high",
        message: "Height 22.0m exceeds the 18.0m limit for zone R1.",
      },
    ],
    explanations: [
      {
        rule_code: "LAND_USE_COMPATIBILITY",
        outcome: "pass",
        message: "Use 'residential' is allowed in zone R1.",
      },
      {
        rule_code: "HEIGHT_MAX_BY_ZONE",
        outcome: "fail",
        message: "Height 22.0m exceeds the 18.0m limit for zone R1.",
      },
      {
        rule_code: "HERITAGE_OVERRIDE",
        outcome: "pass",
        message: "No heritage-protection flag is present in the MVP evidence bundle.",
      },
    ],
  },
  "PARIS-DEMO-0003": {
    building_id: "PARIS-DEMO-0003",
    address: "5 Rue du Chevaleret",
    arrondissement: 13,
    status: "illegal_today",
    confidence: 0.9,
    rule_version: "2026-baseline",
    missing_evidence: [],
    notes: "Evaluated with ruleset 2026-baseline.",
    violations: [
      {
        rule_code: "LAND_USE_COMPATIBILITY",
        severity: "high",
        message: "Use 'industrial' is not allowed in zone C1.",
      },
    ],
    explanations: [
      {
        rule_code: "LAND_USE_COMPATIBILITY",
        outcome: "fail",
        message: "Use 'industrial' is not allowed in zone C1.",
      },
      {
        rule_code: "HEIGHT_MAX_BY_ZONE",
        outcome: "pass",
        message: "Height 20.0m is within the 25.0m limit for zone C1.",
      },
      {
        rule_code: "HERITAGE_OVERRIDE",
        outcome: "pass",
        message: "No heritage-protection flag is present in the MVP evidence bundle.",
      },
    ],
  },
  "PARIS-DEMO-0004": {
    building_id: "PARIS-DEMO-0004",
    address: "3 Boulevard de Belleville",
    arrondissement: 20,
    status: "unknown_insufficient_data",
    confidence: 0.2,
    rule_version: "2026-baseline",
    missing_evidence: ["height_m"],
    notes: "Evaluated with ruleset 2026-baseline.",
    violations: [
      {
        rule_code: "DATA_MINIMUM_REQUIRED",
        severity: "medium",
        message: "Missing required fields: height_m",
      },
    ],
    explanations: [
      {
        rule_code: "DATA_MINIMUM_REQUIRED",
        outcome: "fail",
        message: "Missing required fields: height_m",
      },
    ],
  },
  "PARIS-DEMO-0005": {
    building_id: "PARIS-DEMO-0005",
    address: "8 Place des Vosges",
    arrondissement: 4,
    status: "unknown_insufficient_data",
    confidence: 0.45,
    rule_version: "2026-baseline",
    missing_evidence: ["heritage_override_review"],
    notes: "Base zoning checks pass, but heritage review remains unresolved in the MVP.",
    violations: [
      {
        rule_code: "HERITAGE_OVERRIDE",
        severity: "medium",
        message: "Heritage-protected parcels need manual review in the MVP before a legal classification can be asserted.",
      },
    ],
    explanations: [
      {
        rule_code: "LAND_USE_COMPATIBILITY",
        outcome: "pass",
        message: "Use 'residential' is allowed in zone R1.",
      },
      {
        rule_code: "HEIGHT_MAX_BY_ZONE",
        outcome: "pass",
        message: "Height 17.5m is within the 18.0m limit for zone R1.",
      },
      {
        rule_code: "HERITAGE_OVERRIDE",
        outcome: "unknown",
        message: "Heritage-protected parcels need manual review in the MVP before a legal classification can be asserted.",
      },
    ],
  },
};

function toQueryString(params) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : "";
}

async function requestJson(path, params = {}, signal) {
  const response = await fetch(`${API_BASE_URL}${path}${toQueryString(params)}`, { signal });
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

function filterFallbackBuildings({ minArr, maxArr }) {
  return fallbackBuildings.filter(
    (building) => building.arrondissement >= minArr && building.arrondissement <= maxArr
  );
}

function buildFallbackStats(buildings) {
  const counts = {
    total_buildings: buildings.length,
    legal_today: 0,
    illegal_today: 0,
    unknown_insufficient_data: 0,
    non_conforming_tolerated: 0,
  };
  buildings.forEach((building) => {
    counts[building.status] += 1;
  });
  return counts;
}

export async function loadDashboard({ minArr, maxArr, signal }) {
  try {
    const [buildings, stats] = await Promise.all([
      requestJson("/v1/buildings", { min_arr: minArr, max_arr: maxArr }, signal),
      requestJson("/v1/stats", { min_arr: minArr, max_arr: maxArr }, signal),
    ]);
    return { buildings, stats, source: "api" };
  } catch (error) {
    if (signal?.aborted) {
      throw error;
    }
    const buildings = filterFallbackBuildings({ minArr, maxArr });
    return {
      buildings,
      stats: buildFallbackStats(buildings),
      source: "fallback",
      error: "Backend unavailable. Showing local demo data.",
    };
  }
}

export async function loadBuildingDetail(buildingId, signal) {
  try {
    return { detail: await requestJson(`/v1/buildings/${buildingId}`, {}, signal), source: "api" };
  } catch (error) {
    if (signal?.aborted) {
      throw error;
    }
    const detail = fallbackDetails[buildingId];
    if (!detail) {
      throw error;
    }
    return { detail, source: "fallback" };
  }
}
