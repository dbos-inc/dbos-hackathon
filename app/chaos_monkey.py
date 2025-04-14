import os
import random
import threading
import time


class ChaosMonkey:
    """
    Randomly terminate the process to simulate failures 🙈🙉🙊 
    """
    
    def __init__(self, min_time=5, max_time=20):
        """
        Initialize the ChaosMonkey and start the background thread.
        
        Args:
            min_time (int): Minimum time in seconds before termination (default: 5)
            max_time (int): Maximum time in seconds before termination (default: 20)
        """
        self.min_time = min_time
        self.max_time = max_time
        self.thread = threading.Thread(target=self._chaos_thread, daemon=True)
        self.thread.start()
        
        print(f"🐒 ChaosMonkey initialized! Process may randomly terminate...")
    
    def _chaos_thread(self):
        """Background thread that waits a random amount of time then kills the process."""
        wait_time = random.uniform(self.min_time, self.max_time)
        time.sleep(wait_time)
        print(f"\n🐒 ChaosMonkey strikes after {wait_time:.2f} seconds! Terminating process...")            
        os._exit(1)