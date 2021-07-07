ARG ALPINE_VERSION=${ALPINE_VERSION}
FROM alpine:${ALPINE_VERSION} as base

RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        alpine-sdk sudo bash-completion git vim curl shadow openssh-client

FROM scratch as user
COPY --from=base . .

ARG HOST_UID=${HOST_UID:-4000}
ARG HOST_USER=${HOST_USER:-nodummy}

RUN [ "${HOST_USER}" == "root" ] || \
    (adduser -h /home/${HOST_USER} -D -u ${HOST_UID} ${HOST_USER} \
    && chown -R "${HOST_UID}:${HOST_UID}" /home/${HOST_USER})

RUN for u in $(ls /home); do for g in disk lp floppy audio cdrom dialout video netdev games users; do addgroup $u $g; done;done

ARG PASSWORD=${PASSWORD}
RUN echo ${HOST_USER}:${PASSWORD} | chpasswd
RUN echo root:${PASSWORD} | chpasswd
RUN echo "${HOST_USER} ALL=(ALL) ALL" >> /etc/sudoers
RUN echo "root ALL=(ALL) ALL" >> /etc/sudoers
RUN echo "Set disable_coredump false" >> /etc/sudo.conf

USER ${HOST_USER}
WORKDIR /home/${HOST_USER}

RUN mkdir -p /home/${HOST_USER}/.ssh &&  chmod 700 /home/${HOST_USER}/.ssh
#COPY ${HOME}/.ssh/id_rsa /home/${HOST_USER}/.ssh/id_rsa
#RUN chmod 600 /home/${HOST_USER}/.ssh/id_rsa

