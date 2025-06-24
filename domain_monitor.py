import requests
import time
import pygame
import sys
import threading
import os.path

# Configuration
DOMAIN_URL = "https://onescan.lspedia.com/"
CHECK_INTERVAL = 10  # seconds between checks
TIMEOUT = 5  # seconds before request times out

# Alert sound file (local file)
ALERT_SOUND_FILE = "vivid-recallection_till-the-end.mp3"

# Initialize pygame for audio
pygame.init()
pygame.mixer.init()

# Functions to handle the alert sound
class SoundManager:
    def __init__(self, sound_file):
        self.sound_file = sound_file
        self.is_loaded = False
        self.is_playing = False
        
    def load_sound(self):
        """Load the local alert sound file"""
        try:
            if not os.path.exists(self.sound_file):
                print(f"Error: Sound file '{self.sound_file}' not found!")
                return False
                
            print(f"Loading alert sound from '{self.sound_file}'...")
            pygame.mixer.music.load(self.sound_file)
            self.is_loaded = True
            print("Alert sound loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading sound: {e}")
            return False
    
    def play_alert(self):
        """Play the alert sound only if it's not already playing"""
        if not self.is_loaded:
            if not self.load_sound():
                print("Cannot play alert - sound not loaded")
                return
        
        try:
            # Check if the sound is already playing
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
                self.is_playing = True
                print("🚨 ALERT: Domain is down! 🚨")
            else:
                # Sound is already playing, just print the alert message
                print("🚨 ALERT: Domain is still down! 🚨")
        except Exception as e:
            print(f"Error playing sound: {e}")
            
    def stop_alert(self):
        """Stop the alert sound"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

# Function to check if the domain is reachable
def check_domain(url, timeout):
    """
    Check if a domain is reachable
    Returns True if reachable, False otherwise
    """
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 400  # Consider any non-4xx/5xx status as "up"
    except requests.RequestException:
        return False

# Function to simulate the domain being down (for testing)
def simulate_domain_down():
    """
    Simulate the domain being down by returning False
    """
    print("Simulating domain down...")
    return False

# Main monitoring function
def monitor_domain(url, interval, timeout, sound_manager, test_mode=False):
    """
    Monitor a domain and play an alert when it's unreachable
    
    Args:
        url: The URL to monitor
        interval: Time between checks in seconds
        timeout: Request timeout in seconds
        sound_manager: SoundManager instance for alerts
        test_mode: If True, run in test mode (simulate domain down)
    """
    print(f"Starting to monitor {url}")
    print(f"Checking every {interval} seconds (timeout: {timeout}s)")
    print("Press Ctrl+C to stop monitoring")
    
    if test_mode:
        print("🧪 TEST MODE ACTIVE - Will simulate domain being down 🧪")
    
    previous_state = None  # Track the previous state to detect changes
    
    try:
        while True:
            is_up = False if test_mode else check_domain(url, timeout)
            
            # First check or state changed
            if previous_state is None or previous_state != is_up:
                if is_up:
                    print(f"✅ {url} is UP - {time.strftime('%H:%M:%S')}")
                    # Stop alert if it was playing and domain is now up
                    sound_manager.stop_alert()
                else:
                    print(f"❌ {url} is DOWN - {time.strftime('%H:%M:%S')}")
                    # Play alert in a separate thread to avoid blocking
                    threading.Thread(target=sound_manager.play_alert).start()
            else:
                # State unchanged, just print a status dot to show we're still checking
                if is_up:
                    print(".", end="", flush=True)
                else:
                    # If still down, ensure alert is playing
                    threading.Thread(target=sound_manager.play_alert).start()
            
            # Update previous state
            previous_state = is_up
                
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    finally:
        # Make sure to stop any playing sounds before quitting
        sound_manager.stop_alert()
        pygame.quit()

# Main function
def main():
    # Parse command line arguments
    test_mode = "--test" in sys.argv
    
    # Create sound manager with the correct alert sound file
    sound_manager = SoundManager(ALERT_SOUND_FILE)
    
    # Load sound at startup
    sound_manager.load_sound()
    
    # Start monitoring
    monitor_domain(DOMAIN_URL, CHECK_INTERVAL, TIMEOUT, sound_manager, test_mode)

if __name__ == "__main__":
    main()