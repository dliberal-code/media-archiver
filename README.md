#Media Organization Architecture

## Overview
A two-phase automated system designed to identify primary capture devices and systematically organize mixed media from multiple source disks into a structured, deduplicated library.

## Environment & Tools
* Platform: Ubuntu (WSL2) with native EXT4 mounts.
* System Dependency: exiftool (sudo apt install exiftool).
* Python Dependencies: pyexiftool (installed via pip).

## Repository Management (One-liner Sync)
To keep your repository updated easily, you can use the following command:
`git add . && git commit -m "Update: $(date +'%Y-%m-%d %H:%M')" && git push origin main`

Or create a `sync.sh` file:
```bash
#!/bin/bash
git add .
git commit -m "${1:-'chore: Manual archive update'}"
git push origin main

```

## Phase 1: Metadata Sampling & Cataloging (sampler.py)
Goal: Build and refine a device "dictionary" to distinguish between primary cameras and "Misc" sources.
* Catalog Awareness: The script loads the existing catalog.json.
* Target-Driven Sampling:
    - TARGET_FILE_COUNT: Maximum number of files to inspect (e.g., 500).
    - TARGET_VENDOR_COUNT: Maximum number of new unique camera vendors to discover before stopping (e.g., 5).
* Filtering Logic:
    - For each sampled file, extract the EXIF signature (Make, Model, Software, HostComputer).
    - If the signature is already in catalog.json, it is ignored.
    - If unknown, it is stored in a "Discovery Buffer" with a frequency count.
* Interaction: After hitting a target or finishing the scan, the script presents the Discovery Buffer. The user can assign a "Friendly Name" to a signature to append it to the catalog.

## Phase 2: Systematic Sorting & Moving (archiver.py)
Goal: Process disks one by one and sort media based on the approved catalog.
* Consumption: Uses the finalized catalog.json.
* Logic:
    - Match: Copy to {base}/{device}/{year}/{month}/{filename}.
    - No Match: Copy to {base}/Misc/{disk_id}/{year}/{filename}.
* Deduplication: SHA-256 hash comparison.
* Conflict Resolution: 4-character hash-based suffix for name collisions with different content.

## Security & Integrity Constraints
1. Source Preservation: All operations are Read-Only on source disks.
2. Atomic Operations: Checksums verified after copying.
3. Logging: Comprehensive CSV logging for audit trails.

