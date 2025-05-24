from collections import defaultdict
import time

class Analyzer:
    def __init__(self, log_deque, time_window=60):
        self.log = log_deque
        self.time_window = time_window

    def get_aggressive_offenders(self):
        now = time.time()
        offenders = defaultdict(int)
        for entry in self.log:
            if now - entry['timestamp'] < self.time_window:
                offenders[entry['mac']] += 1
        return {mac: count for mac, count in offenders.items() if count > 10}
