import { useDeferredValue, useEffect, useState } from "react";

import { loadBuildingDetail, loadDashboard } from "./api";
import { BuildingDetailPanel } from "./components/BuildingDetailPanel";
import { FilterBar } from "./components/FilterBar";
import { MapPanel } from "./components/MapPanel";
import { StatsPanel } from "./components/StatsPanel";

const STATUS_OPTIONS = [
  { value: "all", label: "All statuses" },
  { value: "legal_today", label: "Legal today" },
  { value: "illegal_today", label: "Illegal today" },
  { value: "unknown_insufficient_data", label: "Unknown" },
  { value: "non_conforming_tolerated", label: "Tolerated" },
];

export default function App() {
  const [minArr, setMinArr] = useState(1);
  const [maxArr, setMaxArr] = useState(20);
  const [statusFilter, setStatusFilter] = useState("all");
  const [dashboard, setDashboard] = useState({
    buildings: [],
    stats: {
      total_buildings: 0,
      legal_today: 0,
      illegal_today: 0,
      unknown_insufficient_data: 0,
      non_conforming_tolerated: 0,
    },
    source: "api",
    error: "",
  });
  const [isDashboardLoading, setIsDashboardLoading] = useState(true);
  const [selectedBuildingId, setSelectedBuildingId] = useState("");
  const [selectedBuilding, setSelectedBuilding] = useState(null);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const deferredStatusFilter = useDeferredValue(statusFilter);

  useEffect(() => {
    const controller = new AbortController();
    setIsDashboardLoading(true);

    loadDashboard({ minArr, maxArr, signal: controller.signal })
      .then((payload) => {
        setDashboard(payload);
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setIsDashboardLoading(false);
        }
      });

    return () => controller.abort();
  }, [minArr, maxArr]);

  const visibleBuildings = dashboard.buildings.filter((building) => {
    if (deferredStatusFilter === "all") {
      return true;
    }
    return building.status === deferredStatusFilter;
  });

  useEffect(() => {
    if (visibleBuildings.length === 0) {
      setSelectedBuildingId("");
      setSelectedBuilding(null);
      return;
    }
    const hasSelection = visibleBuildings.some(
      (building) => building.building_id === selectedBuildingId
    );
    if (!hasSelection) {
      setSelectedBuildingId(visibleBuildings[0].building_id);
    }
  }, [selectedBuildingId, visibleBuildings]);

  useEffect(() => {
    if (!selectedBuildingId) {
      return;
    }
    const controller = new AbortController();
    setIsDetailLoading(true);

    loadBuildingDetail(selectedBuildingId, controller.signal)
      .then((payload) => {
        setSelectedBuilding(payload.detail);
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setIsDetailLoading(false);
        }
      });

    return () => controller.abort();
  }, [selectedBuildingId]);

  return (
    <div className="layout">
      <header className="hero panel">
        <div>
          <p className="eyebrow">Illegal Structure — Paris Building Legality (2026)</p>
          <h1>Street-level legality signals for the current MVP inventory.</h1>
          <p className="hero-copy">
            The UI now reads live backend evaluations when available and falls back to
            the local demo inventory when the API is offline.
          </p>
        </div>
        <div className="hero-status">
          <span className={`source-pill source-${dashboard.source}`}>
            Source: {dashboard.source === "api" ? "backend API" : "local fallback"}
          </span>
          <p>Rule version: 2026-baseline</p>
        </div>
      </header>
      <FilterBar
        minArr={minArr}
        maxArr={maxArr}
        statusFilter={statusFilter}
        statusOptions={STATUS_OPTIONS}
        onMinArrChange={setMinArr}
        onMaxArrChange={setMaxArr}
        onStatusFilterChange={setStatusFilter}
      />
      {dashboard.error ? <p className="banner warning">{dashboard.error}</p> : null}
      <main className="dashboard-grid">
        <section className="primary-column">
          <MapPanel
            buildings={visibleBuildings}
            isLoading={isDashboardLoading}
            selectedBuildingId={selectedBuildingId}
            onSelectBuilding={setSelectedBuildingId}
          />
          <BuildingDetailPanel
            building={selectedBuilding}
            isLoading={isDetailLoading}
          />
        </section>
        <aside className="secondary-column">
          <StatsPanel
            stats={dashboard.stats}
            visibleCount={visibleBuildings.length}
            activeStatusFilter={statusFilter}
            isLoading={isDashboardLoading}
          />
        </aside>
      </main>
    </div>
  );
}
