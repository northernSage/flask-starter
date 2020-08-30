FROM nginx:1.17.9

# set up env values
ENV USER_HOME=/home/appuser
ENV APP_HOME=/home/appuser/web
ENV SSL_CERT=/home/appuser/cert
ENV STATIC_FOLDER=/home/appuser/web/static-files

# install certbot
RUN apt-get update && \
apt-get install -y certbot python-certbot-nginx

# set up non-root user
RUN useradd --create-home appuser && mkdir -p $APP_HOME $SSL_CERT $STATIC_FOLDER

# copy custom configuration files over to container
RUN rm /etc/nginx/*.conf && rm /etc/nginx/conf.d/*.conf
COPY nginx.conf /etc/nginx/
COPY default-custom.conf /etc/nginx/conf.d/
ADD cert $SSL_CERT
