# About
This is a repository for a *Luxor* to *OpenSMCE* converter.

This is needed so that the engine can be legally playtested (*Luxor* assets can't be uploaded onto the repository due to legal reasons).

The main OpenSMCE project can be found at https://github.com/jakubg1/OpenSMCE

# Game Conversion
In order to play Luxor or Luxor Amun Rising on this engine, you need to have an original copy of the game.
Then, you need to convert this game using this converter, which is bundled in the `games/` directory if you've downloaded from the Releases page.

You will need:
- raw uncompressed Luxor 1 or Luxor Amun Rising's data (Luxor 2, Luxor 3, Luxor Evolved etc. WILL NOT WORK!),
- Python 3 installed on your computer.

The conversion is a one-time process, though it needs to be repeated for each OpenSMCE version, because of incompatibilities between versions.
Make sure you're running the correct converter for your OpenSMCE version.

## Python Installation (Windows only)
1. Download the latest Python version from the [official Python page](https://www.python.org/downloads/windows/).
2. Open the installer and click "Install Now"
3. You don't need to add Python to PATH, but you can if you want to.
4. Wait until the installation finishes.

## Pillow Installation
Pillow is a library that is used to process images from the original games.
On Linux, you might need to install `pip` first:
- Ubuntu/Debian: `sudo apt install python3-pip`
- Fedora: `sudo dnf install python3-pip`

To install Pillow, regardless of your OS, run this command in the command prompt:
`python -m pip install pillow`

## Installation
1. Uncompress Luxor files using QuickBMS - both `data.mjz` and `English.mjz` files will be needed.
2. Copy the unpacked `data/` and `English/` folders, ALONG WITH `assets` folder to the `games` folder in your main OpenSMCE directory.
3. Run the `convert.bat` (Windows) / `convert.sh` (Linux) script and follow the instructions if necessary.

## Running the game
If the conversion has been successful, go back to the main engine directory and launch OpenSMCE. The converted game should be visible on the boot screen.

If the conversion has been unsuccessful or the converted game crashed during startup, make sure to [report an issue](https://github.com/jakubg1/OpenSMCE_Converter/issues).
