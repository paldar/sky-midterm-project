#!/bin/bash
set -eux

docker run -d -p 15000:7689 --rm turkunlp/turku-neural-parser:latest-fi-en-sv-cpu server fi_tdt parse_plaintext
