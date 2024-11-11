FROM python:3.11-slim-bullseye AS builder

COPY requirements.txt .
RUN apt update && apt install --no-install-recommends -y \
    build-essential \
    libgeos-dev \
    libpq-dev
RUN python -m pip install uwsgi
RUN pip install --upgrade pip && pip install -r requirements.txt

# Start runtime image,
FROM python:3.11-slim-bullseye
RUN apt update && apt install --no-install-recommends -y \
    curl \
    libgdal28 \
    libgeos-c1v5 \
    libpq5 \
    media-types \
    netcat-openbsd

# Copy python build artifacts from builder image
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

WORKDIR /code
COPY . /code

ENV DJANGO_SETTINGS_MODULE=assessment.settings DJANGO_DEBUG=true STATIC_DIR=/static
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
