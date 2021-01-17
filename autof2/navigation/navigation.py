from autof2.readf2 import parse
from autof2.interface import window
from autof2.interface.send_data import SendData


import time

# change menues
def to_main(tries = 25):
    send = SendData()
    screen = None
    for ik in range(tries):
        time.sleep(0.1)
        for j in range(10):
            try:
                screen = parse.process_scene(window.get_window())
                break
            except:
                time.sleep(0.1)

            time.sleep(0.1)
                
        if parse.identify_screen(screen,'Main Menu'):
            send.send('{LEFT 5}')
            send.send('{UP}')
            send.send('{HOME 2}')
            return True
        send.send('{F12}')
    return False

def traverse(menu_list):
    send = SendData()
    index = 0
    time.sleep(.2)
    for m in menu_list:
        send.send('{Home}')
        num = parse.menu_nav_columns(index,m)
        if num:
            cmd = "{DOWN " + num + "}"
            send.send(cmd)
            send.send("{ENTER}")
            time.sleep(.5)
            
        index += 1
    time.sleep(.2)


def to_margeanalyse_bld(from_date, to_date, product_type, dutch = False, depth=0):
    send = SendData()
    send.activate_window()
    if depth > 5:
        exit()
    if to_main():
        time.sleep(0.2)
        menus = ('Financial', 'Margeanalyse bld')
        traverse(menus)
        send.send('CAN')
        send.send('{ENTER}')
        send.send(product_type)
        send.send('{ENTER}')
        if not verify([('Margeanalyse bld', 2, 92)]):
            return (to_margeanalyse_bld(from_date, to_date, product_type, dutch, depth + 1))
        send.send(' ')
        send.send(from_date)
        send.send('{ENTER}')
        send.send(to_date)
        send.send('{ENTER}')
        send.send('{F11}')
        send.send('{ENTER}')
        targets = [('Bedr.', 5, 5), ('Marge %', 5, 63)]
        if not wait_for_load(targets): 
            exit()
        send.send('{ENTER}')
        if dutch:
            pass
        else:
            send.send('+{F11 2}')
            targets = [('Gebied', 7, 12), ('Commissie', 7, 100)]
        if not wait_for_load(targets):
            exit()
        send.send('{HOME 3}')
        time.sleep(1)


def wait_for_load(points, depth = 0):
    while depth < 150:

        if verify_fast(points): 
            return True
        else:
            return wait_for_load(points, depth + 1)
    return False
        



def to_purchase_list():
    send = SendData()
    #send.activate_window()
    if to_main():
        time.sleep(0.2)
        menus = ('Purchase', 'Purchaselist', 'Advanced')
        traverse(menus)
        send.send('{ENTER}')
        time.sleep(.1)
        screen = parse.process_scene(window.get_window())

        if parse.identify_screen(screen, 'Advanced'):

            send.send('{UP}')
            send.send('{ENTER}')
            time.sleep(.1) 
            screen = parse.process_scene(window.get_window())
            if parse.identify_screen(screen, '√', 8):
                send.send('{UP}')
                send.send(' ')
                send.send('{ENTER}')
        else:
            return False
        time.sleep(.1)
        screen = parse.process_scene(window.get_window())
        return True  # parse.identify_sc
        
def to_order_order(date='',client='',plist = '03'):
    send = SendData()
    delay = .1

    if to_main():
        time.sleep(delay)
##        menus = ('Orders')
##        traverse(menus)
        
        send.send('{HOME}')
        time.sleep(delay)
        send.send('{ENTER}')
        time.sleep(delay)
        send.send('{HOME}')
        time.sleep(delay)
        send.send('{HOME}')
        send.send('{ENTER}')
        time.sleep(.5)
        screen = parse.process_scene(window.get_window())
        if client and date:
            if parse.identify_screen(screen,'Order'):
                send.send(client)
                send.send('{HOME}')
                send.send('{LEFT}')
                send.send(date)
                send.send('{F11}')
                send.send('{ENTER}')
                send.send('F')
                send.send('{ENTER}')
                time.sleep(delay)
                screen = parse.process_scene(window.get_window())
                if 'Create new order number' in screen[5]:
                    send.send('{HOME}')
                    send.send('{ENTER}')
                send.send(plist)
                time.sleep(delay)
    else:   
        return False


def to_standing_update(date='',to_date='',client='',plist = '03'):
    send = SendData()
    if to_main():
        time.sleep(0.02)
##        menus = ('Orders')
##        traverse(menus)
        send.send('{HOME}')
        time.sleep(0.02)
        send.send('{ENTER}')
        time.sleep(0.02)
        send.send('{HOME}')
        time.sleep(0.02)
        send.send('{HOME}')
        send.send('{ENTER}')
        time.sleep(.5)
        screen = parse.process_scene(window.get_window())
        if client and date:
            if parse.identify_screen(screen,'Order'):
                send.send(client)
                send.send('{HOME}')
                send.send('{LEFT}')
                send.send(date)
                send.send('{F11}')
                send.send('{ENTER}')
                send.send('F')
                send.send('{ENTER}')
                time.sleep(0.3)
                screen = parse.process_scene(window.get_window())
                if 'Create new order number' in screen[5]:
##                    send.send('{HOME}')
                    send.send('{ENTER}')
                send.send(plist)
                time.sleep(0.2)
                send.send('{ENTER}')
                send.send('{F5}')
                send.send('{+ 2}')
                send.send('y')
                screen = parse.process_scene(window.get_window())
                if 'Universe' in screen[4]:
                    send.send('{INSERT}')
                    send.send('{DOWN}')
                    send.send('{ENTER}')
                    send.send('{DOWN}')
                    send.send('{ENTER}')
                    send.send('{DOWN}')
                    send.send('{RIGHT}')
                    send.send(to_date)
                    send.send('{F11}')
                    send.send('{y 2}')
                    
##                send.send('{DOWN}')
##                send.send('{ENTER}')
##                ##
####                send.send(' ')
####                send.send('{RIGHT}')
####                send.send(' ')
##                ##
##                send.send('{DOWN}')
##                send.send('{ENTER}')
##                send.send('{DOWN}')
##                send.send('{ENTER}')
##                send.send(to_date)
##                send.send('{ENTER}')
####                

    else:   
        return False    

def to_order_category(cat_num, cat_name):
    send = SendData()
    send.activate_window()
    send.send(cat_num)
    for i in range(5):
        screen = parse.process_scene(window.get_window())
        if parse.identify_screen(screen, cat_name, 4):
            return True
        time.sleep(.3)
        screen = parse.process_scene(window.get_window())
    return False        

def to_virtual_stock(from_date,to_date):
    send = SendData()
    if to_main():
        time.sleep(0.02)
        menus = ('stock','Stock virtual products','Edit stock virtual')
        traverse(menus)
        send.send(from_date)
        send.send('{enter}')
        send.send(to_date)
        send.send('{f11}')
        send.send('{enter}')
        send.send('{down}')
        send.send('{enter}')
        for i in range(20):
            screen = parse.process_scene(window.get_window())
            if parse.identify_screen(screen, "Edit stock virtual Flowers", line_num=2):
                return True
            time.sleep(.1)


def to_virtual_purchase(date, depth=0):
    send = SendData()
    if to_main():
        time.sleep(0.04)
        menus = ('Purchase','Default','Insert virtual purchases')
        traverse(menus)
        time.sleep(.5)
        send.send('{enter}')
        send.send(date)
        send.send('{enter}')
        for i in range(10):
            screen = parse.process_scene(window.get_window())
            if parse.identify_screen(screen, "Insert virtual purchases Flowers", line_num=2):
                return True
            time.sleep(.1)
        if depth < 3:
            to_virtual_purchase(date, depth = depth + 1)


def to_menu(command_order):
    send = SendData()
    if to_main():
        time.sleep(0.05)
        traverse(command_order)
        time.sleep(0.05)

def to_menu_slow(command_order):
    send = SendData()
    if to_main():
        time.sleep(0.2)
        print(command_order)
        traverse(command_order)
        time.sleep(0.2)

def to_menu_slowest(command_order, verbose=False):
    send = SendData()
    if to_main():
        send.send("{HOME}")
        time.sleep(1)
        if verbose:
            print(command_order)
        traverse(command_order)
        time.sleep(1)
    return True

def to_menu_parsed(command_order):
    ''' (tuple of str)=> bool
         Navigate main menu to desired window
         returns True if successful, False if not
    
    '''
    send = SendData()
    if to_main():
        time.sleep(0.02)
        col = 1
        for c in command_order:
            row = parse.main_menu_row(col,c)
            if not row:
                return False
            else:
##                print("{DOWN %s}" % row)
                send.send("{DOWN %s}" % row)
                send.send('{enter}')
                time.sleep(1)
            
            col += 1
    screen = parse.process_scene(window.get_window())
    return parse.identify_screen(screen,command_order[-1])
    
            
        


    
def to_distribution_report(date,supplier, printer = "laserprinter"):
    delay = .8
    if to_main():
        to_main() 
        delay = .8
        to_main()
        send = SendData()
        command_order = ('Purchase','Purchase details (suppl)','Without distribution')
        to_menu(command_order)
        time.sleep(delay)
        send.send('{enter}')
        time.sleep(delay)
        send.send(date)
        send.send('{enter}')
        time.sleep(delay)
        send.send(date)
        send.send('{enter}')
        send.send(supplier)
        send.send('{enter}')
        send.send(printer)
        send.send('{enter}')

def to_pricelist_type(list_num):
    ''' (str)->None
    goes to list number in price

    '''
    send = SendData()
    to_menu(('Maintenance data','Pricelists','Pricelist type'))
    send.send('{home}')
    time.sleep(0.5)
    send.send('{enter}')
    send.send(list_num)
    send.send('{f12}')


def to_purchase(date):
    ''' (None)->None
    goes to Assortment Menu
    '''

    match = False
    wait = .01
    for i in range(2):
        send = SendData()
        # to_menu(('Maintenance data','Assor'))
        # hack
        to_main()
        send.send('Purchase')
        send.send('{enter}')
        time.sleep(wait)
        send.send('{HOME}')
        send.send('{enter}')

        send.send('{home}')
        time.sleep(wait)
        send.send('{enter}')
        time.sleep(wait)
        send.send('{home}')
        time.sleep(wait)
        send.send('{enter}')
        time.sleep(wait)
        send.send(date)
        time.sleep(wait)
        send.send('{F11}')

        screen = parse.process_scene(window.get_window())
        if parse.identify_screen(screen, 'Purchase/distribute Flowers'):
            return True
    return match

def to_assortment():
    ''' (None)->None
    goes to Assortment Menu 
    '''

    match = False
    for i in range(2):
        send = SendData()
        #to_menu(('Maintenance data','Assor'))
        # hack
        to_main()
        send.send('Maintenance data')
        send.send('{enter}')
        time.sleep(0.5)
        send.send('{DOWN} 4')
        send.send('{enter}')
        
        send.send('{home}')
        time.sleep(0.5)
        send.send('{enter}')
        time.sleep(0.5)
        screen = parse.process_scene(window.get_window())
        if parse.identify_screen(screen,'Assortment Flowers'):
            return True
    return match

def to_assortment_category(category):
    target = ' ' + category + ' '
    send = SendData()
    to_assortment()
    time.sleep(.5)
    old_screen = window.get_window()
    while category.lower() not in old_screen.lower():
        send.send('{PGDN}')
        time.sleep(0.5)
        if old_screen == window.get_window():
            return None
        old_screen = window.get_window()
    index = old_screen.index(target)
    category_number = old_screen[index - 3: index].strip('║')
    send.send(category_number)
    send.send('{enter}')
    send.send('+{F11}') 
    time.sleep(.5)
    return True


def to_purchase_category(category, date):
    target = ' ' + category + ' '
    send = SendData()
    to_purchase(date)
    time.sleep(.5)
    old_screen = window.get_window()
    while category.lower() not in old_screen.lower():
        send.send('{PGDN}')
        time.sleep(0.5)
        if old_screen == window.get_window():
            return None
        old_screen = window.get_window()
    index = old_screen.index(target)
    category_number = old_screen[index - 3: index].strip('║')
    send.send(category_number)
    send.send('{enter}')
    send.send('+{F11}')
    time.sleep(.5)
    for i in range(10):
        send.send('+{F11}')
        send.send('{HOME 4}')
        time.sleep(1)
        if 'everything' in window.get_window().lower():
            break
    return True



def to_orderstatus(date):
    if to_main():
        
        send = SendData()
        index = 0
        while not to_menu_slowest(['Sales','Orderstatus Sales']):
            time.sleep(.3)
            index += 1
            if index > 3:
                exit()
        send.send(date)
        send.send('{ENTER}')


def to_orderstatus_range(date):
    if to_main():

        send = SendData()
        index = 0
        while not to_menu_slowest(['Sales', 'Orderstatus sales (f/t)']):
            time.sleep(.3)
            index += 1
            if index > 3:
                exit()
        send.send(date)
        send.send('{ENTER}')


def get_order_status_orders(date, company="CAN"):
    to_orderstatus_range(date)
    send = SendData()
    send.send("{F9}")
    send.send(company)
    send.send("{enter}")






def to_order(date, ordernumber, go_to_menu=True):
    send = SendData()
    if go_to_menu:
        to_orderstatus(date)
    else:
        send.send('{HOME 5}')
    found = False
    time.sleep(.5)
    while not found:
        index = 0
        
        screen = parse.process_scene(window.get_window())[6:-6]
        for line in screen:
            if ordernumber in line:
                found = True
                send.send('{DOWN %s}' % index)
                send.send('{ENTER}')
                return True
            index += 1
            
        if not found:
            send.send('{PGDN}')
            time.sleep(.5)
            next_screen = parse.process_scene(window.get_window())[6:-6]
            if next_screen == screen:
                return False

def get_order(date, ordernumber, go_to_menu=True):
    to_order(date, ordernumber,go_to_menu)
    send = SendData()
    time.sleep(.3)
    index = 0
    if 'Debet' in parse.process_scene(window.get_window())[8]:
        return []
    while 'Everything' not in parse.process_scene(window.get_window())[7]:
        if index > 10:
            exit()
        time.sleep(.3)
        if 'Everything' not in parse.process_scene(window.get_window())[7]:
            send.send('+{F11}')
        index += 1

    send.send('{END 5}')
    time.sleep(.5)
    screen = parse.process_scene(window.get_window())[8:-4]
    screen.reverse()
    for line in screen:
        if line[1:6].strip():
            last_num = int(line[1:6].strip())
            break
    send.send('{HOME 5}')
    time.sleep(.5)
    items = []
    
    
    pages = last_num // 23
    if last_num != 23:
        pages += 1
    for i in range(pages):
        screen = parse.process_scene(window.get_window())[8:-4]
        for line in screen:
            try:
                if line[1:6].strip():
                    items.append({})
                    items[-1]['status_title'] = line[18:18+24].strip()
                    q = line[18+25:18+25+10]
                    q = q.strip().split('x')
                    
                    items[-1]['quantity'] = int(q[0]) * int(q[1])
                    price = line[18+25+10 + 13: 18+25+10 + 13 + 6].replace(',','.').strip()
                    items[-1]['price'] = price
            except:
                print(line)

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
            if "║" not in assortment_code:
                break
            else:
                time.sleep(.1)

        items[i]['assortment_code'] = assortment_code
        send.send('{ENTER}')
        send.send('{F12}')
        send.send('{DOWN}')
        time.sleep(.05)
        
        
    send.send('{F12}')    
    return items

def get_order_no_nav(date, ordernumber, go_to_menu=True):
    send = SendData()
    index = 0
    if 'Debet' in parse.process_scene(window.get_window())[8]:
        return []
    while 'Everything' not in parse.process_scene(window.get_window())[7]:
        if index > 10:
            exit()
        time.sleep(.3)
        if 'Everything' not in parse.process_scene(window.get_window())[7]:
            send.send('+{F11}')
        index += 1

    send.send('{END 5}')
    time.sleep(.5)
    screen = parse.process_scene(window.get_window())[8:-4]
    screen.reverse()
    for line in screen:
        if line[1:6].strip():
            last_num = int(line[1:6].strip())
            break
    send.send('{HOME 5}')
    time.sleep(.5)
    items = []

    pages = last_num // 23
    if last_num != 23:
        pages += 1
    for i in range(pages):
        screen = parse.process_scene(window.get_window())[8:-4]
        for line in screen:
            try:
                if line[1:6].strip():
                    items.append({})
                    items[-1]['status_title'] = line[18:18 + 24].strip()
                    q = line[18 + 25:18 + 25 + 10]
                    q = q.strip().split('x')

                    items[-1]['quantity'] = int(q[0]) * int(q[1])
                    price = line[18 + 25 + 10 + 13: 18 + 25 + 10 + 13 + 6].replace(',', '.').strip()
                    items[-1]['price'] = price
            except:
                print(line)

        send.send('{PGDN}')
        time.sleep(.5)

    send.send('{HOME 5}')
    time.sleep(.5)

    for i in range(last_num):
        send.send('+{F10}')
        send.send('{ENTER}')
        time.sleep(.3)
        assortment_code = parse.process_scene(window.get_window())[9][-13:-1].strip()
        items[i]['assortment_code'] = assortment_code
        send.send('{ENTER}')
        send.send('{F12}')
        send.send('{DOWN}')

    send.send('{F12}')
    return items
def to_iris_online_dates(list_num):
    send = SendData()
    to_pricelist_type(list_num)
    send.send('{f4}')
    send.send('{tab}')

def to_input_purchase(date):
    match = False
    for i in range(20):
        send = SendData()
        send.activate_window()
        to_menu(('Purchase', 'Default', 'Input purchases'))
        send.send('{home}')
        time.sleep(0.5)
        send.send('{enter}')
        send.send(date)
        send.send('{enter}')
        time.sleep(0.5)
        screen = parse.process_scene(window.get_window())
        if parse.identify_screen(screen, 'Input purchases Flowers'):
            screen = parse.process_scene(window.get_window())
            match = True
            if 'Article' not in screen[-6]:
                send = SendData()
                send.send('{INSERT}')
            break

    return match

def to_insert_virtual_purchases(date, delay = .5):
    match = False

    for i in range(20):
        send = SendData()
        send.activate_window()
        to_menu(('Purchase','Default','Insert virtual purchases'))
        send.send('{home}')
        time.sleep(delay)
        send.send('{enter}')
        send.send(date)
        send.send('{enter}')
        time.sleep(delay)
        time.sleep(.8)
        screen = parse.process_scene(window.get_window())
        #input("break")
        time.sleep(.8)
        send.activate_window()
        screen = parse.process_scene(window.get_window())
        if parse.identify_screen(screen,'Insert virtual purchases Flowers'):
            screen = parse.process_scene(window.get_window())
            match = True
            print(screen[-6])
            #input("break")
            time.sleep(.8)
            send.activate_window()
            if 'Article' not in screen[-6]:
                send = SendData()
                send.send('{INSERT}')
            break
    return match

def to_pricelist(pricelist_num, date=''):
    match = False
    for i in range(2):
        send = SendData()
        to_menu_parsed(('Maintenance data','Pricelists','Edit pricelist'))
        time.sleep(0.5)
        send.send('{home}')
        time.sleep(0.5)
        send.send('{enter}')
        time.sleep(0.5)
        screen = parse.process_scene(window.get_window())
        if parse.identify_screen(screen,'Edit pricelist Flowers'):
            match = True
            time.sleep(0.1)
            if date:
                send.send('+3')
                send.send(date)
                
                #send.send('{enter}')
            
            send.send(pricelist_num)
            time.sleep(0.1)

##            send.send('{enter}')
            
            break
        
    return match


def to_input_purchase_insert(date):
    send = SendData()
    to_menu(('Purchase', 'Default', 'Input purchases'))
    send.send('{home}')
    time.sleep(0.5)
    send.send('{enter}')
    print(date)
    send.send(date)
    send.send('{enter}')
    points = [('Input purchases Flowers', 2, 92),
              ('Article', 29, 4), ('Buyer  :', 29, 59),
              ('Available', 21, 54), ('Bought for  :', 30, 4)]
    time.sleep(.1)
    if not verify(points):
        send.send('{insert}')
    time.sleep(.2)
    if not verify(points):
        to_input_purchase_insert(date)

def to_input_purchase_ps_insert(date):
    send = SendData()
    to_menu(('Purchase', 'Per shipment', 'Input purchases (PS)'))
    send.send('{home}')
    time.sleep(0.5)
    send.send('{enter}')
    send.send(date)
    send.send('{enter}')
    # points = [('Input purchases Flowers', 2, 92),
    #           ('Article', 29, 4), ('Buyer  :', 29, 59),
    #           ('Available', 21, 54), ('Bought for  :', 30, 4)]
    # time.sleep(.1)
    # if not verify(points):
    #     send.send('{insert}')
    # time.sleep(.2)
    # if not verify(points):
    #     to_input_purchase_insert(date)

def to_input_purchase_mix_insert(date):
    send = SendData()
    points = [('Input purchase mixbox Flowers', 2, 92), ('Inkoopdatum', 4, 2), ('Zendingnr', 6, 19)]
    index = 0
    to_main()
    while not verify(points):
        to_menu(('Purchase', 'Per shipment', 'Input purchase mixbox'))
        send.send('{home}')
        time.sleep(1)
        send.send('{enter}')
        send.send(date)
        send.send('{enter}')
        if not verify([('Airbill', 6, 5)]):
            send.send('{F11}')
        time.sleep(1)
        if index > 10:
            return False
        index += 9
    return True

def verify(points):

    time.sleep(1)
    screen = parse.process_scene(window.get_window())
    for p in points:
        if not p[0] in screen[p[1]][p[2]:]:
            return False
    return True
def verify_fast(points):

    time.sleep(.05)
    screen = parse.process_scene(window.get_window())
    for p in points:
        try:
            if not p[0] in screen[p[1]][p[2]:]:
                return False
        except:
            verify_fast(points)
    return True

def to_input_order(date, client, list=21):
    send = SendData()
    delay = .15
    points = [('Article :', 19, 4), ('n/a', 4, 2), ('Client :', 4, 24)]
    index = 0
    commands = ['{LEFT}', date, '{ENTER}', client, '{ENTER}', '{F11}', '{HOME}', '{ENTER}', list, '{ENTER}']
    to_main()
    while not verify(points):
        to_main()
        to_menu(('Orders', 'Input order'))
        for c in commands:
            if c == '{HOME}':
                if verify([('Client information', 6, 4)]):
                    send.send('{F12}')
            if c == list:
                time.sleep(delay)
                if verify([('Create new order number', 5, 21)]):
                    time.sleep(delay)
                    send.send('{HOME}')
                    time.sleep(delay)
                    send.send('{ENTER}')
                    time.sleep(delay)
            time.sleep(delay)
            send.send(c)
            time.sleep(delay)
        if index > 10:
            return False
        index += 1


def get_window_info(targets):
    total = []
    w = parse.process_scene(window.get_window())

    for target in (targets):
        i = 0
        for line in w:
            if target in line:
                total.append((target, i, line.index(target)))
            i += 1

    print(total)

def get_purchase_orders(date):
    send = SendData()
    if to_main():

        index = 0
        retries = 2
        points = [('Orderstatus purchase', 2, 92), ('Date :', 4, 2)]
        while not verify(points):
            index += 1
            to_main()
            to_menu(('Purchase', 'Orderstatus purchase'))
            send.send(date)
            send.send('{ENTER}')
            send.send('y')
            time.sleep(0.5)

            if index > retries:
                return False
        ### END FUTURE WHILE loop
        i = []
        old_screen = ''
        index = 0
        points = [('ALL', 4, 63)]
        while not verify(points):
            send.send('+{F11}')
            if index > retries:
                return False
            index += 1
        send.send('{HOME 3}')
        time.sleep(.5)
        while True:

            invoices = parse.process_scene(window.get_window())[6:29]
            if old_screen == invoices:
                return i
            for line in invoices:
                supplier = line[1:7].strip()
                order_num = line[20:28].strip()
                stems = line[49:55].strip()
                price = line[72:81].strip()
                if ',' in price:
                    price = price.replace(',','.')
                shipment = line[82:94].strip()
                invoice_num = line[95:107].strip()
                data = {'stems':stems, 'order_num': order_num,
                          'supplier':supplier, 'price':price,'shipment':shipment,
                          'invoice_num':invoice_num, 'date': date}
                if data not in i and data['stems'] != '':
                    i.append(data)
            time.sleep(.1)
            send.send('{PGDN}')
            time.sleep(.5)
            old_screen = invoices

        return i
    
def activate_window():
    window.get_window()


def switch_F2(target_system):
    send = SendData()
    send.activate_window()
    if target_system == "FleuraMetz Toronto":
        points = [('FleuraMetz Toronto', 1, 92)]
        if verify_fast(points):
            return True
        else:
            to_main()
            send.send("{F12}")
            send.send("y")
            time.sleep(2)
            send.send("07")
            time.sleep(2)
            send.send("1")
            time.sleep(1)
    elif target_system == "F2-NL":
        points = [('F2-NL', 1, 92)]
        if verify_fast(points):
            return True
        else:
            to_main()
            send.send("{F12}")
            send.send("y")
            time.sleep(.5)
            send.send("{F12}")
            time.sleep(.5)
            send.send("01")
            time.sleep(.5)


#get_window_info(("ALL",))


#print(len(get_purchase_orders('27/05/18')))
#get_purchase_orders('27/05/18')
#get_window_info(['mirsweet0','0,56 ','1x','25(','CAROPR'])

#to_input_order('01/01/18', 'CAN*ON')
##if __name__ == '__main__':
##    
##    date = '13/11/17'
####    a = get_order(date,'358627')
##    b = get_order(date,'354391', False)
##
##    
##    end_date = '31/12/17'
##    client = 'CN*GRO'
####    to_standing_update(date,end_date,client,'11')
    


##        
##to_pricelist('052', '07/08/17')
####        
####client = 'FENDLA'        
##date = '24/07/17'
##to_date = '31/10/17'
##
##send = SendData()
##
##to_standing_update(date=date, to_date= to_date, client=client, plist='11')
##send.send('{enter}')
#to_input_order('09/01/18', 'ROCKWO', 21)
#print(get_order("01/10/18", "409882", go_to_menu=True))

