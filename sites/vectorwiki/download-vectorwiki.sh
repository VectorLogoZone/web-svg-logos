#!/bin/bash
#
# download vectorwiki's sitemap.xml
#

set -o errexit
set -o pipefail
set -o nounset

wget https://vectorwiki.com/sitemap.xml
