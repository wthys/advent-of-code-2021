#!/usr/bin/env bash
LATEST_DAY="$(ls [012][0-9].py | sort | tail -1 | sed 's/\.py$//')"
LATEST_YEAR="2021"

if [[ -z "$1" ]]; then
    docker build  -t aoc:latest -t aoc:$LATEST_YEAR-$LATEST_DAY . > /dev/null
else
    docker build  -t aoc:latest -t aoc:$LATEST_YEAR-$LATEST_DAY .
fi
