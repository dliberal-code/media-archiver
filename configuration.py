# Configuration Template for Media Archiver
# Copy this file to 'config.py' and adjust settings.

# --- 1. COMMON SETTINGS ---
# The disk or folder you want to scan/process
SOURCE_PATH = "/mnt/d"

# File to store recognized device signatures. 
# Created in the folder where you run the script. (Excluded from Git)
CATALOG_FILE = "catalog.json"

# Supported extensions for media (lowercase)
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi', '.m4v'}


# --- 2. PHASE 1 SETTINGS (sampler.py) ---
# Stop after inspecting this many files
TARGET_FILE_COUNT = 500

# Stop after finding this many new unique camera signatures
TARGET_VENDOR_COUNT = 5


# --- 3. PHASE 2 SETTINGS (archiver.py) ---
# The physical root folder where the organized library will be created
DESTINATION_PATH = "/mnt/storage/organized_library"

# The subfolder structure inside DESTINATION_PATH
# Available variables: {device}, {year}, {month}
PATH_TEMPLATE = "{device}/{year}/{month}"

# Disk Identifier (Optional)
# If set, Misc files go to: /Misc/{DISK_ID}/{year}/
# If set to None, Misc files go to a global: /Misc/{year}/
DISK_ID = None

