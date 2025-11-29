# Sect - Game Automation Tool

## What This Does
Automates Roblox games using computer vision (OpenCV) and template matching.

## Key Technical Decisions
- **Template Matching → ORB fallback**: Template matching is fast but fails with rotation/scale. ORB is slower but more robust.
- **PyQt Threading**: Used QThread + Worker pattern to prevent UI freezing during image processing
- **Window Embedding**: Attached Roblox window to Qt container using win32gui

## Challenges Solved
- **Coordinate Systems**: Had to convert between screen coords, window coords, and relative coords
- **Screenshot Performance**: Cached grayscale images, used mss for fast capture
- **Window Management**: Removing/restoring window borders cleanly on attach/detach
- **Connecting Multiple Stuff Together**: I enjoyed it a lot.

## If I Had to Do It Again
- Implement dataclasses for configs
- More comprehensive error handling in coordinate_picker

## User Flow:
MainWindow → chooses game/mode → RobloxWindow
   ↓
GameManager → manages state, threading
   ↓
ImageProcessor → screenshot → template match
   ↓
Worker (QThread) → processes images
   ↓
Clicks module → executes actions

## Things That Worked Well
- Pre-filling functions with partial/lambda made code cleaner