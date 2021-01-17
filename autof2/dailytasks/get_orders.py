from autof2.navigation import navigation
from autof2.readf2 import parse
from autof2.interface import window
from autof2.readf2 import dates
from autof2.interface.send_data import SendData
import json
import time
from datetime import datetime

def get_order_num():
    w = window.get_window()
    p = parse.process_scene(w)
    order_info_row = p[6]
    return order_info_row[20:27].strip()

def create_order():
    w = window.get_window()
    p = parse.process_scene(w)
    order_info_row = p[6]
    client_name = order_info_row[1:7].strip()
    invoice_num = order_info_row[12:19].strip()
    order_num = order_info_row[20:27].strip()
    order_date = dates.f2_to_datetime(order_info_row[35:43])
    return {'client_name': client_name,'invoice_num': invoice_num,'order_num': order_num,'order_date': order_date}


def create_order_lines():
    if 'Debet' in parse.process_scene(window.get_window())[8]:
        return []
    if 'Password' in parse.process_scene(window.get_window())[-3]:
        return []
    cur_window = parse.process_scene(window.get_window())

    while 'Everything' not in cur_window[7]:
        if "Art. info" in cur_window[5]:
            send.send("{F12}")
            time.sleep(.05)
        elif 'Everything' not in cur_window[7]:
            send.send('+{F11}')
            send.send('{HOME}')
            time.sleep(.05)
        time.sleep(.05)
        cur_window = parse.process_scene(window.get_window())
    send.send("{LEFT 12}")
    send.send("{RIGHT 10}")
    # get order _number
    order_num = get_order_num()
    ### get total number of rows
    send.send('{END 5}')  # got to end of page
    time.sleep(.5)
    screen = parse.process_scene(window.get_window())[8:-4]
    screen.reverse()
    for line in screen:
        if line[1:6].strip():
            last_num = int(line[1:6].strip())
            break

    #### start making list
    send.send('{HOME 5}')  # back to top of page
    time.sleep(.05)
    items = []
    lines_per_page = 23
    pages = last_num // lines_per_page
    if last_num != lines_per_page:
        pages += 1
    for i in range(pages):
        screen = parse.process_scene(window.get_window())[8:-4]
        for line in screen:

            if line[1:6].strip() and "-(C)" not in line:
                items.append({})
                salesperson = line[-8:-1].strip()
                entry_date = dates.convert_to_datetime(line[-20:-10] + " " + line[-30:-22], '%d-%m-%Y %H:%M:%S')
                canceled = line[21] == 'a'

                items[-1]['salesperson'] = salesperson
                items[-1]['entry_date'] = entry_date
                items[-1]['canceled'] = canceled

                items[-1]['status_title'] = line[17:18 + 24].strip()
                q = line[18 + 25:18 + 25 + 10]
                q = q.strip().split('x')
                try:
                    items[-1]['quantity'] = int(q[0]) * int(q[1])
                except(ValueError):
                    if line[18 + 25:18 + 25 + 10] == 'Not order.':
                        items[-1]['quantity'] = 0
                    else:
                        items[-1]['quantity'] = 999
                delivered = line[28 + 25:18 + 25 + 10]
                try:
                    delivered = delivered.strip().split('x')
                    delivered = int(delivered[0]) * int(delivered[1])
                except:
                    delivered = 0
                items[-1]['delivered'] = delivered
                price = line[18 + 25 + 10 + 13: 18 + 25 + 10 + 13 + 6].replace(',', '.').strip()
                items[-1]['price'] = price
            elif "-(C)" in line:
                last_num -= 1
        send.send('{PGDN}')
        time.sleep(.5)

    send.send('{HOME 5}')
    time.sleep(.5)

    for i in range(last_num):
        send.send('+{F10}')
        send.send('{ENTER}')
        time.sleep(.3)
        for j in range(20):
            assortment_code = parse.process_scene(window.get_window())[9][-13:-1].strip()
            status_title = parse.process_scene(window.get_window())[6][-35:-1].strip()
            supplier = parse.process_scene(window.get_window())[11][-30:-23].strip()
            if "║" not in assortment_code:
                break
            else:
                time.sleep(.1)

        items[i]['assortment_code'] = assortment_code
        items[i]['supplier'] = supplier
        items[i]['order_num'] = order_num
        send.send('{ENTER}')
        send.send('{F12}')
        send.send('{DOWN}')
        time.sleep(.05)
    return items

def datetimeconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
def jsonify(data,pretty=False):
    if pretty:
        return json.dumps(data, default=datetimeconverter,sort_keys=True,indent=4, separators=(',', ': '))
    return json.dumps(data, default=datetimeconverter)

def get_orders(date):
    send = SendData()
    navigation.get_order_status_orders(date)
    send.send("{UP}{ENTER}")
    time.sleep(1)
    orders = []
    order_nums = []
    while True:
        order = create_order()
        order_num = order['order_num']
        if order_num in order_nums:
            # verify duplicate
            time.sleep(1)
            order = create_order()
            order_num = order['order_num']
            print(order_nums)
            if order_num in order_nums:
                print("doublicate")
                break
            else:
                order_nums.append(order_num)
        else:
            order_nums.append(order_num)
        if str(order['invoice_num']) == "0":
            try:
                lines = create_order_lines()
            except:
                send.send("{LEFT 10}")
                time.sleep(1)
                lines = create_order_lines()
        else:
            lines = []
        orders.append({'order_info':order, 'order_lines': lines})
        send.send('{f12}{DOWN}{ENTER}')
        time.sleep(.5)
    return jsonify(orders)
send = SendData()
