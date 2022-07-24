import schedule
import time

def job ():
    print("123---")

schedule.every(2).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

