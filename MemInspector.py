#!/usr/bin/env python3
import signal
from subprocess import run, Popen, PIPE
from os import kill
from time import sleep
from setproctitle import setproctitle

cache = {"startup": True}

def get_memory_info():
    memory_raw_data = Popen("free", stdout=PIPE)
    memory_info = memory_raw_data.stdout.read().split()
    memory_free = int(memory_info[12])
    memory_total = int(memory_info[7])
    swap_free = int(memory_info[16])
    swap_total = int(memory_info[14])
    pid = int(Popen(["ps", "-aux", "--sort", "-%mem"], stdout=PIPE).stdout.read().splitlines()[1].split()[1])

    return {"memory_free": memory_free,
            "memory_total": memory_total,
            "swap_free": swap_free,
            "swap_total": swap_total,
            "the_most_usage_process": pid}

def control_swap(mode: int):
    if mode == 0:
        run(["swapoff", "-a"])
    if mode == 1:
        run(["swapon", "-a"])

if __name__ == "__main__":
    while True:
        if cache["startup"]:
            setproctitle("meminspector")
        memory = get_memory_info()
        if memory["memory_free"] / memory["memory_total"] <= 0.10 and memory["swap_total"] == 0:
            control_swap(1)
        else:
            if (memory["memory_free"] - (memory["swap_total"] - memory["swap_free"])) / memory["memory_total"] > 0.15:
                control_swap(0)
        if (memory["memory_free"] + memory["swap_free"]) / (memory["memory_total"] + memory["swap_total"]) <= 0.05:
            kill(memory["the_most_usage_process"], signal.SIGKILL)
        sleep(5)
