import time
from database import remove_expired

def run_expiry_checker():
    while True:
        remove_expired()
        time.sleep(3600)  # every 1 hour
