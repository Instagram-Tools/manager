FROM python:3.6.6-alpine3.8

ENV INSTALL_PATH=/app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual .build-deps \
  build-base postgresql-dev libffi-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk add openssh \
    && apk del .build-deps

COPY ./src .
COPY ./.aws /root/.aws

ENV PYTHONUNBUFFERED=0
ENV API_PORT=8000

EXPOSE 8765
CMD sh start.sh 8765