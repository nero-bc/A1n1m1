import requests
from datetime import datetime, timedelta, timezone , date
import re

def english(text):
    if re.match(r'^[A-Za-z\s]+$', text):
        return True
    else:
        return False

def day_(x: int,today: int = None):
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    if not today:return days[x]
    else: 
        diff = x - today
        day = 'yesterday' if diff == -1 else 'tomorrow' if diff == 1 else 'today' if diff == 0 else ''
        if day != '':return day
        else: return days[x]
  
def get_scheduled(weekday=None):
    base_url = "https://api.jikan.moe/v4/schedules/"
    if not weekday:
        day = str(day_((datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date().weekday()))
        day_str = day
    else:
        day = day_(weekday)
        day_str = day_(weekday,(datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date().weekday())
    date_str = f"Scheduled animes for {day_str}\n\n"
    data = requests.get(base_url+day).json()
    sched_ls =  data["data"]
    out = []
    for i in sched_ls:
        try:
            title = i['titles'][-1]['title'] if english(i['titles'][-1]['title']) else i['titles'][1]['title'] if english(i['titles'][1]['title']) else i['titles'][0]['title']
        except IndexError:
            title = i['title']
        out.append(title)
    return date_str, out 

def get_estimated_time_of_arrival() -> int:
    sri_lanka_time = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30))
    midnight = datetime.strptime('23:59:59', '%H:%M:%S').time()
    difference = int((datetime.combine(datetime.today(), midnight) - datetime.combine(datetime.today(), sri_lanka_time.time())).seconds) + 20
    return int(difference)
