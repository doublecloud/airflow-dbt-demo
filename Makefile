MAKEFLAGS    += -s --always-make -C
SHELL        := bash
.SHELLFLAGS  := -Eeuo pipefail -c

MAJOR_VERSION ?= 1

.PHONY: version
version:
	printf "%s.%s-build-%s" "${MAJOR_VERSION}" "$$(git rev-list --count HEAD)" "$$(git rev-parse --short HEAD)"