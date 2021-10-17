from celery import Celery
from celery.app import task
import time
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x,y):
    time.sleep(2)
    return x+y