FROM python:3.6

ARG project_dir=/app/

WORKDIR $project_dir
ADD app/main.py $project_dir
RUN pip install flask

CMD ["python", "main.py"]