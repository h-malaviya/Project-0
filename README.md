Project-0

A small, professional FastAPI-style service for working with app models, routes, and services.

Why this exists
- Minimal API scaffold with database, models, schemas, and service layers for quick prototyping.

Quick start

- Create and activate a virtual environment:

  ```bash
  python -m venv .venv
  .venv\Scripts\activate    # Windows
  source .venv/bin/activate  # macOS / Linux
  ```

- Install dependencies (use `pip`):

  ```bash
  pip install -r requirements.txt
  ```

- Run the app (example using `uvicorn`):

  ```bash
  uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
  ```

Note about `uv` vs `pip`

- `uv` is not a package installer. If you typed `uv` when trying to install, use `pip` instead.
- If you meant to start the server and used `uv` as shorthand, use `uvicorn` (or create an alias).

  Verify installed packages:

  ```bash
  pip list
  ```

  PowerShell alias example (optional):

  ```powershell
  Set-Alias uv uvicorn
  ```

Where to look
- App entry: [app/main.py](app/main.py)
- Routes: [app/routes.py](app/routes.py)
- Models & schemas: [app/models.py](app/models.py), [app/schemas.py](app/schemas.py)
- Database helpers: [app/database.py](app/database.py), [app/database2.py](app/database2.py)
- Business logic/services: [app/service.py](app/service.py), [app/service2.py](app/service2.py)

Notes
- Keep secrets and DB credentials out of the repository; use environment variables.
- This README is intentionally short — tell me if you want a longer developer guide or API examples.
