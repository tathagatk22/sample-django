FROM centos:7

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
RUN set -ex \
    && yum install -y --setopt=tsflags=nodocs --setopt=skip_missing_names_on_install=False epel-release yum-utils unixODBC unixODBC-devel  \
    && BUILD_DEPS=" \
        gcc \
        gcc-c++ \
        python-devel \
        kernel-devel \
        make \
        python-pip \
    " \
    && yum update -y && yum install -y --setopt=tsflags=nodocs --setopt=skip_missing_names_on_install=False $BUILD_DEPS

# Copy in your requirements file
COPY requirements.txt /requirements.txt

# Setting virtual env path
ENV VIRTUAL_ENV=/venv

# Install requirements for the django project
RUN pip install --upgrade pip \
    && pip install virtualenv \
    && virtualenv $VIRTUAL_ENV \
    && $VIRTUAL_ENV/bin/pip install -U pip \
    && $VIRTUAL_ENV/bin/pip install --no-cache-dir -r /requirements.txt

# Removing unwanted dependencies
RUN set -ex \
    && BUILD_DEPS=" \
        gcc \
        gcc-c++ \
        python-devel \
        kernel-devel \
        make \
        python-pip \
    " \
    && yum remove -y $BUILD_DEPS

# Copy your application code to the container and configuration files
RUN mkdir -p /usr/src/app/sample-django/
WORKDIR /usr/src/app/sample-django/
COPY . /usr/src/app/sample-django/

# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=django_sample_project.settings

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL='' $VIRTUAL_ENV/bin/python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=/usr/src/app/sample-django/django_sample_project/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_VIRTUALENV=$VIRTUAL_ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# To run any sub-process from virtualenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# makemigrations will be performed
RUN $VIRTUAL_ENV/bin/python manage.py makemigrations

# migrate will be performed
RUN $VIRTUAL_ENV/bin/python manage.py migrate

# Creating random users
RUN $VIRTUAL_ENV/bin/python manage.py create_users 10

# Start uWSGI
CMD ["uwsgi", "--show-config"]
