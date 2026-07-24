#!/bin/bash

# ==========================================
# 1. WAKE UP THE SCREEN (TTY SETUP)
# ==========================================
# Force output to the physical console so the user can see the progress
export TERM=linux
export CONSOLE=/dev/tty1
exec < $CONSOLE > $CONSOLE 2>&1
clear

# Define colors for terminal aesthetics
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}    Ruffle                            ${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# ==========================================
# 2. INTERNET CHECK
# ==========================================
echo -e "${GREEN}[*] Checking internet connection...${NC}"

# Send a single ping to Google servers, with a 2-second timeout
if ping -q -c 1 -W 2 8.8.8.8 >/dev/null; then
    echo -e "${GREEN}[+] Connection detected. Preparing system...${NC}"
else
    echo -e "${RED}[!] ERROR: No internet connection.${NC}"
    echo -e "${RED}Please connect a Wi-Fi dongle or share network via USB to your console.${NC}"
    echo ""
    echo -e "${GREEN}Returning to dArkOS in 5 seconds...${NC}"
    sleep 5
    clear
    exit 1
fi

echo ""

# ==========================================
# 3. INSTALLING DEPENDENCIES (PYGAME)
# ==========================================
echo -e "${GREEN}[*] Enabling write permissions on the root partition...${NC}"
sudo mount -o remount,rw /

echo -e "${GREEN}[*] Updating repositories (This may take a few minutes)...${NC}"
sudo apt-get update -y

echo -e "${GREEN}[*] Downloading and installing Pygame for ArkOS...${NC}"
# We use apt-get instead of pip because on ARM architectures (like the R36S) 
# compiling Pygame from scratch takes a long time. The precompiled package is immediate.
sudo apt-get install -y python3-pygame

# ==========================================
# 4. FINAL CHECK
# ==========================================
# $? stores the result of the last command. 0 means absolute success.
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}[+] INSTALLATION COMPLETED SUCCESSFULLY!${NC}"
    echo -e "${GREEN}[+] Your R36S is now compatible with the native Ruffle interface.${NC}"
else
    echo ""
    echo -e "${RED}[!] There was a problem downloading the packages.${NC}"
    echo -e "${RED}Please ensure your internet connection is stable and try again.${NC}"
fi

echo ""
echo -e "${GREEN}Returning to dArkOS in 5 seconds...${NC}"
sleep 5
clear
exit 0