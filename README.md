
# CareBalance AI Alpha

CareBalance AI is an educational prototype that uses synthetic staffing data to generate seven day staffing demand forecasts and illustrative workload risk estimates for one department.

The application uses a linear regression model. No real patient or employee data is used. The workload risk indicator is not a validated burnout prediction.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- npm

## Run the backend

Open a terminal in the `backend` directory.

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

API documentation:

http://localhost:8000/docs

## Run the frontend

Open a second terminal in the `frontend` directory.

Install dependencies:

```bash
npm install
```

Start the application:

```bash
npm run dev
```

Open http://localhost:5173 and select **Generate forecast**.

## Testing and CI/CD

From the `backend` directory:

```bash
python -m pytest tests -q
```

From the `frontend` directory:

```bash
npm run build
```

GitHub Actions automatically runs backend tests and builds the frontend for each push and pull request.

The pipeline currently verifies testing and build success. Automated deployment is not configured.

## System Architecture

- Frontend: React and Vite
- Backend: FastAPI
- Input validation: Pydantic
- AI component: scikit learn linear regression
- Training data: Synthetic CSV observations
- API endpoints: POST `/api/forecast` and GET `/api/health`
- Forecast period: Seven days
- Department scope: General Care

The frontend sends staffing information to the backend API. The backend uses the trained regression model to estimate required staffing hours and calculate illustrative workload risk.

The regression model is cached to avoid unnecessary retraining during forecast requests.

## Security and Privacy

Authentication and user authorization are not implemented in the Alpha release.

The application must not be used with real patient, employee, or other sensitive information.

Only synthetic data is permitted during development and testing.

The backend restricts browser access through CORS configuration to approved local development origins. CORS is not a replacement for authentication.

Input validation is implemented using Pydantic.

Before any production deployment, authentication, authorization, data protection, and security testing must be implemented.

## Model Evaluation

The current model uses linear regression trained on synthetic staffing observations.

Model performance has not yet been validated against real historical staffing outcomes.

Future evaluation will compare forecast accuracy against a historical baseline using Mean Absolute Error (MAE).

MAE measures the average absolute difference between predicted and actual values.

The model should demonstrate measurable improvement over the baseline before being considered for further operational evaluation.

Workload risk thresholds are currently illustrative:

- Low: Below 85 percent utilization
- Moderate: 85 percent to below 100 percent utilization
- High: 100 percent utilization or greater, or no available staffing capacity

These thresholds have not been clinically validated and do not measure employee burnout.

## Known Limitations

1. The application uses synthetic data rather than real staffing records.
2. Authentication and authorization are not implemented.
3. PostgreSQL database integration is not included in the Alpha release.
4. The forecasting model has not undergone formal accuracy evaluation.
5. Workload risk thresholds are illustrative.
6. Automated testing does not yet cover the complete browser experience.
7. Automated deployment and production monitoring are not configured.
8. The application currently supports one department.

## Peer Review Findings

The Alpha implementation was reviewed for code readability, security, performance, integration compatibility, and documentation.

The reviewer recommended:

1. Caching the regression model to improve performance.
2. Separating forecasting, data processing, and API routes into smaller modules.
3. Documenting missing authentication and protecting sensitive information.
4. Expanding automated integration and error handling tests.
5. Documenting model evaluation criteria and technical debt priorities.

## Technical Debt Mitigation Plan

### Priority 1: Completed Alpha Improvements

- Cache the trained regression model to reduce repeated training.
- Add an automated CORS test to verify permitted frontend communication.
- Improve documentation of security limitations and synthetic data requirements.
- Document model evaluation criteria and current limitations.

### Priority 2: Next Development Phase

- Separate data processing, forecasting logic, and API routes into smaller Python modules.
- Expand automated tests to cover API errors and frontend integration.
- Evaluate forecasting accuracy using MAE and a historical baseline.
- Add additional validation and error handling.

### Priority 3: Future Development

- Implement authentication and authorization.
- Integrate PostgreSQL for persistent data storage.
- Add monitoring and automated deployment.
- Expand forecasting to additional departments.
- Improve the dashboard and reporting capabilities.

## Alpha Release Status

The Alpha release demonstrates:

- Working React and FastAPI integration
- Functional regression based staffing forecasts
- Seven day forecast results
- Illustrative workload risk indicators
- Automated backend tests
- Successful frontend build
- GitHub Actions CI checks
- Peer review feedback and documented improvement priorities

CareBalance AI remains an educational prototype and is not intended for real staffing, clinical, or employee decisions.
