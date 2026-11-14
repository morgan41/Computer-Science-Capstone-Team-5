
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [staff, setStaff] = useState(9);
  const [hours, setHours] = useState(8);
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function run(e) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API}/api/forecast`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          department: 'General Care',
          available_staff: Number(staff),
          hours_per_staff: Number(hours)
        })
      });

      if (!response.ok) {
        throw new Error(
          `Forecast request failed (${response.status})`
        );
      }

      setData(await response.json());
    } catch (err) {
      setData(null);
      setError(
        `${err.message}. Check that the backend is running.`
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <header>
        <div className="eyebrow">
          ALPHA RELEASE · SYNTHETIC DEMO
        </div>
        <h1>CareBalance AI</h1>
        <p>
          Seven day staffing demand forecast and
          illustrative workload risk
        </p>
      </header>

      <section className="panel">
        <h2>Staffing scenario</h2>

        <form onSubmit={run}>
          <label>
            Available staff
            <input
              type="number"
              min="0"
              max="1000"
              step="1"
              required
              value={staff}
              onChange={e => setStaff(e.target.value)}
            />
          </label>

          <label>
            Hours per staff member
            <input
              type="number"
              min="0.1"
              max="24"
              step="any"
              required
              value={hours}
              onChange={e => setHours(e.target.value)}
            />
          </label>

          <button disabled={loading}>
            {loading ? 'Calculating…' : 'Generate forecast'}
          </button>
        </form>
      </section>

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {data && (
        <section className="panel">
          <h2>General Care · Next seven days</h2>
          <p className="note">{data.disclaimer}</p>

          <div className="tablewrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Patients</th>
                  <th>Required hours</th>
                  <th>Capacity hours</th>
                  <th>Utilization</th>
                  <th>Risk</th>
                </tr>
              </thead>

              <tbody>
                {data.forecast.map(r => (
                  <tr key={r.date}>
                    <td>{r.date}</td>
                    <td>{r.patients}</td>
                    <td>{r.required_hours}</td>
                    <td>{r.capacity_hours}</td>
                    <td>
                      {r.utilization_pct === null
                        ? 'N/A'
                        : `${r.utilization_pct}%`}
                    </td>
                    <td>
                      <span
                        className={`risk ${r.risk.toLowerCase()}`}
                      >
                        {r.risk}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <p className="note">{data.method}</p>
        </section>
      )}

      <footer>
        No real patient or employee data is collected or
        stored. This prototype is not a decision support tool.
      </footer>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);

