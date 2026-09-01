#!/usr/bin/env bash
exec ros2 launch realsense2_camera multi_camera.launch.py \
  front_serial:="_339222072303" \
  left_serial:="_342222072249" \
  right_serial:="_335222076319"
