#!/bin/bash
#
# download logowine's sitemap.xml
#

set -o errexit
set -o pipefail
set -o nounset

wget https://www.logo.wine/sitemap.xml
