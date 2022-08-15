######################## BASE PYTHON IMAGE ########################
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

WORKDIR /src
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements/dev.txt


EXPOSE 80

ENTRYPOINT sh ./entrypoint.dev.sh
