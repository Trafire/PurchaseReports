from autof2.interface import send_data, window,mouse
from autof2.readf2 import parse
from autof2.navigation import navigation
from autof2.interface.send_data import SendData

##import window
##import mouse
##import clipboard
##import parse
##import navigation
import csv

import time
import win32gui
import win32con
##from send_data import SendData

def drag_window():
    win32gui.ShowWindow(window.f2_hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(window.f2_hwnd)
    c = window.get_corners(window.f2_hwnd)
    mouse.click_and_drag(c[0] +25,c[1] + 50,c[2] - 25,c[3]-50)

def get_window():
    send = SendData()
    send = SendData()
    drag_window()
    send.send('%c')
    data = None
    for i in range(3):
        try:
            data = clipboard.get_clipboard()
            break
        except:
            time.sleep(0.01)
    return data

def run_purchase_list(from_date, to_date,supplier, new = True):
    if new:
        navigation.to_purchase_list()
    drag_window()
    send = SendData()
    send.send(from_date)
    send.send('{enter}')
    send.send(to_date)
    send.send('{enter}')
    send.send('{DOWN}')
    send.send(supplier)
    send.send('{enter}')
    send.send('{F11}')
    send.send('n')
    send.send('screen')
    send.send('{enter}')

    for i in range(15):
        screen = parse.process_scene(get_window())
        if parse.identify_screen(screen,'Inkoop advies avc',1):
            return get_window()
        time.sleep(0.1)
    

def get_orders(orders = {}):
    # change string to list of string, per line
    
    screen = None
    screen = parse.process_scene(get_window())
    '''
    for i in range(10):
        try:
            screen = parse.process_scene(get_window())
        except:
            time.sleep(0.1)
        if screen:
            break
        time.sleep(0.1)
    '''
    # get supplier name
    supplier = parse.distribution_list_supplier(screen)
    if not supplier:

         return None

    # get list of orders
    if supplier not in orders:
        orders[supplier] = []
    return orders

def total_orders(orders):
    orders_totals = {}
    for o in orders:
        if (o.category, o.name, o.grade,o.colour) in orders_totals:
            orders_totals[(o.category, o.name, o.grade,o.colour)] += o.quantity
        else:
            orders_totals[(o.category, o.name, o.grade,o.colour)] = o.quantity
            print(o.quantity)
        
    return orders_totals

def get_full_report(from_date,to_date,supplier ):
    send = SendData()
    run_purchase_list(from_date, to_date,supplier)
    screen = parse.process_scene(get_window())
    o = parse.distribution_list_product(screen)
    i = 0
    print(screen[-1])
    while '< More >' in screen[-1] and i < 10:
        send.send('{enter}')
        time.sleep(0.8)
        screen = parse.process_scene(get_window())
        o.extend(parse.distribution_list_product(screen))
        i+=1
    return o

def thursday_orders(from_date,to_date,supplier):    
    orders = get_full_report(from_date, to_date,supplier)
    t = total_orders(orders)
    l = []
    for line in t:
        l.append((line, t[line]))
    l.sort()
    for line in l:
        print(line[0][0],"\t",line[0][1].strip('*'),"\t",line[0][2],"\t",line[0][3],"\t",line[1])

    return t,l, orders
    
def make_shipment_list(date = '051115', client='CAN*ON',plist = '03'):
    send = SendData()
    navigation.to_order_order(date,client,plist)
    screen = parse.process_scene(get_window())
    categories = parse.order_categories(screen)
    items = {}
    for c in categories:
        if navigation.to_order_category(c[0],c[1]):
            screen = parse.process_scene(get_window())
            ### get items
            
            items[c[1]] = parse.parse_order_category(c[1])[c[1]]
            time.sleep(.1)
            print(items[c[1]])

            
        send.send("{F12}")
    return items

def make_shipment_list_NZ(date = '051115', client='CAN*ON',plist = '03'):
    send = SendData()
    navigation.to_order_order(date,client,plist)
    time.sleep(1.5)
    screen = parse.process_scene(get_window())
    categories = parse.order_categories(screen)
    print(categories)
    items = {}
    
    for c in categories:
        if navigation.to_order_category(c[0],c[1]):
            time.sleep(.5)
            screen = parse.process_scene(get_window())
            print(screen)
            ### get items
            
            items[c[1]] = parse.parse_order_category_NZ(c[1])[c[1]]
            time.sleep(.3)
            print(items[c[1]])

            
        send.send("{F12}")
    return items

def make_virtual_shipment_list(date = '051115', client='CAN*ON',plist = '03'):
    send = SendData()
    navigation.to_order_order(date,client,plist)
    screen = parse.process_scene(get_window())
    categories = parse.order_categories(screen)
    items = {}
    for c in categories:
        if navigation.to_order_category(c[0],c[1]):
            screen = parse.process_scene(get_window())
            ### get items
            
            items[c[1]] = parse.parse_virtual_order_category(c[1])[c[1]]
##            print(items[c[1]])

            
        send.send("{F12}")
    return items


def get_groupings(grouping_loc = "D:\\BuyProg\\new\pricelist_groupings.csv"):
    groupings = {}
    with open(grouping_loc, 'r') as file:
        for line in file:
            line = line.strip()
            line = line.split(',')
            groupings[line[1]] = line[0]
    return groupings

def open_excel(from_date,to_date,supplier):
    t, a = thursday_orders(from_date,to_date,supplier)
    

        


##if __name__ == "__main__":
##    send = SendData()
##    t, a, o = thursday_orders('131215', '191215','CAROSA')
##    for i in o:
##        print(i.category,"\t", i.name,"\t", i.quantity)

