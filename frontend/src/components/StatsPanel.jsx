const STATUS_LABELS = {
  total_buildings: "Inventory in range",
  legal_today: "Legal today",
  illegal_today: "Illegal today",
  unknown_insufficient_data: "Unknown",
  non_conforming_tolerated: "Tolerated",
};

export function StatsPanel({ stats, visibleCount, activeStatusFilter, isLoading }) {
  return (
    <div className="panel stats">
      <div className="panel-header">
        <div>
          <h2>Dashboard</h2>
          <p>Counts come from the backend stats endpoint for the active arrondissement range.</p>
        </div>
      </div>
      <div className="stats-grid">
        {Object.entries(stats).map(([key, value]) => (
          <article key={key} className={`stat-card ${key}`}>
            <span>{STATUS_LABELS[key]}</span>
            <strong>{isLoading ? "..." : value}</strong>
          </article>
        ))}
      </div>
      <div className="stats-footnote">
        <p>Visible cards after status filter: {visibleCount}</p>
        <p>Status filter: {activeStatusFilter === "all" ? "All" : activeStatusFilter}</p>
      </div>
    </div>
  );
}
