#!/bin/env bash
cd "$(dirname ${BASH_SOURCE[0]})"

printf "%s\n" \
    "-=- Luxor to OpenSMCE Game Converter -=-" \
    "" \
    "===========================================" \
    "Step 0. Checking the requirements..." \
    "==========================================="
good=1

python --version > /dev/null
if [ $? -ne 0 ]; then
    printf "! Python is not installed !\n"
    good=0
fi

if [ ! -d "./data" ]; then
    printf "! Folder \"data\" does not exist !\n"
    good=0
fi

if [ ! -d "./english" ] && [ ! -d "./English" ]; then
    printf "! Folder \"english\" does not exist !\n"
    good=0
fi

if [ ! -d "./assets" ]; then
    printf "! Folder \"assets\" does not exist !\n"
    good=0
fi

if [ ! -d "./Luxor_appendix" ]; then
    printf "! Folder \"/Luxor_appendix\" does not exist !\n"
    good=0
fi

if [ $good -eq 1 ]; then
    printf "All good!\n"
else
    printf "%s\n" \
        "===========================================" \
        "The converter found some issues and will not convert the game properly." \
        "They are listed above." \
        "Before proceeding, fix them and run convert.bat again." \
        "If you think some of these errors are false positive," \
        "contact me on Discord!" \
        "===========================================" \
        "" \
        "The converter will now close."
    exit
fi

printf "%s\n" '' '' \
    "If you haven't checked README file yet, just in case please do it before proceeding!" \
    "The original files will be available in \"_BACKUP\" directory. If you want to, you can delete it afterwards." \
    "===========================================" \
    "The converter will start working once you press any key."

read -rsn1

printf "%s\n" '' '' '' '' \
    "===========================================" \
    "Step 1. Preparing and backing up..." \
    "==========================================="

if [ -d "./English" ]; then
    printf "The \"English\" folder should be named \"english\" because Linux, fixing... "
    mv ./English ./english
    printf "Done!\n"
fi

if [ -d "./data/data" ]; then
    printf "The \"data\" folder is nested too deeply, fixing... "
    cp -aflt ./data ./data/data/*
    rm -rf ./data/data
    printf "Done!\n"
fi

if [ -d "./english/english" ]; then
    printf "The \"english\" folder is nested too deeply, fixing... "
    cp -aflt ./english ./english/english/*
    rm -rf ./english/english
    printf "Done!\n"
fi

mkdir -p ./_BACKUP
cp -aft ./_BACKUP ./data ./english ./assets ./Luxor_appendix

printf "%s\n" '' '' '' '' \
    "===========================================" \
    "Step 2. Merging data/ with english/..." \
    "==========================================="

    cp -aflt ./data ./english/data/*
    rm -rf ./english


printf "%s\n" '' '' '' '' \
    "===========================================" \
    "Step 3. Converting..." \
    "==========================================="
# Linux is case sensitive -_-
# TODO: Move this logic to main.py!
mv data/maps/PooloftheLotusBlossom data/maps/PoolOfTheLotusBlossom
mv data/maps/ScrollofThoth data/maps/ScrollOfThoth

#python -m pip install pillow
python main.py
if [ $? -ne 0 ]; then
    printf "%s\n" '' '' '' '' \
	"===========================================" \
	"Oh no! Something has gone wrong during the conversion process." \
	"Please screenshot the console and send it to me via Discord!" \
	"===========================================" \
	"" \
	"The converter will now close."
    read -rn1 -p "Would you like to revert the files to the original state? [Y/n]" keep

    if [[ $keep =~ [yY] ]]; then
        printf "%s\n" '' \
        "Okay, reverting..."
        rm -rf output Luxor data assets Luxor_appendix
        cp -aft . ./_BACKUP/data ./_BACKUP/english ./_BACKUP/assets ./_BACKUP/Luxor_appendix
        rm -rf _BACKUP
    fi
	exit
fi

printf "%s\n" '' '' '' '' \
    "===========================================" \
    "Step 4. Copying additional files..." \
    "==========================================="
mkdir -p ./output/music ./output/sounds
cp -aft ./output/music ./data/music/*
cp -aft ./output/sounds ./data/sound/*
cp -aft ./output/ ./Luxor_appendix/*
rm -f ./output/music/*.sl3
rm -f ./output/sounds/*.sl3

printf "%s\n" '' '' '' '' \
    "===========================================" \
    "Step 5. Cleaning up..." \
    "==========================================="

mv output Luxor
rm -rf data assets Luxor_appendix
mv Luxor/_config.json Luxor/config.json

printf "%s\n" \
    "The converter finished its job, hopefully successfully." \
    "If you haven't spotted any error in this console, you can launch OpenSMCE now.." \
    "If you have spotted an error though, make sure you have Python installed and all required folders." \
    "If you struggle to find a source of the error, send a screenshot of this console to me via Discord!" \
    "Press any key to close this window."
read -rsn1