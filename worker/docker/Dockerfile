FROM python:3.7.7-slim-buster

# set up non-root user
ENV APPUSER_HOME=/home/appuser
ENV WORKER_HOME=/home/appuser/worker
ENV APP_HOME=/home/appuser/worker/app

RUN useradd --create-home appuser && \
mkdir -p $WORKER_HOME && \
mkdir -p $APP_HOME

WORKDIR $WORKER_HOME

# worker requirements, tasks and db models to worker home
COPY ./worker/requirements.txt $WORKER_HOME
COPY ./worker/tasks.py $WORKER_HOME
COPY ./app/models.py $APP_HOME
ADD ./worker/app $APP_HOME

# extra packages from extra-packages.sh
COPY ./worker/extra-packages.sh $WORKER_HOME
RUN chmod +x $WORKER_HOME/extra-packages.sh && $WORKER_HOME/extra-packages.sh

# upgrade pip, container and install requirements
RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements.txt

# set worker home permission
RUN chown -R appuser:appuser $APPUSER_HOME
USER appuser
