#!/bin/sh
# Full screenshots with software compositing avoid incomplete GPU paint tiles.
set -eu
cd "$(dirname "$0")"
node /home/wangchenkang/.agents/skills/hyperframes/scripts/plugin-cli.mjs render . \
  --fps 24 --quality delivery --low-memory-mode --no-browser-gpu \
  -o ../贾队长-慌啥子嘛-国风鼎香楼-修复闪烁版.mp4
/home/wangchenkang/miniconda3/envs/llm_new/bin/python verify_continuity.py \
  ../贾队长-慌啥子嘛-国风鼎香楼-修复闪烁版.mp4 \
  --output continuity-fixed.json
