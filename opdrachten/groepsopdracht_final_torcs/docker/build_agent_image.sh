#!/usr/bin/env bash

(cd ..; docker build . -t agent:22234 -f docker/Dockerfile)