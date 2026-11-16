
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path
import csv

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression


app = FastAPI(title="CareBalance AI Alpha", version="0.1.0")

# Allow the local React frontend to access the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DATA = Path(__file__).resolve().parents[1] / "data" / "staffing.csv"


class ForecastRequest(BaseModel):
    available_staff: int = Field(default=9, ge=0, le=1000)
    hours_per_staff: float = Field(default=8, gt=0, le=24)
    department: str = Field(
        default="General Care",
        min_length=1,
        max_length=100,
    )


@lru_cache(maxsize=1)
def training_data():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    return [
        (
            int(r["day_index"]),
            float(r["patients"]),
            float(r["required_hours"]),
        )
        for r in rows
    ]


# Train once and reuse the regression model.
@lru_cache(maxsize=1)
def get_model():
    rows = training_data()

    if not rows:
        raise ValueError("Training data unavailable")

    x = np.array([[day, patients] for day, patients, _ in rows])
    y = np.array([hours for _, _, hours in rows])

    return LinearRegression().fit(x, y)


def predict_hours(day_index: int, patients: float) -> float:
    model = get_model()
    prediction = model.predict([[day_index, patients]])[0]
    return max(0.0, float(prediction))


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "synthetic demo"}


@app.post("/api/forecast")
def forecast(payload: ForecastRequest):
    rows = training_data()

    if not rows:
        raise HTTPException(
            status_code=503,
            detail="Training data unavailable",
        )

    capacity = payload.available_staff * payload.hours_per_staff
    today = date.today()
    output = []

    for offset in range(7):
        current_date = today + timedelta(days=offset)
        weekday = current_date.weekday()

        subset = [
            patients
            for day, patients, _ in rows
            if day == weekday
        ]

        if subset:
            patients = round(sum(subset) / len(subset))
        else:
            patients = round(
                sum(p for _, p, _ in rows) / len(rows)
            )

        required = round(predict_hours(weekday, patients), 1)

        utilization = (
            round(required / capacity * 100, 1)
            if capacity
            else None
        )

        if capacity == 0 or utilization >= 100:
            risk = "High"
        elif utilization >= 85:
            risk = "Moderate"
        else:
            risk = "Low"

        output.append({
            "date": current_date.isoformat(),
            "patients": patients,
            "required_hours": required,
            "capacity_hours": round(capacity, 1),
            "utilization_pct": utilization,
            "risk": risk,
        })

    return {
        "department": payload.department,
        "disclaimer": (
            "Educational demonstration using synthetic data. "
            "Not validated for real staffing or employee decisions."
        ),
        "method": (
            "Linear regression trained on synthetic patient volume "
            "and weekday observations. Risk thresholds are illustrative, "
            "not clinically validated."
        ),
        "forecast": output,
    }
