const OUTCOME_LABELS = {
  pass: "Pass",
  fail: "Fail",
  unknown: "Unknown",
};

export function BuildingDetailPanel({ building, isLoading }) {
  return (
    <section className="panel detail-panel">
      <div className="panel-header">
        <div>
          <h2>Building detail</h2>
          <p>Violation and explanation traces come from the evaluated building detail endpoint.</p>
        </div>
      </div>
      {isLoading ? <div className="detail-placeholder">Loading building detail...</div> : null}
      {!isLoading && !building ? (
        <div className="detail-placeholder">Select a building to inspect its rule trace.</div>
      ) : null}
      {!isLoading && building ? (
        <div className="detail-content">
          <div className="detail-headline">
            <div>
              <p className="detail-address">{building.address}</p>
              <p className="detail-meta">
                {building.building_id} · {building.arrondissement}e arrondissement
              </p>
            </div>
            <span className={`status-pill status-${building.status}`}>{building.status}</span>
          </div>
          <div className="detail-facts">
            <div>
              <span>Confidence</span>
              <strong>{(building.confidence * 100).toFixed(0)}%</strong>
            </div>
            <div>
              <span>Rule version</span>
              <strong>{building.rule_version}</strong>
            </div>
          </div>
          <div className="trace-grid">
            <article>
              <h3>Violations</h3>
              {building.violations.length === 0 ? <p>No rule violations recorded.</p> : null}
              <ul className="trace-list">
                {building.violations.map((violation) => (
                  <li key={`${violation.rule_code}-${violation.message}`}>
                    <strong>{violation.rule_code}</strong>
                    <span>{violation.severity}</span>
                    <p>{violation.message}</p>
                  </li>
                ))}
              </ul>
            </article>
            <article>
              <h3>Explainability trace</h3>
              <ul className="trace-list">
                {building.explanations.map((explanation) => (
                  <li key={`${explanation.rule_code}-${explanation.message}`}>
                    <strong>{explanation.rule_code}</strong>
                    <span>{OUTCOME_LABELS[explanation.outcome] || explanation.outcome}</span>
                    <p>{explanation.message}</p>
                  </li>
                ))}
              </ul>
            </article>
          </div>
          <div className="detail-footnotes">
            <p>
              <strong>Missing evidence:</strong>{" "}
              {building.missing_evidence.length > 0
                ? building.missing_evidence.join(", ")
                : "None"}
            </p>
            <p>
              <strong>Notes:</strong> {building.notes || "No additional notes."}
            </p>
          </div>
        </div>
      ) : null}
    </section>
  );
}
