FROM python:3.6
LABEL maintainer="sho"

ARG project_dir=/api/

WORKDIR $project_dir

COPY main.py $project_dir
COPY model.py $project_dir
COPY uwsgi.ini $project_dir
RUN pip install flask uWSGI requests redis sqlalchemy mysqlclient

ENV MYSQL_HOST=mysqld
ENV REDIS_HOST=redis

CMD ["uwsgi", "uwsgi.ini"]