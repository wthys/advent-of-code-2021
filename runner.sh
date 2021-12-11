#!/usr/bin/env bash

SCRIPTDIR="$(dirname "$(readlink -f "$0")")"

YEAR=2021

DAY="$(echo 0$1 | sed 's/.*\(..\)$/\1/')"

INPUT="$2"

RUNDAY="python3 $DAY.py"

case $INPUT in
    input)
        TMPFILE="$(mktemp)"
        aocd $DAY $YEAR > $TMPFILE || (rm -f $TMPFILE && exit 1)

        $RUNDAY $TMPFILE
        rm -f $TMPFILE
        ;;
    *)
        $RUNDAY $SCRIPTDIR/$DAY-example.txt
        ;;
esac
