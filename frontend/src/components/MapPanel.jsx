const STATUS_LABELS = {
  legal_today: "Legal today",
  illegal_today: "Illegal today",
  unknown_insufficient_data: "Unknown",
  non_conforming_tolerated: "Tolerated",
};

export function MapPanel({
  buildings,
  isLoading,
  selectedBuildingId,
  onSelectBuilding,
}) {
  return (
    <div className="panel map">
      <div className="panel-header">
        <div>
          <h2>Inventory view</h2>
          <p>
            Geometry is still pending, so the MVP uses a navigable building board grouped
            by arrondissement and legality status.
          </p>
        </div>
        <span className="count-badge">{buildings.length} visible</span>
      </div>
      {isLoading ? <div className="map-placeholder">Loading building inventory...</div> : null}
      {!isLoading && buildings.length === 0 ? (
        <div className="map-placeholder">No buildings match the current filters.</div>
      ) : null}
      {!isLoading && buildings.length > 0 ? (
        <div className="building-grid">
          {buildings.map((building) => (
            <button
              key={building.building_id}
              className={`building-card status-${building.status} ${
                selectedBuildingId === building.building_id ? "selected" : ""
              }`}
              onClick={() => onSelectBuilding(building.building_id)}
              type="button"
            >
              <span className="arr-chip">{building.arrondissement}e</span>
              <strong>{building.address}</strong>
              <span className="status-label">{STATUS_LABELS[building.status]}</span>
              <span className="confidence-copy">
                Confidence {(building.confidence * 100).toFixed(0)}%
              </span>
              <span className="rule-copy">{building.rule_version}</span>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
