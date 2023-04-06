# syntax = docker/dockerfile:1.2
FROM cassandra:3.11.14
LABEL maintainer="apt-decoder project <matmccann@gmail.com>"

WORKDIR /
ENV DEBIAN_FRONTEND noninteractive
ARG DB_USER
ARG DB_PWD

# Copy files for install.sh
COPY apt /start/apt
COPY run /start/run

# Change permissions for script usage
RUN chmod 755 /start/*
RUN chmod +x /start -R
# Base apt installs (uses caching from buildx)
RUN --mount=type=cache,target=/var/cache/apt apt-get update -yqq --fix-missing && \
    apt-get install -yqq --no-install-recommends \
    $(cat /start/apt/general.apt)

# increase linux kernal maximum memory size for cassandra (who is such a hog)
CMD sysctl -w vm.max_map_count=1048575

# Health check on docker container to ensure that cqlsh (cassandra shell) is functional and can connect to DB
HEALTHCHECK CMD cqlsh -u $DB_USER -p $DB_PWD -e describe keyspaces
EXPOSE 7000 7001 7199 9042 9160
# Container config for `docker run` or `docker-compose .....`
ENTRYPOINT ["/start/run/entrypoint-wrap.sh", "-s", "/start/run/schema_decoder.cql"]
#CMD "bash"