#!/usr/bin/env bash
#
# download logobook locally for ease of processing
#

set -o errexit
set -o pipefail
set -o nounset

echo "INFO: logobook download starting at $(date -u +%Y-%m-%dT%H:%M:%SZ)"


SCRIPT_HOME="$( cd "$( dirname "$0" )" && pwd )"
LOGDIR=$(realpath "${SCRIPT_HOME}/../../tmp")
CACHEDIR=$(realpath "${SCRIPT_HOME}/../../cache")

if [ ! -d "${LOGDIR}" ]; then
	echo "INFO: creating log directory ${LOGDIR}"
	mkdir -p "${LOGDIR}"
fi

if [ ! -d "${CACHEDIR}" ]; then
	echo "INFO: creating cache directory ${CACHEDIR}"
	mkdir -p "${CACHEDIR}"
fi

wget \
	"--directory-prefix=${CACHEDIR}" \
	"--exclude-directories=wp-json,icons,wp-content/themes,letter,country,nature,shape,design-company,designer,business" \
	--continue \
	--recursive \
	http://www.logobook.com/ \
	| tee -a "${LOGDIR}/logobook.log"

echo "INFO: logobook download complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

