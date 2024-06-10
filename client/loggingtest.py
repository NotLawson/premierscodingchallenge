## Logging test ##
from threading import Thread
import sys, time, random, math
import progressbar as taskbar


def task1():
    from time import sleep
    sleep(1)
    print("after 1 sec")
    sleep(2)
    print("after 2 sec")

def task2():
    from time import sleep
    sleep(5)


def tasker(task, taskname):
    widgets = [
        f"time -- (TASK) [{taskname}] Running for ", taskbar.Timer("%s"), "s ", taskbar.AnimatedMarker()
    ]
    taskthread = Thread(target=task, daemon=True)
    starttime = time.perf_counter()
    taskthread.start()
    bar = taskbar.ProgressBar(max_value=1, widgets=widgets, redirect_stdout=True).start()
    while taskthread.is_alive():
        bar.update(0)
    bar.update(1)
    out = f"\rtime -- (DONE) [{taskname}] Finished in {bar.start_time}      "
    print(out)




tasker(task1, "task1")
tasker(task2, "task2")

'''out = f"time -- (TASK) [app] [{round(time.perf_counter() - starttime, 1)}] Running {taskname}"
        sys.stdout(out+"\r")
    out = f"time -- (DONE) [app] [{round(time.perf_counter()- starttime, 1)}]    {taskname}"
    print(out)'''