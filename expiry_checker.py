import time
from database import remove_expired

def run():
    while True:
        remove_expired()
        time.sleep(3600)
