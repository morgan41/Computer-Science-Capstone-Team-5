# CareBalance AI Alpha

Educational prototype for one department. The app uses synthetic staffing observations to train a simple linear regression model and returns seven days of illustrative demand and workload risk estimates. No real patient or employee data is used. The risk indicator is not a validated burnout prediction.

## Requirements

Python 3.11 or newer, Node.js 20 or newer, and npm.

## Run the backend

Open a terminal in the `backend` directory:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

The API documentation is at http://localhost:8000/docs.

## Run the frontend

Open a second terminal in the `frontend` directory:

```bash
npm install
npm run dev
```

Open http://localhost:5173 and select **Generate forecast**.

## Test

From the `backend` directory with the virtual environment active:

```bash
python -m pytest tests -q
```

From the `frontend` directory:

```bash
npm run build
```

The GitHub Actions workflow runs both checks for each push and pull request. A green check in GitHub is required before claiming the pipeline passed.

## Design and limitations

* Frontend: React and Vite
* Backend: FastAPI and Pydantic validation
* AI: scikit learn linear regression trained on synthetic observations
* Interface: POST `/api/forecast`, GET `/api/health`
* Data: CSV only, no persistent database in this Alpha
* Risk: thresholds at 85 percent and 100 percent utilization are illustrative
* Scope: one department, seven day forecast

The current model is not evaluated against real historical staffing outcomes. It does not measure employee burnout. Planned improvements include PostgreSQL persistence, model evaluation against a baseline, authentication, monitoring, and a richer interface.

## Suggested review checklist

Ask a teammate to review `backend/app/main.py` and the API contract for readability, input validation, potential security risks, performance, integration compatibility, and documentation. Capture the review comments and resulting commits before writing the individual Refinement Report. Do not claim a review occurred until it actually happens.
