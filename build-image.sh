#!/usr/bin/env bash
LATEST_DAY="$(ls [012][0-9].py | sort | tail -1 | sed 's/\.py$//')"
LATEST_YEAR="2021"
TARGET="aoc-$LATEST_YEAR"

if [[ -z "$1" ]]; then
    docker build  -t $TARGET:latest -t $TARGET:$LATEST_DAY . > /dev/null
else
    docker build  -t $TARGET:latest -t $TARGET:$LATEST_DAY .
fi
