FROM python:3.6
LABEL maintainer="sho"

ARG project_dir=/api/

WORKDIR $project_dir

ADD main.py $project_dir
RUN pip install flask uWSGI requests redis

CMD ["uwsgi", "uwsgi.ini"]