#!/usr/bin/env bash

YEAR=2021

DAY="$(echo 0$1 | sed 's/.*\(..\)$/\1/')"

INPUT="$2"


RUNDOCKER="docker run --rm -i aoc python $DAY.py"



case $INPUT in
    input)
        TMPFILE="$(mktemp)"
        aocd $DAY $YEAR > $TMPFILE || (rm -f $TMPFILE && exit 1)

        cat $TMPFILE | $RUNDOCKER
        rm -f $TMPFILE
        ;;
    *)
        cat $DAY-example.txt | $RUNDOCKER
        ;;
esac
