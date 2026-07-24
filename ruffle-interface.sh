#!/bin/bash

ENGINE_DIR="/roms/ports/ruffleEngine"
GAMES_DIR="$ENGINE_DIR/games"
cd "$ENGINE_DIR" || exit

# Clean up old temporary files
rm -f /tmp/ruffle_selected.txt

# Force 640x480 output for Pygame and Ruffle
sudo mount -o remount,rw /
echo '#!/bin/bash' | sudo tee /usr/local/bin/console_detect > /dev/null
echo 'echo "640x480"' | sudo tee -a /usr/local/bin/console_detect > /dev/null
sudo chmod 777 /usr/local/bin/console_detect

# Clean SDL layout to prevent force feedback issues
sdl_controllerconfig="190000004b4800000011000000010000,GO-Super Gamepad,x:b2,a:b1,b:b0,y:b3,back:b12,start:b13,dpleft:b10,dpdown:b9,dpright:b11,dpup:b8,leftshoulder:b4,lefttrigger:b6,rightshoulder:b5,righttrigger:b7,leftstick:b14,rightstick:b15,leftx:a0,lefty:a1,rightx:a2,righty:a3,platform:Linux,"

while true; do
    clear
    
    # Run the Python menu (system errors will be saved to pygame_error.log)
    python3 launcher.py 2> "$ENGINE_DIR/pygame_error.log"
    
    # Check if Python successfully created the temp file with the game name
    if [ -f "/tmp/ruffle_selected.txt" ]; then
        SELECTED_GAME=$(cat "/tmp/ruffle_selected.txt")
        rm -f "/tmp/ruffle_selected.txt" # Delete it for the next run
        
        # Execute Ruffle
        env SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig" ./rufflesa "$GAMES_DIR/$SELECTED_GAME" -Q low
    else
        # If the file doesn't exist, the user pressed Exit (Button B / Start)
        clear
        break
    fi
done

clear
exit 0