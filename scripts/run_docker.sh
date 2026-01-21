#!/usr/bin/env bash

set -e

docker run --env-file .env --restart unless-stopped -p 8050:8050 --detach --name wbui weather_bikes_ui
