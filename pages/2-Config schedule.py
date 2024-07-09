import pandas as pd
import streamlit as st
import os
import seaborn as sns
import pathlib
import schedule
import time

import pathlib
from model.train import training
from crawl.carconnection import crawl_all_car
from crawl.get_detail_car import get_detail_car
from crawl.autolist import crawl_autolist
from data.merge import merge

def job():
    print('crawling from the carconnection...')
    crawl_all_car(st)
    print('get car detail')
    get_detail_car()
    print('crawling from autolist...')
    crawl_autolist(st)
    merge()
    print('training ...')
    training()
    

code_dir = pathlib.Path(__file__).parent.resolve()
def save_config(schedule_type, run_day, run_hour, run_minute):
    config = {
        "schedule_type": schedule_type,
        "run_day": run_day,
        "run_hour": run_hour,
        "run_minute": run_minute
    }

    with open(code_dir/"config.txt", "w") as f:
        f.write(str(config))

    st.success("Cron job configuration saved successfully!")
    # st.experimental_rerun()
    
st.title("Cron Job Scheduler")

    # Load configuration from file if it exists
if os.path.exists(code_dir/"config.txt"):
    with open(code_dir/"config.txt", "r") as f:
        config = eval(f.read())
    schedule_type = config["schedule_type"]
    run_day = config["run_day"]
    run_hour = config["run_hour"]
    run_minute = config["run_minute"]
else:
    schedule_type = "Daily"
    run_day = None
    run_hour = "00"
    run_minute = "00"

schedule_type = st.selectbox("Select Schedule Type", ["Daily", "Weekly"], index=["Daily", "Weekly"].index(schedule_type))

if schedule_type == "Daily":
    run_day = None
    run_hour = st.selectbox("Run at Hour", [f"{i:02d}" for i in range(24)], index=int(run_hour))
    run_minute = st.selectbox("Run at Minute", [f"{i:02d}" for i in range(60)], index=int(run_minute))
elif schedule_type == "Weekly":
    run_day = st.selectbox("Run on Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(run_day) if run_day else 0)
    run_hour = st.selectbox("Run at Hour", [f"{i:02d}" for i in range(24)], index=int(run_hour))
    run_minute = st.selectbox("Run at Minute", [f"{i:02d}" for i in range(60)], index=int(run_minute))
if st.button("Save"):
    schedule.clear()
    if schedule_type == "Weekly":
        if run_day == "Monday":
            schedule.every().monday.at(f"{run_hour}:{run_minute}").do(job)
        elif run_day == "Tuesday":
            schedule.every().tuesday.at(f"{run_hour}:{run_minute}").do(job)
        elif run_day == "Wednesday":
            schedule.every().wednesday.at(f"{run_hour}:{run_minute}").do(job)
        elif run_day == "Thursday":
            schedule.every().thursday.at(f"{run_hour}:{run_minute}").do(job)
        elif run_day == "Friday":
            schedule.every().friday.at(f"{run_hour}:{run_minute}").do(job)
        elif run_day == "Saturday":
            schedule.every().saturday.at(f"{run_hour}:{run_minute}").do(job)
        elif run_day == "Sunday":
            schedule.every().sunday.at(f"{run_hour}:{run_minute}").do(job)
    elif schedule_type == "Daily":
        schedule.every().day.at(f"{run_hour}:{run_minute}").do(job)
    save_config(schedule_type, run_day, run_hour, run_minute)
code_dir = pathlib.Path(__file__).parent.resolve()


if st.button('Recrawl and training now'):
    print('crawling from autolist...')
    crawl_autolist(st)
    print('crawling from the carconnection...')
    crawl_all_car(st)
    print('get car detail')
    get_detail_car()
    merge()
    print('training ...')
    training()
    
    
    
while True:
    
    schedule.run_pending()
    time.sleep(1)
