FROM python:3.6
LABEL maintainer="sho"

ARG project_dir=/app/

WORKDIR $project_dir

ADD app/main.py $project_dir
RUN pip install flask uWSGI requests redis

CMD ["uwsgi", "uwsgi.ini"]