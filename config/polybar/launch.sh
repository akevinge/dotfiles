#!/bin/bash

killall -q polybar

while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

CONF_PATH=$1

polybar main --config=$CONF_PATH &

if [[ $(xrandr -q | grep "HDMI-1 connected") ]]; then
    polybar monitor1 --config=$CONF_PATH &
fi
