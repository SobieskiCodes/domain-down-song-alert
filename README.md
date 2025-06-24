# Domain Monitor with Alert

A simple Python script that monitors a domain and plays an alert sound when the domain becomes unreachable. Perfect for emergency monitoring during high-alert situations.

## Features

- Continuously monitors a website/domain for availability
- Plays a customizable alert sound when the domain goes down
- Automatically stops the alert when the domain comes back online
- Includes test mode to verify alert functionality
- Clean, informative console output with status indicators
- Simple to set up and use

## Requirements

- Python 3.6 or higher
- Required Python packages (see `requirements.txt`):
  - requests
  - pygame

## Installation

1. Clone or download this repository
2. Place your alert sound file (MP3 format) in the same directory as the script
3. Install required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Edit the following variables at the top of `domain_monitor.py` to customize:

```python
# Configuration
DOMAIN_URL = "URL HERE"  # URL to monitor
CHECK_INTERVAL = 10  # seconds between checks
TIMEOUT = 5  # seconds before request times out

# Alert sound file (local file) https://www.reverbnation.com/vividrecallection/song/14147315-till-the-end
ALERT_SOUND_FILE = "vivid-recallection_till-the-end.mp3"  # Your sound file
```

## Usage

### Normal monitoring mode

```bash
python domain_monitor.py
```

### Test mode (simulates domain being down)

```bash
python domain_monitor.py --test
```

Press `Ctrl+C` to stop monitoring at any time.

## Console Output

- `✅ [URL] is UP - [time]`: Domain is reachable
- `❌ [URL] is DOWN - [time]`: Domain is unreachable
- `.`: Domain continues to be up (reduces console clutter)
- `🚨 ALERT: Domain is down! 🚨`: Alert sound is playing

## Troubleshooting

- **Sound file not found**: Ensure your MP3 file is in the same directory and correctly named
- **No sound playing**: Check that your system volume is on and pygame is properly installed
- **Installation errors**: Make sure you have Python 3.6+ and pip installed correctly

## License

This project is open source and available for any use.