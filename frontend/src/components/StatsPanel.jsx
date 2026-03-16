const demoStats = {
  total_buildings: 0,
  legal_today: 0,
  illegal_today: 0,
  unknown_insufficient_data: 0,
  non_conforming_tolerated: 0,
};

export function StatsPanel() {
  return (
    <div className="panel stats">
      <h2>Dashboard</h2>
      <ul>
        {Object.entries(demoStats).map(([k, v]) => (
          <li key={k}>
            <strong>{k}</strong>: {v}
          </li>
        ))}
      </ul>
      <p>TODO: add arrondissement filters and violation breakdown charts.</p>
    </div>
  );
}
