# Top section copied from http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c
.DEFAULT_GOAL := default
.DELETE_ON_ERROR:
.SUFFIXES:

# CONCAT COMMANDS
circlei-cmd := circleci config process .circleci/config.yml > .circleci/config_v1.yml && \
				sleep 2 && \
				circleci local execute -c .circleci/config_v1.yml

circleci-local:
	@printf "Running circleci in DIR: $(PWD) \n"
	${circlei-cmd}
