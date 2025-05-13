FROM python:3.13.2
WORKDIR /app
RUN pip install --no-cache-dir fastf1
COPY api.py .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
