import os
import threading

import fibmodule

for _ in range(os.cpu_count()):
    arg = 35
    threading.Thread(target=fibmodule.fib, args=(arg,)).start()
