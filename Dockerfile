FROM python:3.11.3
LABEL maintainer="erik.agayan1@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR theatre_api_service/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
