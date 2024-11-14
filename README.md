# RimLists

**RimLists** is a user-friendly script designed to create a RimWorld modlist from a Steam Workshop collection URL. The generated modlist is compatible with [RimPy Mod Manager for RimWorld](https://github.com/rimpy-custom/RimPy).

## Quick Start Guide

1. **Install Python:** Download and install [Python 3.9 or higher](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. **Download This Tool:**
   - Click the green "Code" button above
   - Select "Download ZIP"
   - Extract the ZIP file anywhere on your computer

3. **Install Requirements:**
   - Open Command Prompt (cmd)
   - Navigate to the extracted folder:
     ```bash
     cd path/to/extracted/folder
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Tool:**
   ```bash
   python main.py
   ```

5. **Using the Tool:**
   - Paste your Steam Workshop Collection URL
   - Choose where to save the modlist (defaults to RimPy's ModLists folder)
   - Toggle "Include DLCs" if you want DLCs in your modlist
   - Click "Start"!

## Detailed Instructions

### Getting Your Workshop Collection URL
1. Go to your Steam Workshop Collection
2. Copy the URL from your browser
3. It should look something like: `https://steamcommunity.com/sharedfiles/filedetails/?id=XXXXXXXX`

### Where to Find the Generated Modlist
By default, the modlist saves to:
```
C:\Users\[YourUsername]\AppData\Local\RimPy Mod Manager\ModLists
```

### Troubleshooting

If you encounter any issues:

1. **Python Not Found:**
   - Make sure Python is installed and added to PATH
   - Try running `python --version` in Command Prompt to verify

2. **Dependencies Error:**
   - Try running:
     ```bash
     pip install requests beautifulsoup4 Gooey
     ```

3. **Path Not Found:**
   - Make sure Steam and RimWorld are installed
   - The script should auto-detect paths, but you might need to manually specify them

4. **Other Issues:**
   - Check if all mods in the collection are downloaded in Steam
   - Verify your Steam Workshop collection URL is correct
   - [Create an issue](https://github.com/olibols/Steam-Rimworld-Modlist-Scraper/issues) if you need help

## Requirements

- Python 3.9+
- Steam
- RimWorld (installed via Steam)
- Internet connection to access Steam Workshop

## Contributing

Found a bug or want to contribute? [Open an issue](https://github.com/olibols/Steam-Rimworld-Modlist-Scraper/issues) or submit a pull request!

---

© 2024 RimLists Contributors
