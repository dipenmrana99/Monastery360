# Monastery360 (Flask)

A free, offline-friendly Flask app to showcase Sikkim's monasteries with virtual tours via Google Street View links (no paid APIs).

## Features
- Browse monasteries on an interactive map (Leaflet + OpenStreetMap).
- Detail pages with description, images, audio guides, and a **"Open Street View"** button (redirects to Google Maps Street View link you provide).
- Search and filters.
- Cultural calendar / events.
- Digital archives (images & documents) gallery.
- Participation & booking form stored locally in SQLite (no external services).
- Mobile-friendly, clean UI.

## Requirements
- Python 3.9+ (works with most recent versions)
- pip

## Quick Start
```bash
pip install -r requirements.txt
export FLASK_APP=app.py
flask run  # or: python app.py
```

Then open: http://127.0.0.1:5000/

## Adding/Editing Monasteries
Edit `data/monasteries.json`. Each item supports:
```json
{
  "id": "rumtek-monastery",
  "name": "Rumtek Monastery",
  "district": "Gangtok",
  "founded": "18th century",
  "lat": 27.3323,
  "lng": 88.6227,
  "languages": ["en", "hi", "ne"],
  "street_view_url": "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=27.3323,88.6227",
  "image": "/static/assets/images/rumtek.jpg",
  "audio_guide": "/static/assets/audio/rumtek_guide.mp3",
  "summary": "Seat of the Karma Kagyu lineage, known for its grandeur and sacred relics.",
  "description": "Longer description here...",
  "nearby": ["Pemayangtse Monastery"]
}
```

> **Street View:** Paste any Google Street View or Maps panorama link into `street_view_url`. The app simply opens the link in a new tab.

## Adding Events
Edit `data/events.json` and add your own festival/ritual schedules.

## Archives
Place images/documents into `static/assets/images/` and add metadata entries in `data/archives.json` (optional).

## Data Privacy
All data stays local. Booking/participation submissions are stored in `submissions.db` (SQLite).

## Notes
- Leaflet + OSM tiles are free to use for light to moderate traffic. For heavy use, consider hosting your own tiles per OSM policy.
- No paid APIs or keys needed.
