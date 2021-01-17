# import win32api
import time

import win32com.client


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SendData(metaclass=Singleton):
    def __init__(self, window_name="Connect (© Uniware Computer Systems BV) (Session 1 : connect.metz.com)",
                 shell=win32com.client.Dispatch("WScript.Shell")):
        self.window_name = window_name
        ##        self.window_name = 'notepad'
        self.shell = shell

    def activate_window(self):
        self.shell.AppActivate(self.window_name)
        '''if self.shell.AppActivate(self.window_name):
            #self.shell.AppActivate(self.window_name)
            print("activate")
        else:
            pass
            #messagebox.showinfo(message= self.window_name + " is not open, please prepare window to accept input.\nOutput will instead print to Notepad")
            #if not self.shell.AppActivate("Notepad"):
            #    self.shell.Run("Notepad")
            #    self.shell.AppActivate("Notepad")
            #time.sleep(.05)
        time.sleep(.1)'''

    def send(self, data):
        data = str(data)
        if "{" not in data:
            data = convert(data)
            data = stringfy(data)
        self.shell.SendKeys(data)
        time.sleep(.01)

    def send_exact(self, data):
        data = convert(data)
        data = stringfy_exact(data)
        self.send(data)

    def f2_purchase(self, assortment_code, price, number, packing, supplier):
        '''assortment_code = assortment_code.replace('+','{+}')
        assortment_code = assortment_code.replace('%','{%}')
        assortment_code = assortment_code.replace('^','{^}')
        assortment_code = assortment_code.replace('[','{[}')
        assortment_code = assortment_code.replace(']','{]}')
        assortment_code = assortment_code.replace('~','{~}')
        assortment_code = assortment_code.replace('(','{(}')
        assortment_code = assortment_code.replace(')','{)}')'''

        cmd_order = ['{enter}', price, '{enter}', ' ', '{enter}', number, '{enter}', packing, '{enter}', supplier,
                     '{F11}', '{enter}']
        self.send_exact(assortment_code)
        for cmd in cmd_order:
            self.send(cmd)
            time.sleep(.001)

    ##        print (assortment_code)

    def f12(self):
        self.send('{F12}')

    def enter_csv(self, filename):
        import csv
        self.activate_window()
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                if row[0] != '':
                    self.f2_purchase(row[0], row[1], row[2], row[3], row[4])


def stringfy_exact(s):
    final = ''
    special = '+%^[]~{}'
    for st in s:
        if st[0] in special or st[1] > 1:
            if st[1] > 1:
                new_str = "{%s %s}" % (st[0], st[1])
            else:
                new_str = "{%s}" % st[0]
            final += new_str

        else:
            final += st[0]
    return final


def stringfy(s):
    final = ''
    for st in s:
        if st[1] != 1:
            final += "{%s %s}" % (st[0], st[1])
        else:
            final += st[0]
    return final


def convert(st):
    s = []
    st = str(st)
    for c in st:
        if not s:
            s.append([c, 1])
        else:
            if c == s[-1][0]:
                s[-1][1] += 1
            else:
                s.append([c, 1])
    return s

#### testing code####################
# purchases = SendData()
# purchases.activate_window()
##purchases.send('2')
##a
##purchases.activate_window()
##for i in range(10):
# purchases.f2_purchase('RSR7','1.00','1','50','CASIFL')
##
# time.sleep(1)
# purchases.send("Aaaaaaaaaaaaaaaaaaaa")
## dutch_window_name = 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : connect.metz.com)'
##data = "dcafrege+g"
# data = convert(data)
# data = stringfy_exact(data)
# print(data)
