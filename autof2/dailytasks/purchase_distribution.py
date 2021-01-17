from autof2.navigation import navigation
from autof2.interface.send_data import SendData
import time

def print_distribution_report(date,supplier):
    navigation.to_distribution_report(date,supplier, "laserprinter")

def run_distribution_report(date,supplier):
    navigation.to_distribution_report(date,supplier, "screen")

def pdf_email_distribution_report(date,supplier, to = "awood@fleurametz.com", title=''):
    delay = .5

    navigation.to_distribution_report(date,supplier, "pdf")
    send = SendData()
    send.send('I')
    send.send('{F10}')
    send.send(to)
    send.send('{ENTER}')
    send.send(' ')
    send.send('{DEL}')
    send.send('y ')
    send.send('{F10}')
    send.send('{F12}')
    send.send('{DOWN}')
    if not title:
        title = supplier + " " + date
    send.send(title)
    time.sleep(delay)
    send.send('{ENTER}')
    time.sleep(delay)
    send.send('{F11}')
    time.sleep(delay)
    send.send('{ENTER}')
    time.sleep(delay)
    send.send('{F11}')
    time.sleep(delay)
    send.send('y')
    time.sleep(delay)
    send.send('{ENTER}')
