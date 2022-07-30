#!/bin/bash
#
# run locally for dev
#

set -o errexit
set -o pipefail
set -o nounset

wget \
	--append-output=wget.log \
	--continue \
	--no-parent \
	--recursive \
    https://iconape.com/
	