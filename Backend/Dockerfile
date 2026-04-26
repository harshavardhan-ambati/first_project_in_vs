FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
