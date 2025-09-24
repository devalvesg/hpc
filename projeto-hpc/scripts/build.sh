#!/usr/bin/env bash
set -e

# Ambiente local ou SD
pip install -r env/requirements.txt || true

echo "Build concluído"
