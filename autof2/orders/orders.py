from autof2.navigation import navigation
from autof2.interface.send_data import SendData
from autof2.interface import window
import time



def enter_order(date, order, pricelist='21'):
    client = order[0]['client']
    navigation.to_input_order(date, client,pricelist)
    enter_lines(order)
    print(total_order(order))


def enter_lines(order):
    send = SendData()
    window.get_window()
    for line in order:
        time.sleep(.1)
        if 'assortment_code' not in line and 'f2_code' in line:
            line['assortment_code'] = line['f2_code']
        if 'assortment_code' in line:
            window.get_window()
            print(line)
            time.sleep(.1)
            send.send('{F10}')
            send.send_exact(line['assortment_code'])
            send.send('{ENTER}')
            time.sleep(.5)
            w = window.get_window()

            if '00-00-00)' in w:
                send.send('{F11}')
                time.sleep(.1)
            send.send('{F10}')
            send.send(line['quantity'])
            send.send('{ENTER}')
            send.send('{F10}')
            if line['price'] == '':
                line['price'] = '0.00'
            send.send(line['price'])
            send.send('{ENTER}')
            time.sleep(.1)

            #input()
            check = window.get_window()
        send.send('{F11}')
        send.send('{F12}')

def total_order(order):
    total = 0
    for o in order:
        if o['price'] == '':
            o['price'] = '0.00'
        total += o['quantity'] * float(o['price'])
    return total
