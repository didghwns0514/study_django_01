#!/bin/sh
cd ..

brew install git-lfs

git lfs install
git lfs track "*.pdf"
git lfs track "*.COD"

git config alias.commit-test '!pre-commit run --all-files && git commit'
pre-commit autoupdate
pre-commit install
pre-commit run --all-files
