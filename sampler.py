import os
import json
import random
import logging
from pathlib import Path
import exiftool

# Try to import local config, fallback to defaults or exit if missing
try:
    import config
except ImportError:
    print("Error: 'config.py' not found.")
    print("Please copy 'config.py.sample' to 'config.py' and edit it.")
    exit(1)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_catalog():
    """Loads the existing catalog or returns an empty dict."""
    if os.path.exists(config.CATALOG_FILE):
        try:
            with open(config.CATALOG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load catalog: {e}")
            return {}
    return {}

def save_catalog(catalog):
    """Saves the catalog dictionary to a JSON file."""
    with open(config.CATALOG_FILE, 'w') as f:
        json.dump(catalog, f, indent=4)
    logging.info(f"Catalog saved to {config.CATALOG_FILE}")

def get_signature(metadata):
    """Creates a unique string signature from EXIF data."""
    make = str(metadata.get('EXIF:Make', 'Unknown')).strip()
    model = str(metadata.get('EXIF:Model', 'Unknown')).strip()
    software = str(metadata.get('EXIF:Software', 'None')).strip()
    
    return f"Make: {make} | Model: {model} | Software: {software}"

def run_sampler():
    catalog = load_catalog()
    discovery_buffer = {}
    files_processed = 0
    new_vendors_found = 0
    
    logging.info(f"Scanning {config.SOURCE_PATH} for media files...")
    all_files = []
    for root, _, files in os.walk(config.SOURCE_PATH):
        for name in files:
            if Path(name).suffix.lower() in config.EXTENSIONS:
                all_files.append(os.path.join(root, name))
    
    if not all_files:
        logging.warning("No media files found in the source path.")
        return

    random.shuffle(all_files)
    logging.info(f"Starting sampling of {len(all_files)} files...")

    with exiftool.ExifToolHelper() as et:
        for file_path in all_files:
            if files_processed >= config.TARGET_FILE_COUNT or new_vendors_found >= config.TARGET_VENDOR_COUNT:
                break
            
            try:
                metadata_list = et.get_metadata(file_path)
                if not metadata_list:
                    continue
                
                metadata = metadata_list[0]
                sig = get_signature(metadata)
                
                if sig in catalog:
                    continue
                
                if sig not in discovery_buffer:
                    discovery_buffer[sig] = {"count": 1, "example": file_path}
                    new_vendors_found += 1
                    logging.info(f"Found new signature: {sig}")
                else:
                    discovery_buffer[sig]["count"] += 1
                
                files_processed += 1
                
            except Exception as e:
                logging.debug(f"Could not process {file_path}: {e}")
                continue

    if not discovery_buffer:
        logging.info("No new signatures found. All sampled files match the existing catalog.")
        return

    print("\n" + "="*50)
    print("DISCOVERY RESULTS")
    print("="*50)
    
    new_entries = {}
    for i, (sig, info) in enumerate(discovery_buffer.items(), 1):
        print(f"\n[{i}] Signature: {sig}")
        print(f"    Occurrences found: {info['count']}")
        print(f"    Example file: {info['example']}")
        
        choice = input("Assign a friendly name for this device (or press Enter to skip/misc): ").strip()
        if choice:
            new_entries[sig] = choice

    if new_entries:
        catalog.update(new_entries)
        save_catalog(catalog)
        print(f"Added {len(new_entries)} new devices to your catalog.")
    else:
        print("No changes made to the catalog.")

if __name__ == "__main__":
    run_sampler()
