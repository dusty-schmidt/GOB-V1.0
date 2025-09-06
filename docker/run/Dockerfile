# Use the pre-built base image for GOB
# FROM gob-base:local
FROM gob-base:local

# Check if the argument is provided, else throw an error
ARG BRANCH
RUN if [ -z "$BRANCH" ]; then echo "ERROR: BRANCH is not set!" >&2; exit 1; fi
ENV BRANCH=$BRANCH

# Copy filesystem files to root
COPY ./fs/ /

# Normalize line endings for shell scripts copied into the image
RUN find /ins -type f -name "*.sh" -exec sed -i 's/\r$//' {} + && \
    find /exe -type f -name "*.sh" -exec sed -i 's/\r$//' {} +

# pre installation steps
RUN bash /ins/pre_install.sh $BRANCH

# install GOB
RUN bash /ins/install_gob.sh $BRANCH

# install additional software
RUN bash /ins/install_additional.sh $BRANCH

# cleanup repo and install GOB without caching, this speeds up builds
ARG CACHE_DATE=none
RUN echo "cache buster $CACHE_DATE" && bash /ins/install_gob2.sh $BRANCH

# post installation steps
RUN bash /ins/post_install.sh $BRANCH

# Expose ports
EXPOSE 22 80 9000-9009

RUN chmod +x /exe/initialize.sh /exe/run_gob.sh /exe/run_searxng.sh /exe/run_tunnel_api.sh

# initialize runtime and switch to supervisord
CMD ["/exe/initialize.sh", "$BRANCH"]
