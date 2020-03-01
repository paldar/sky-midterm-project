#!/bin/bash

curl $(echo $1 | sed "s:Duration\/300:Duration\/7200:g") -o $2
  # sed '/^[0-9].*/d' |\
  # tr -d '\n' |\
  # sed 's/\.\.\././g' |\
  # sed 's/\([\.?!]\)[-) ]*\([ÖÅÄA-Z]\)/\1\n\2/g' |\
  # sed 's/\.)/.)\n/g' |\
  # sed 's/\s?-\s?\([ÄÖÅA-Z]\)/\n\1/g' |\
  # sed 's/ -\([äöåa-z]\)/ \1/g' |\
  # sed 's/\([\.?!]\)"/\1\n/g' |\
  # sed 's/WEBVTT//g;s/"//g' |\
  # head -n -1 > $2
