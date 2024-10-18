FROM python:3.11.0-alpine

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Turns off an automatic check for pip updates each time
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN mkdir /src

COPY ../src /src

WORKDIR /src

RUN pip install --no-cache-dir -r requirements.txt

# This is unnecessary if you set command in the compose file
# ENTRYPOINT ["python3", "...", "...", "..."]
