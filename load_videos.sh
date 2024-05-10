#!/bin/bash

ffmpeg -hide_banner -y -loglevel error -rtsp_transport tcp -use_wallclock_as_timestamps 1 -i rtsp://77.232.139.186:8554/live.stream -vcodec copy -acodec copy -f segment -reset_timestamps 1 -segment_time 300 -segment_format mkv -segment_atclocktime 1 -strftime 1 ./videos/%Y-%m-%dT%H-%M-%S.mkv < /dev/null