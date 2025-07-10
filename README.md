# TT-Seek 🚍🧠

TT-Seek is a smart transit optimization prototype built using the Gemini API, Python Flask, and Leaflet.js. This project visualizes real-time transit data on a map, estimates foot traffic around bus stops, and uses AI to suggest optimized bus scheduling — including which stops to emphasize or avoid.

This project was developed during the MLH x SolutionHacks Hackathon (June 27–29, 2025).

The aim of this project is to assist with the UN's SDG goal #11: Sustainable Cities & Communities

---

## 🔍 Project Overview

The app simulates and analyzes transit flow by:
- Randomly generating commuter presence around TTC bus stops.
- Mapping this data into a heatmap-style visualization.
- Sending that compiled information to the Gemini API.
- Using AI analysis to determine:
  - Optimal number of buses to deploy
  - Ideal bus intervals
  - High-priority and low-priority bus stops

---

## 📦 How to Run the Demo

1. Download the ZIP file from this repository.
2. Open `run.py` in your preferred Python IDE or compiler.
3. Run the script.

Once running, visit:

```bash
http://127.0.0.1:5000/map
```