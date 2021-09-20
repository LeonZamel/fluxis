#!/bin/bash
PYTHONPATH=PYTHONPATH:$PWD/packages celery --workdir ./packages/fluxis_api -A fluxis_api worker --loglevel=info
