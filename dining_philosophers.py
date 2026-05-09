# WITH SEMAPHORES (Controlled Concurrency to avoid deadlocks)

import threading
import time
from threading import Semaphore

N = 5  # Number of philosophers
chopstick = [Semaphore(1) for _ in range(N)]

def philosopher(id):
    while True:
        print(f'Philosopher {id} is thinking...')
        time.sleep(1)

        # Pick up left chopstick
        chopstick[id].acquire()

        # Pick up right chopstick
        chopstick[(id + 1) % N].acquire()

        print(f'Philosopher {id} is eating...')
        time.sleep(2)

        # Put down left chopstick
        chopstick[id].release()

        # Put down right chopstick
        chopstick[(id + 1) % N].release()

        print(f'Philosopher {id} finished eating and put down chopsticks.')

threads = []

# Create philosopher threads
for i in range(N):
    thread = threading.Thread(target=philosopher, args=(i,))
    threads.append(thread)
    thread.start()

# Join threads (never ends in this example)
for thread in threads:
    thread.join()