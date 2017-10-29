#!/bin/sh

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

source venv/bin/activate

export FLASK_APP=server.py
export FLASK_DEBUG=1

flask run
