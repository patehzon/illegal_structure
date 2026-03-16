import { MapPanel } from "./components/MapPanel";
import { StatsPanel } from "./components/StatsPanel";

export default function App() {
  return (
    <div className="layout">
      <header>
        <h1>Paris Building Legality — 2026</h1>
        <p>
          Street-level legality classification scaffold with explainable rule outputs.
        </p>
      </header>
      <main>
        <section>
          <MapPanel />
        </section>
        <aside>
          <StatsPanel />
        </aside>
      </main>
    </div>
  );
}
