# backend/app.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from decimal import Decimal, InvalidOperation
from fastapi.middleware.cors import CORSMiddleware

def parse_number(s: str) -> Decimal:
    s = s.strip()
    if s == "":
        raise ValueError("Empty input")
    try:
        return Decimal(s)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid numeric value: {s}") from exc

def calculate(a: Decimal, b: Decimal, op: str) -> Decimal:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b
    if op == "%":
        if b == 0:
            raise ZeroDivisionError("Modulo by zero")
        return a % b
    if op == "**" or op.lower() == "pow":
        return a ** b
    raise ValueError(f"Unsupported operator: {op}")

app = FastAPI(title="Calculator Demo - API only")

# For demo: allow your GitHub Pages origin specifically.
# Replace the origin below with your GH Pages URL when deployed:
# e.g. "https://<your-github-username>.github.io"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Change to your GH Pages origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/calc")
async def api_calc(a: str = Form(...), b: str = Form(...), op: str = Form(...)):
    try:
        da = parse_number(a)
        db = parse_number(b)
        res = calculate(da, db, op)
        return JSONResponse({"ok": True, "result": format(res.normalize(), "f")})
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except ZeroDivisionError as zde:
        raise HTTPException(status_code=400, detail=str(zde))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
