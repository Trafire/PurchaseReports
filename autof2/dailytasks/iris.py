from autof2.navigation import navigation
from autof2.interface.send_data import SendData
from datetime import date, timedelta, datetime
import time

def turn_off_iris(list_num):
    send = SendData()
    navigation.to_iris_online_dates(list_num)
    send.send('{enter}')
    send.send('00/00/00')
    send.send('{enter}')
    send.send('01/01/15')
    send.send('{enter}')
    send.send('{tab}')
    send.send('{F11}')
    send.send('y')
 ##    time.sleep(1)
    
def turn_on_iris(list_num):
    next_date = date.today() + timedelta(days=7)
    year, next_week = next_date.isocalendar()[0], next_date.isocalendar()[1]
    day_string = "%i-W%i" % (year, next_week)
    next_tuesday = datetime.strptime(day_string + '-2', "%Y-W%W-%w")
    next_tuesday = next_tuesday.strftime("%d/%m/%y")
    send = SendData()
    navigation.to_iris_online_dates(list_num)
    send.send('{enter}')
    send.send('00/00/00')
    send.send('{enter}')
    send.send(next_tuesday)
    send.send('{enter}')
    send.send('{tab}')
    send.send('{F11}')
    send.send('y')
##    time.sleep(1)

def iris_off():
    turn_off_iris('051')
    turn_off_iris('052')

def iris_on(include_NZ = None):
    turn_on_iris('051')
    if include_NZ:
        turn_on_iris('052')
