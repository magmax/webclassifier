FROM python:3.10-bullseye

ADD requirements.txt .
RUN apt-get update -y \
  && apt-get install -y \
    bogofilter \
    lynx \
  && apt-get clean -y \
  && pip install -r requirements.txt
ADD webclassifier /app
WORKDIR /app

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
