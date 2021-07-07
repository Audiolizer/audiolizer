# If you see pwd_unknown showing up, this is why. Re-calibrate your system.
PWD ?= pwd_unknown

# PROJECT_NAME defaults to name of the current directory.
# should not to be changed if you follow GitOps operating procedures.
PROJECT_NAME = $(notdir $(PWD))

# Note. If you change this, you also need to update docker-compose.yml.
# only useful in a setting with multiple services/ makefiles.
SERVICE_TARGET := alpine

ifeq ($(user),)
# USER retrieved from env, UID from shell.
HOST_USER ?= $(strip $(if $(USER),$(USER),nodummy))
HOST_UID  ?=  $(strip $(if $(shell id -u),$(shell id -u),4000))
else
# allow override by adding user= and/ or uid=  (lowercase!).
# uid= defaults to 0 if user= set (i.e. root).
HOST_USER = $(user)
HOST_UID = $(strip $(if $(uid),$(uid),0))
endif

ifeq ($(alpine),)
ALPINE_VERSION := 3.11.10
else
ALPINE_VERSION := $(alpine)
endif
export ALPINE_VERSION

ifeq ($(no-cache),true)
NO_CACHE := --no-cache
else
NO_CACHE :=	
endif
export NO_CACHE

ifeq ($(verbose),true)
VERBOSE := --verbose
else
VERBOSE :=	
endif
export VERBOSE

ifneq ($(passwd),)
PASSWORD := $(passwd)
else
PASSWORD := changeme
endif
export PASSWORD


THIS_FILE := $(lastword $(MAKEFILE_LIST))

ifeq ($(cmd),)
CMD_ARGUMENTS := 	
else
CMD_ARGUMENTS := $(cmd)
endif
export CMD_ARGUMENTS

# export such that its passed to shell functions for Docker to pick up.
export PROJECT_NAME
export HOST_USER
export HOST_UID

DOCKER_MAC:=$(shell find /Applications -name Docker.app)
export DOCKER_MAC

# all our targets are phony (no files to check).
.PHONY: alpine shell help alpine-build alpine-rebuild build rebuild alpine-test service login  clean

# suppress makes own output
#.SILENT:

.PHONY: report
report:
	@echo ''
	@echo '	[ARGUMENTS]	'
	@echo '      args:'
	@echo '        - PWD=${PWD}'
	@echo '        - Makefile=${Makefile}'
	@echo '        - THIS_FILE=${THIS_FILE}'
	@echo '        - TIME=${TIME}'
	@echo '        - HOST_USER=${HOST_USER}'
	@echo '        - HOST_UID=${HOST_UID}'
	@echo '        - SERVICE_TARGET=${SERVICE_TARGET}'
	@echo '        - ALPINE_VERSION=${ALPINE_VERSION}'
	@echo '        - PROJECT_NAME=${PROJECT_NAME}'
	@echo '        - GIT_USER_NAME=${GIT_USER_NAME}'
	@echo '        - GIT_USER_EMAIL=${GIT_USER_EMAIL}'
	@echo '        - GIT_SERVER=${GIT_SERVER}'
	@echo '        - GIT_PROFILE=${GIT_PROFILE}'
	@echo '        - GIT_REPO_ORIGIN=${GIT_REPO_ORIGIN}'
	@echo '        - GIT_REPO_NAME=${GIT_REPO_NAME}'
	@echo '        - GIT_REPO_PATH=${GIT_REPO_PATH}'
	@echo '        - DOCKERFILE=${DOCKERFILE}'
	@echo '        - DOCKERFILE_BODY=${DOCKERFILE_BODY}'
	@echo '        - DOCKERFILE_PATH=${DOCKERFILE_PATH}'
	@echo '        - NO_CACHE=${NO_CACHE}'
	@echo '        - VERBOSE=${VERBOSE}'
	@echo '        - PUBLIC_PORT=${PUBLIC_PORT}'
	@echo '        - PASSWORD=${PASSWORD}'
	@echo '        - CMD_ARGUMENTS=${CMD_ARGUMENTS}'
	@echo ''

.PHONY: start-docker-mac
start-docker-mac:
	bash -c "${DOCKER_MAC}/Contents/MacOS/./Docker"

.PHONY: alpine
alpine:
ifeq ($(CMD_ARGUMENTS),)
	docker-compose $(VERBOSE) -p $(PROJECT_NAME)_$(HOST_UID) run --rm ${SERVICE_TARGET} sh
else
	docker-compose $(VERBOSE) -p $(PROJECT_NAME)_$(HOST_UID) run --rm $(SERVICE_TARGET) sh -c "$(CMD_ARGUMENTS)"
endif

.PHONY:shell
shell: alpine

# Regular Makefile part for buildpypi itself
.PHONY: help
help:
	@echo ''
	@echo 'Usage: make [TARGET] [EXTRA_ARGUMENTS]'
	@echo 'Targets:'
	@echo '  service   	run as service --container-- for current user: $(HOST_USER)(uid=$(HOST_UID))'
	@echo '  login   	run as service and login --container-- for current user: $(HOST_USER)(uid=$(HOST_UID))'
	@echo '  clean    	remove docker --image-- for current user: $(HOST_USER)(uid=$(HOST_UID))'
	@echo '  shell    	run docker --container-- for current user: $(HOST_USER)(uid=$(HOST_UID))'
	@echo ''
	@echo 'Extra arguments:'
	@echo 'cmd=:	make cmd="whoami"'
	@echo '# user= and uid= allows to override current user. Might require additional privileges.'
	@echo 'user=:	make shell user=root (no need to set uid=0)'
	@echo 'uid=:	make shell user=dummy uid=4000 (defaults to 0 if user= set)'

alpine-build:
	# only build the container. Note, docker does this also if you apply other targets.
	docker-compose build alpine

alpine-rebuild:
	# force a rebuild by passing --no-cache
	docker-compose build $(NO_CACHE) $(VERBOSE) ${SERVICE_TARGET}

alpine-test:
	docker-compose -p $(PROJECT_NAME)_$(HOST_UID) run --rm ${SERVICE_TARGET} sh -c '\
		echo "I am `whoami`. My uid is `id -u`." && /bin/bash -c "curl -fsSL https://raw.githubusercontent.com/randymcmillan/docker.shell/master/whatami"' \
	&& echo success

service:
	# run as a (background) service
	docker-compose -p $(PROJECT_NAME)_$(HOST_UID) up -d $(SERVICE_TARGET)

login: service
	# run as a service and attach to it
	docker exec -it $(PROJECT_NAME)_$(HOST_UID) sh

build: alpine-build

rebuild: alpine-rebuild

link:

	@bash -c '$(pwd) install -v docker-compose.yml ${HOME}/docker-compose.yml && install -v alpine ${HOME}/alpine && install -v GNUmakefile ${HOME}/GNUmakefile && install -v .dockerignore ${HOME}/.dockerignore'

clean:
	# remove created images
	@docker-compose -p $(PROJECT_NAME)_$(HOST_UID) down --remove-orphans --rmi all 2>/dev/null \
	&& echo 'Image(s) for "$(PROJECT_NAME):$(HOST_USER)" removed.' \
	|| echo 'Image(s) for "$(PROJECT_NAME):$(HOST_USER)" already removed.'


