import time
from autof2.interface.send_data import SendData
from autof2.interface import window


##from autof2.navigation import navigation

class Order:
    def __init__(self, category, name, grade, colour, client, quantity, supplier, comment=''):
        self.supplier = supplier.strip().replace('╚', '').replace('═', '').replace('╝', '').replace('╝', '').replace(
            '╠', '').replace('╣', '')
        self.category = category.strip().replace('╚', '').replace('═', '').replace('╝', '').replace('╝', '').replace(
            '╠', '').replace('╣', '')
        self.name = name.strip().replace('╚', '').replace('═', '').replace('╝', '').replace('╝', '').replace('╠',
                                                                                                             '').replace(
            '╣', '')
        self.colour = colour.strip().replace('╚', '').replace('═', '').replace('╝', '').replace('╝', '').replace('╠',
                                                                                                                 '').replace(
            '╣', '')
        self.grade = grade.strip().replace('╚', '').replace('═', '').replace('╝', '').replace('╝', '').replace('╠',
                                                                                                               '').replace(
            '╣', '')
        self.client = client.strip().strip('!').replace('╚', '').replace('═', '').replace('╝', '').replace('╝',
                                                                                                           '').replace(
            '╠', '').replace('╣', '')
        if '/' in quantity:
            quantity = '26'
        self.quantity = int(quantity.strip())
        self.comment = comment.strip()
        self.standing = client[0].strip() == '!'
        self.date = ''
        self.key = self.category + self.name + self.colour + self.grade + self.supplier

    def __str__(self):
        return "%s %s %s %s %s %s " % (self.category, self.name, self.grade, self.colour,
                                       self.client, self.quantity)

    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        return (self.category, self.name, self.colour, self.grade) == (
            other.category, other.name, other.colour, other.grade)

    def __lt__(self, other):
        return self.key < other.key

    def tupple(self):
        return (self.category, self.name, self.grade, self.colour,
                self.client, self.quantity)

    def excel_heading(self):
        return (
            "OrderID", "Category", "Variety", "Colour", "Grade", "Client", "Date", "Quantity", "Supplier", "Standing",
            "Comment")

    def excel_data(self):
        return (self.key, self.category, self.name, self.colour, self.grade, self.client, self.date, self.quantity,
                self.supplier, str(self.standing), self.comment)

    def excel_order_headings(self):
        return ("PurchaseID", "f2_supplier", "Category", "Variety", "Colour", "Grade", "Supplier", "Price", "Ordered",
                "Confirmed")

    def excel_order_data(self):
        return (self.key, self.supplier, self.category, self.name, self.colour, self.grade, '', 0, 0, 0)

    def excel_order_dict_vers(self):
        return {"PurchaseID": self.key,
                "f2_supplier": self.supplier,
                "Category": self.category,
                "Variety": self.name,
                "Colour": self.colour,
                "Grade": self.grade,
                "Supplier": '',
                "Price": 0,
                "Ordered": self.quantity,
                "Confirmed": 0,
                }
    def all_data(self):
        headings = self.excel_heading()
        data = self.excel_data()
        d = {}
        
        for index in range(len(headings)):
            d[headings[index]] = data[index]
        return d

# distribution list
def distribution_list_supplier(screen):
    ''' (list of str) -> str
    '''
    for i in range(20):
        try:
            line = screen[1]
            target = 'Inkoop advies avc'
            line = line[line.index(target) + len(target):].strip()
            line = line[:line.index(' ')].strip()
            break
        except:
            screen = process_scene(window.get_window())
            time.sleep(.1)
    return line


# main menu
def identify_screen(screen, target, line_num=2):
    for w in range(20):
        try:
            line = screen[line_num]
            # print(line)
            if target in screen[line_num]:
                return True
            break
        except:
            screen = process_scene(window.get_window())
            time.sleep(.1)
    return False


# helper functions
def process_scene(uscreen):
    for j in range(10):
        try:
            return uscreen.split('\r\n')
        except:
            uscreen = window.get_window()
    return None


def distribution_list_product(screen):
    supplier = distribution_list_supplier(screen)
    orders = []
    category = None
    grade = None

    for line in screen:
        if (line[0:4] == '    ' and line[4] != ' ') or (line[0:3] == '   ' and line[4] != ' '):
            category = line.strip()

        if category:
            if line[0] not in (' ', '═', '╚'):
                name = line[0:30].strip().strip('═')
                grade = line[31:35].strip().strip('═')
                colour = line[35:40].strip().strip('═')

                if len(line) >= 91:
                    quantity = line[80:85].strip().strip('═')
                    client = line[85:95].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
                if len(line) >= 103:
                    quantity = line[95:103].strip().strip('═')
                    client = line[103:113].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
                if len(line) >= 131:
                    quantity = line[113:121].strip().strip('═')
                    client = line[121:131].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))




            elif line[1] == '>':
                client = line[7:15].strip().strip('═')
                for o in orders:

                    if (o.client, o.category, o.name, o.grade, o.client, str(o.quantity), o.supplier) == (
                            client, category, name.strip('!'), grade, client, str(quantity), supplier):
                        o.comment += line[15:].strip().strip('═')
            elif line[0] not in ('═', '╚') and line[:5] != ' Till' and line[1] != ' ':
                name = line[0:30].strip().strip('═')
                grade = line[31:35].strip().strip('═')
                colour = line[35:40].strip().strip('═')

                if len(line) >= 95:
                    quantity = line[80:85].strip().strip('═')
                    client = line[85:95].strip().strip('═')
                    if client != '':
                        ##                        print(line)
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
                if len(line) >= 103:
                    quantity = line[95:103].strip().strip('═')
                    client = line[103:113].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
                if len(line) >= 131:
                    quantity = line[113:121].strip().strip('═')
                    client = line[121:131].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))



            elif line[:67].strip().isdigit():
                if len(line) >= 80:
                    quantity = line[:67].strip().strip('═')
                    client = line[68:80].strip().strip('═')
                    if client != '':
                        ##                        print(category, name,grade,client,quantity,supplier)
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))

                if len(line) >= 95:
                    quantity = line[80:85].strip().strip('═')
                    client = line[85:95].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
                if len(line) >= 103:
                    quantity = line[95:103].strip().strip('═')
                    client = line[103:113].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
                if len(line) >= 131:
                    quantity = line[113:121].strip().strip('═')
                    client = line[121:131].strip().strip('═')
                    if client != '':
                        orders.append(Order(category, name, grade, colour, client, quantity, supplier))
    return orders


def order_categories(screen):
    categories = []
    line_num = 6
    while line_num < 30 and "═" not in screen[line_num]:

        if screen[line_num][1] == ' ':
            start = 1
        else:
            start = 0

        line = screen[line_num][start:]
        while True:
            try:
                start = line.index('║') + 1
                line = line[start:]
                end = line.index('║')

                c = line[:end]
                if c.isspace() or c.strip() == '':
                    break

                cat_num = c[:3].strip()
                cat_name = c[3:].strip()
                categories.append((cat_num, cat_name))
                ##                print(cat_num + " , " + cat_name)
                line = line[end:]
            except:
                break
        line_num += 1

    categories.sort()
    return categories


def pricelist_categories(screen):
    categories = []
    line_num = 8
    while line_num < 30 and "═" not in screen[line_num]:

        if screen[line_num][1] == ' ':
            start = 1
        else:
            start = 0

        line = screen[line_num][start:]
        while True:
            try:
                start = line.index('║') + 1
                line = line[start:]
                end = line.index('║')

                c = line[:end]
                if c.isspace() or c.strip() == '':
                    break

                cat_num = c[:3].strip()
                cat_name = c[3:].strip()
                categories.append((cat_num, cat_name))
                ##                print(cat_num + " , " + cat_name)
                line = line[end:]
            except:
                break
        line_num += 1

    categories.sort()
    return categories


def parse_order_category(cat_name):
    items = []
    send = SendData()
    while True:
        screen = process_scene(window.get_window())
        to_process = screen[6:]
        for line in to_process:
            if '═' in line:
                break
            line = line[4:]
            l = line.split('║')
            if l[0].isspace():
                break
            else:
                if 'x' in line:
                    quantity = l[7][:l[7].index('x')]
                    price = l[9].replace(',', '.').strip('■').strip('▲').strip('█').strip('▼')
                    items.append((l[0].strip(), l[1].strip(), l[2].strip(), quantity.strip(), price.strip()))

        send.send('{PGDN}')
        time.sleep(0.1)
        new_screen = process_scene(window.get_window())
        if new_screen == screen:
            time.sleep(0.3)
            new_screen = process_scene(window.get_window())
            if new_screen == screen:
                break
    return {cat_name: items}


def parse_price_list_category(cat_name):
    items = []
    send = SendData()
    while True:
        screen = process_scene(window.get_window())
        to_process = screen[6:]
        for line in to_process:
            if '═' in line:
                break
            line = line[4:]
            l = line.split('║')
            if l[0].isspace():
                break
            else:
                if 'x' in line:
                    print(l)
                    quantity = l[7][:l[7].index('x')]
                    price = l[9].replace(',', '.').strip('■').strip('▲').strip('█').strip('▼')
                    print(price)
                    items.append((l[0].strip(), l[1].strip(), l[2].strip(), quantity.strip(), price.strip()))

        send.send('{PGDN}')
        time.sleep(0.1)
        new_screen = process_scene(window.get_window())
        if new_screen == screen:
            time.sleep(0.1)
            new_screen = process_scene(window.get_window())
            if new_screen == screen:
                break
    return {cat_name: items}


def parse_order_category_NZ(cat_name):
    items = []

    send = SendData()

    while True:
        screen = process_scene(window.get_window())

        to_process = screen[6:]

        for line in to_process:

            if '═' in line:
                break

            line = line[4:]

            l = line.split('║')

            if l[0].isspace():

                break

            else:

                quantity = l[7][:l[7].index('x')]

                price = l[9].replace(',', '.').strip('■').strip('▲').strip('█').strip('▼')

                print(price)

                items.append((l[0].strip(), l[1].strip(), l[2].strip(), l[3].strip(), l[4].strip(), quantity.strip(),
                              price.strip()))

        send.send('{PGDN}')

        time.sleep(0.5)

        new_screen = process_scene(window.get_window())

        if new_screen == screen:

            time.sleep(0.1)

            new_screen = process_scene(window.get_window())

            if new_screen == screen:
                break

    return {cat_name: items}


def parse_virtual_order_category(cat_name):
    items = []
    send = SendData()
    time.sleep(0.2)
    while True:
        time.sleep(0.1)
        screen = process_scene(window.get_window())
        to_process = screen[6:]
        for line in to_process:
            if '═' in line:
                break
            line = line[4:]
            l = line.split('║')

            if l[0].isspace():
                print(cat_name, l)
                break
            else:
                quantity = l[7][:l[7].index('x')]
                packing = l[7][l[7].index('x') + 1:].strip()
                ##                print(packing)
                price = l[9].replace(',', '.').strip('■').strip('▲').strip('█').strip('▼')
                ##                print(price)
                items.append((l[0].strip(), l[1].strip(), l[2].strip(), quantity.strip(), price.strip(), packing))

        time.sleep(0.2)
        send.send('{PGDN}')
        time.sleep(0.2)
        print("next")
        new_screen = process_scene(window.get_window())
        if new_screen == screen:
            time.sleep(0.5)
            new_screen = process_scene(window.get_window())
            if new_screen == screen:
                break

    return {cat_name: items}


def parse_assortment_category_section(cat_name, max_pages=30):
    send = SendData()
    send.send('{home}{home}')
    screen = process_scene(window.get_window())
    old_screen = screen
    items = []

    for count in range(max_pages):
        to_process = screen[6:]
        seperated = []
        good_list = []

        for line in to_process:
            seperated.append(line.split('║'))
        for line in seperated:
            if '═' in line[0]:
                break
            if line[1].strip() != '':
                good_list.append(line)
        ##        for line in good_list[2:]:
        ##            send.send('{DOWN}')

        for line in good_list:
            send.send(line[1])
            time.sleep(.15)
            screen = process_scene(window.get_window())
            code = screen[-2][63:82].strip()
            name = line[2][:-4].strip()
            name = name[len(cat_name):].strip()
            colour = line[5].strip()
            length = line[6].strip()
            quality = line[7].strip()
            packing = int(line[8].strip())
            new_item = (code, cat_name, name, colour, length, quality, packing)
            if new_item in items:
                return items

            items.append(new_item)

        ##            print((code,cat_name,name,colour,length,quality,packing))
        send.send('{PGDN}')
        send.send('{home}')
        time.sleep(.3)
        new_screen = process_scene(window.get_window())
        screen = new_screen
        if new_screen[6:] == old_screen[6:]:
            break
        old_screen = new_screen

    return items


def parse_assortment_category_section_dict(cat_name, max_pages=30):
    send = SendData()
    send.send('{home}{home}')
    time.sleep(.01)
    screen = process_scene(window.get_window())
    old_screen = screen
    items = []

    for count in range(max_pages):
        to_process = screen[6:]
        seperated = []
        good_list = []

        for line in to_process:
            seperated.append(line.split('║'))
        for line in seperated:
            if '═' in line[0]:
                break
            if line[1].strip() != '':
                good_list.append(line)
        ##        for line in good_list[2:]:
        ##            send.send('{DOWN}')

        for line in good_list:
            send.send(line[1])
            time.sleep(.15)
            screen = process_scene(window.get_window())
            code = screen[-2][63:82].strip()
            name = line[2][:-4].strip()
            name = name[len(cat_name):].strip()
            colour = line[5].strip()
            length = line[6].strip()
            quality = line[7].strip()
            packing = int(line[8].strip())
            new_item = {'code': code, 'cat_name': cat_name, 'name': name, 'colour': colour, "length": length,
                        "quality": quality, "packing": packing}
            if new_item in items:
                return items

            items.append(new_item)

        ##            print((code,cat_name,name,colour,length,quality,packing))
        send.send('{PGDN}')
        send.send('{home}')
        time.sleep(.4)
        new_screen = process_scene(window.get_window())
        screen = new_screen
        if new_screen[6:] == old_screen[6:]:
            time.sleep(1)
            new_screen = process_scene(window.get_window())
            if new_screen[6:] == old_screen[6:]:
                break
        old_screen = new_screen

    return items


def parse_input_purchase(screen):
    send = SendData()
    screen = screen[6:]
    new_screen = None
    items = {}
    while True:

        for line in screen:
            if '══' in line:
                break
            line = line.split('║')
            ##        print(line)
            lot = line[1].strip()
            price = line[6].strip().replace(',', '.')
            items[lot] = price

        send.send('{PGDN}')
        time.sleep(0.5)
        new_screen = process_scene(window.get_window())[6:]
        if screen == new_screen:
            break
        screen = new_screen
    return items


##        i = 1
##        i = screen[line_num][i:].index('║')
##
##        next_line = screen[line_num][i + 5:].index('║')
##
##        cat_num = screen[line_num][i + 2:i + 5]
##
##        cat_name = screen[line_num][i + 5 : i + 16]
##        print(cat_name)
##        

def price(items, from_date, to_date, margin):
    navigation.to_virtual_stock(from_date, to_date)
    screen = process_scene(window.get_window())
    send = SendData()

    for i in items:
        if items[i]:
            print(i, items[i], '... ', end='')
            price = '{0:.2f}'.format(float(items[i]) * margin)
            print(price)
            commands = ('{F7}', i, '{right}', '{enter}', '{F2}', '{enter}')
            for cmd in commands:
                send.send(cmd)

            for n in range(8):
                send.send('{F10}')
                send.send(price)
                send.send('{enter}')
            send.send('{f11}')
            send.send('{f12}')


def need_input():
    screen = process_scene(window.get_window())
    index = 0
    for i in screen:
        index += 1
    if 'Visible' in screen[24] and 'Buyer' in screen[29]:
        return False
    return True


def menu_nav_columns(col, target):
    target = target.lower().strip()
    screen = process_scene(window.get_window())
    col_width = 25
    index = 0
    for line in screen[5:22]:
        start = 4 + (col * col_width)
        line_text = line[start: start + col_width].strip().lower()
        if target == line_text:
            return str(index)
        index += 1
    return False


def get_menu_row(num):
    screen = process_scene(window.get_window())
    screen = screen[5:-4]
    items = []
    column_len = 24
    for s in screen:
        line = s[4:-1].rstrip()
        start = column_len * (num - 1)
        end = column_len * (num)
        ##        if num == 3:
        ##            end+= 4
        line = line[start:end].strip()
        if len(line):
            items.append(line)
    return items


def main_menu_row(col, item):
    menus = get_menu_row(col)
    i = 0
    for menu in menus:
        if item.strip() == menu.strip():
            return i
        i += 1


def price_list_categories():
    screen = process_scene(window.get_window())
    screen = screen[8:-5]
    categories_group_1 = []
    for line in screen:
        l = line.split("║")
        categories_group_1.extend(l)

    ##        print(start, start + col_width)
    categories_group_1.sort()
    categories_group_2 = []
    for l in categories_group_1:
        if l.strip() != '' and '═' not in l:
            l = l[4:]
            l = l.strip()
            categories_group_2.append(l)
    return categories_group_2


def get_price_list_base():
    send = SendData()
    prices = []
    last_screen = []
    process_scene(window.get_window())
    send.send('{HOME 3}')
    time.sleep(0.2)
    while True:
        time.sleep(0.2)
        screen = process_scene(window.get_window())
        screen = screen[8:-4]
        screen_prices = []
        for line in screen:
            if line[-10:-1].strip() not in ('', '═════════'):
                screen_prices.append(line[-10:-1].strip().replace(',', '.'))
        if screen_prices != last_screen:
            last_screen = screen_prices
            prices.extend(screen_prices)
        else:
            break
        send.send('{PGDN}')
        print("Down")
        time.sleep(0.5)
    return prices


def get_categories():
    send = SendData()
    categories = []
    old_screen = []
    screen = process_scene(window.get_window())[6:-1]
    send.send('{home 5}')
    time.sleep(1)
    screen = process_scene(window.get_window())[6:-1]
    while old_screen != screen:
        old_screen = screen
        for line in screen:
            line = line.split('║')
            if '══' not in line[0]:
                for l in line[2:5]:
                    if l[3:].rstrip() and not l[3:].rstrip().isspace():
                        categories.append((l[3:].rstrip()))
            else:
                for l in line[1:4]:
                    if l[3:].rstrip() and not l[3:].rstrip().isspace():
                        categories.append((l[3:].rstrip()))
            # print(line)
        send.send('{PGDN}')
        time.sleep(1)
        screen = process_scene(window.get_window())[6:-1]
        # a[1].split('║')[2][3:].rstrip()
    categories.sort()
    return categories


def get_orderstatus_orders(date):
    send = SendData()
    screen = process_scene(window.get_window())[6:-1]
    send.send('{home 5}')
    screen = process_scene(window.get_window())[6:-1]
    last_screen = None

    clients = []
    while screen != last_screen:
        last_screen = screen
        screen = process_scene(window.get_window())[6:-6]
        for s in screen:

            order_num = s[20:27].strip()
            if order_num:
                clients.append([s[1:7].strip(), order_num, date])
        send.send('{pgdn}')
        time.sleep(.5)
    return clients


def get_orderstatus_orders2():
    send = SendData()
    screen = process_scene(window.get_window())[6:-1]
    send.send('{home 5}')
    screen = process_scene(window.get_window())[6:-1]
    last_screen = None
    date = process_scene(window.get_window())[4][9:20].strip()

    clients = []
    while screen != last_screen:
        last_screen = screen
        screen = process_scene(window.get_window())[6:-6]
        for s in screen:

            order_num = s[20:27].strip()
            if order_num:
                clients.append([s[1:7].strip(), order_num, date])
        send.send('{pgdn}')
        time.sleep(.5)
    return clients


def get_input_purchase_info():
    screen = process_scene(window.get_window())
    time.sleep(.01)
    screen = process_scene(window.get_window())
    assortment, price, quantity, packing, supplier, box_size, name = screen[29][18:30].strip(), screen[31][
                                                                                                18:24].strip(), \
                                                                     screen[31][48:53].strip(), screen[31][
                                                                                                55:58].strip(), \
                                                                     screen[31][64:70].strip(), screen[31][
                                                                                                59:62].strip(), \
                                                                     screen[29][30:50].strip()

    packing = packing.strip('x')

    return {'assortment': assortment, 'price': price, 'packing': packing, 'quantity': quantity, 'supplier': supplier,
            'box_size': box_size, 'name': name}


def get_num_pricelist_items():
    send = SendData()
    old_screen = None
    screen = process_scene(window.get_window())
    send.send("{HOME 2}")
    time.sleep(.5)
    num = 0
    while screen != old_screen:
        screen = process_scene(window.get_window())
        for s in screen[8:-4]:
            if s[1:3].strip():
                num += 1
        send.send("{PGDN}")
        time.sleep(.5)
        old_screen = screen
        screen = process_scene(window.get_window())
        time.sleep(.1)
    send.send("{HOME 2}")
    print(num)
    return num


def read_art_info_pricelist(depth=0):
    try:
        send = SendData()
        window.drag_window()
        send.send("+{F10}")
        send.send("{UP}")
        time.sleep(.05)
        screen = process_scene(window.get_window())
        category_id = get_info(screen, "Agrp:", 1, 5)
        category_name = get_info(screen, f"Articlegroup : {category_id}", 1, 20)
        f2_name = get_info(screen[6:], category_name, 1, 30)

        info = {"f2_code": get_info(screen, "Ofsht:", 1, 10),
                "f2_category_id": category_id,
                "f2_name": f2_name,
                "f2_grade": get_info(screen, "Length/height    :", 1, 10),
                "f2_colour_code_id": get_info(screen, "Kleur            :", 1, 3),
                }

        send.send("{F12}")
        send.send("+{F7}")
        time.sleep(.05)
        screen = process_scene(window.get_window())
        info["packing"] = get_info(screen, "Eenheden per Bos       :", 1, 5)
        send.send("{F12}")
        send.send("+{F10}")
    except:
        if depth < 20:
            return read_art_info_pricelist(depth + 1)
        else:
            assert (1 == 2)
    return info


def get_info(screen, target, offset, length):
    for s in screen:
        if target in s:
            start = s.index(target) + len(target)
            start += offset
            end = start + length
            if end > len(s):
                end = -1
            return s[start:end].strip()


def parse_sales_by_region():
    send = SendData()
    send.activate_window()
    screen = process_scene(window.get_window())[8:-5]
    totals = {}
    for s in screen:
        row = s.split('║')
        code = row[3].strip()
        total = row[6].strip().replace(',', '.')
        if total:
            totals[code] = total
    return totals


def parse_sales_by_client():
    send = SendData()
    send.activate_window()
    clients = {}
    old_screen = None
    screen = process_scene(window.get_window())[8:-5]
    while old_screen != screen:
        for s in screen:
            row = s.split('║')
            code = row[2].strip()
            total = row[5].strip().replace(',', '.')
            if total:
                if code not in clients:
                    clients[code] = {}
                invoice_num = row[3].strip()
                clients[code][invoice_num] = total
        send.send("{PGDN}")
        time.sleep(.1)
        old_screen = screen
        screen = process_scene(window.get_window())[8:-5]

    return clients



# info = read_art_info_pricelist()
# for p in info:
#    print(p,info[p])
# print(get_input_purchase_info())
##get_orderstatus_orders('13/11/17')
##print(menu_nav_columns(1, 'Orderstatus purchase'))
#  def parse_assortment_report(filename = "assortment_report.html"):

##from database import *        

# process_scene(window.get_window())
##if __name__ == "__main__":
##
####    for date, margin in (('01/02/16',1.5),('31/01/16',1.6),('30/01/16',1.45),('02/02/16',1.6)):
##    for date, margin in (('02/02/16',1.6),):
##        send = SendData()
##        screen = process_scene(helper.get_window())
##        navigation.to_virtual_purchase(date)
##        items = parse_input_purchase(screen)
##        price(items,date,date,margin)
##


##    cat_name = 'Ecuador Roses'
##    a = parse_assortment_category_section(cat_name)
# c = order_categories(screen)
##    print(parse_order_category('cat_name'))

##    helper.run_purchase_list("011115", "071115","CASIFL")
##    time.sleep(1)
##    screen = process_scene(helper.get_window())  
##    o = distribution_list_product(screen)
##    for i in o:
##        print(i.client, i.name, i.quantity, i.comment )

##time.sleep(1)

##screen = process_scene(helper.get_window())#
##
##send = SendData()
##items = {}
##
##
##items = parse_input_purchase(helper.get_window())
##price(items,'010516','150516',1.5)


##for date, margin in (('03/05/16',1.6),):
##        send = SendData()
##        screen = process_scene(helper.get_window())
##        navigation.to_virtual_purchase(date)
##        items = parse_input_purchase(screen)
##        price(items,date,date,margin)
##
##        
##a = parse_assortment_category_section('Alstro ON')
