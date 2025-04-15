import os
import random
import threading
import time


class ChaosMonkey:
    """
    Randomly terminate the process to simulate failures 🙈🙉🙊
    """

    @staticmethod
    def start(min_time=5, max_time=20):
        """
        Start a ChaosMonkey that will randomly terminate the process.

        Args:
            min_time (int): Minimum time in seconds before termination (default: 5)
            max_time (int): Maximum time in seconds before termination (default: 20)
        """

        def _chaos_thread():
            """Background thread that waits a random amount of time then kills the process."""
            wait_time = random.uniform(min_time, max_time)
            time.sleep(wait_time)
            print(
                f"\n🐒 ChaosMonkey strikes after {wait_time:.2f} seconds! Terminating process..."
            )
            os._exit(1)

        # Start the chaos thread
        thread = threading.Thread(target=_chaos_thread, daemon=True)
        thread.start()

        print(f"🐒 ChaosMonkey initialized! Process may randomly terminate...")
