# Runs Member 2's unit/integration tests; does not claim the full team app is deployed.
FROM python:3.12-slim
WORKDIR /app
COPY contact_management/ ./contact_management/
COPY database/ ./database/
COPY tests/ ./tests/
COPY demo_member2.py ./
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
