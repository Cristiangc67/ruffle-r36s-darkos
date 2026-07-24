#!/bin/bash

# =========================================================
# Game Configuration
# Edit only these variables for each new Flash game.
# =========================================================
GAME_FOLDER="DadNMe"
SWF_FILE="dadnme.swf"
CONTROL_PROFILE="controls.gptk"
# =========================================================

# Engine paths (do not modify)
ENGINE_DIR="/roms/ports/ruffleEngine"
GAME_DIR="$ENGINE_DIR/games/$GAME_FOLDER"

cd "$ENGINE_DIR"

# ---------------------------------------------------------
# PortMaster
# ---------------------------------------------------------

export controlfolder="/opt/system/Tools/PortMaster"
source "$controlfolder/control.txt"

get_controls
export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

# ---------------------------------------------------------
# Mount Weston Runtime
# ---------------------------------------------------------

weston_dir=/tmp/weston
weston_runtime="weston_pkg_0.2"

$ESUDO mkdir -p "${weston_dir}"

if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
    $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
fi

if [[ "$PM_CAN_MOUNT" != "N" ]]; then
    $ESUDO umount "${weston_dir}" 2>/dev/null
fi

$ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

# ---------------------------------------------------------
# Controller Profile
# ---------------------------------------------------------

sudo chmod 666 /dev/uinput
sudo killall gptokeyb 2>/dev/null

$GPTOKEYB "ruffle" -c "$GAME_DIR/$CONTROL_PROFILE" &
sleep 1

# ---------------------------------------------------------
# Optional Debug Logging
#
# Uncomment the following lines if you need to troubleshoot
# graphics or startup issues.
# ---------------------------------------------------------

# rm -f "$GAME_DIR/crash.log"
#
# echo "===== Environment =====" >> "$GAME_DIR/crash.log"
# env | grep -E "WINIT|LIBGL|MESA|WGPU|DISPLAY|WAYLAND" >> "$GAME_DIR/crash.log"
#
# echo "===== Display =====" >> "$GAME_DIR/crash.log"
# echo "DISPLAY=$DISPLAY" >> "$GAME_DIR/crash.log"
# echo "WAYLAND_DISPLAY=$WAYLAND_DISPLAY" >> "$GAME_DIR/crash.log"
# echo "WAYLAND_SOCKET=$WAYLAND_SOCKET" >> "$GAME_DIR/crash.log"
# echo "XDG_SESSION_TYPE=$XDG_SESSION_TYPE" >> "$GAME_DIR/crash.log"
# echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR" >> "$GAME_DIR/crash.log"

# ---------------------------------------------------------
# Launch Ruffle
# ---------------------------------------------------------

$ESUDO env WRAPPED_LIBRARY_PATH="$PWD" \
$weston_dir/westonwrap.sh drm gl kiosk crusty_x11egl \
env \
    -u WAYLAND_DISPLAY \
    WINIT_UNIX_BACKEND=x11 \
    WGPU_BACKEND=gl \
    SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS=0 \
    RUST_LOG=error \
    ./ruffle \
        --width 640 \
        --height 480 \
        --quality low \
        --no-gui \
        --power low \
        "$GAME_DIR/$SWF_FILE"

# If you want to save a crash log, append the following to the
# end of the command above:
#
# >> "$GAME_DIR/crash.log" 2>&1
#
# Logging is disabled by default to avoid unnecessary writes
# to the SD card while playing.

# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------

sudo kill -9 $(pidof gptokeyb) 2>/dev/null

$ESUDO $weston_dir/westonwrap.sh cleanup

if [[ "$PM_CAN_MOUNT" != "N" ]]; then
    $ESUDO umount "${weston_dir}"
fi

pm_finish