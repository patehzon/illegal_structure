export function FilterBar({
  minArr,
  maxArr,
  statusFilter,
  statusOptions,
  onMinArrChange,
  onMaxArrChange,
  onStatusFilterChange,
}) {
  return (
    <section className="panel controls">
      <div className="panel-header">
        <div>
          <h2>Filters</h2>
          <p>Control the arrondissement range returned by the API and refine the visible status set.</p>
        </div>
      </div>
      <div className="controls-grid">
        <label>
          <span>Min arrondissement</span>
          <input
            type="number"
            min="1"
            max="20"
            value={minArr}
            onChange={(event) => onMinArrChange(Number(event.target.value))}
          />
        </label>
        <label>
          <span>Max arrondissement</span>
          <input
            type="number"
            min="1"
            max="20"
            value={maxArr}
            onChange={(event) => onMaxArrChange(Number(event.target.value))}
          />
        </label>
        <label>
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) => onStatusFilterChange(event.target.value)}
          >
            {statusOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
      </div>
    </section>
  );
}
