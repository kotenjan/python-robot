ARG VARIANT="3.8"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python2

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY .devcontainer/builder/* /tmp/
RUN python2 /tmp/get-pip2.py
RUN pip2 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements-python2.txt
RUN python3 /tmp/get-pip3.py
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements-python3.txt

RUN tar -xf /tmp/python-sdk.tar.gz \
    && mv pynaoqi* /usr/local/bin/python-sdk

ENV PYTHONPATH=${PYTHONPATH}:/usr/local/bin/python-sdk/lib/python2.7/site-packages
ENV QI_SDK_PREFIX=/usr/local/bin/python-sdk

