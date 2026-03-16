export function MapPanel() {
  return (
    <div className="panel map">
      <h2>Interactive map</h2>
      <p>
        TODO: render building geometries and color by legality status
        (`legal_today`, `illegal_today`, `unknown_insufficient_data`,
        `non_conforming_tolerated`).
      </p>
      <div className="map-placeholder">Map canvas placeholder</div>
    </div>
  );
}
