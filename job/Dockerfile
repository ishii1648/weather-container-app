FROM python:3.6
LABEL maintainer="sho"

ARG project_dir=/job/

WORKDIR $project_dir

ADD setup_db.py $project_dir
RUN pip install sqlalchemy requests mysqlclient

ENV MYSQL_HOST=mysqld

CMD ["python", "setup_db.py"]