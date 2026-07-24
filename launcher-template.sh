#!/bin/bash

# ==========================================
# 1. GAME CONFIGURATION
# ==========================================
SWF_FILE="dadnme.swf"
# ==========================================

ENGINE_DIR="/roms/ports/ruffleEngine"
GAMES_DIR="$ENGINE_DIR/games"

cd "$ENGINE_DIR"

# ---------------------------------------------------------
# RESOLUTION HACK (Forces 640x480 output)
# ---------------------------------------------------------
sudo mount -o remount,rw /

echo '#!/bin/bash' | sudo tee /usr/local/bin/console_detect > /dev/null
echo 'echo "640x480"' | sudo tee -a /usr/local/bin/console_detect > /dev/null
sudo chmod 777 /usr/local/bin/console_detect
# ---------------------------------------------------------

# Clean SDL layout to pass all buttons directly to Ruffle and prevent force feedback crash
sdl_controllerconfig="190000004b4800000011000000010000,GO-Super Gamepad,x:b2,a:b1,b:b0,y:b3,back:b12,start:b13,dpleft:b10,dpdown:b9,dpright:b11,dpup:b8,leftshoulder:b4,lefttrigger:b6,rightshoulder:b5,righttrigger:b7,leftstick:b14,rightstick:b15,leftx:a0,lefty:a1,rightx:a2,righty:a3,platform:Linux,"

# ==========================================
# NATIVE EXECUTION
# ==========================================

# Standard execution (Fast, no background logging)
env SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig" ./rufflesa "$GAMES_DIR/$SWF_FILE" -Q low

# --- DEBUGGING MODE ---
# Uncomment the line below (and comment the one above) to save crash logs to the games folder
# env SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig" ./rufflesa "$GAMES_DIR/$SWF_FILE" -Q low > "$GAMES_DIR/crash_${SWF_FILE}.log" 2>&1