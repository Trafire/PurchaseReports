import subprocess
import pickle
import os.path
import json
import time
import os
from datetime import datetime,timedelta

def pdftotext(input_filename,output_filename, read_format="-table"):
    args = [r"bin/pdftotext.exe",read_format, input_filename,output_filename]
    subprocess.call(args)

def get_text(input_filename,output_filename = r"output/out.txt",read_format="-table"):
    pdftotext(input_filename, output_filename, read_format)
    with open(output_filename) as file:
        return file.read()

def find_info(target, invoice_rows):
    for r in invoice_rows:
        if target in r:
            lindex = r.index(target) + len(target)
            return r[lindex:].strip()
    return ''

def get_supplier(invoice_rows):
    for r in invoice_rows:
        if len(r) > 0 and r[0] != ' ':
            return r[:50].strip()
    return ''



def get_product_to_purchase(invoice_rows, invoice_type):
    add = False
    purchase_lines = []
    purchases = []

    for r in invoice_rows:

        if "Page " in r or "THIS IS NOT A BILL" in r or "Service Surcharge" in r or "Fuel Surcharge" in r or "Surcharge" in r:
            add = False
            print(r)
        if 'Inv. Subtotal' in r or "Service Charge" in r or "Handling" in r:
            break
        if add and len(r) > 0 and "Vendor:" not in r and "Customer Code" not in r and "Sleeve: Carton; Cut: AM" not in r:
            purchase_lines.append(r)
        if "Unit Price" in r or "Units/Box" in r:
            add = True
    for r in purchase_lines:
        if invoice_type == "prebook":
            purchases.append(process_line_prebook(r))
        else:
            purchases.append(process_line(r))

    good = []
    for p in purchases:
        #print(p['name'] )
        if p != None and p['grade'].lower() != 'mix' and  p['name'] not in  ("DAV AST Mix","Fleura Metz","Customer Code: 9853",'ROS AST',
                                                                             "ROS AST Special", 'ROS RED - COL',
                                                                             "Sprayrose Assorted","Sprayrose Assorted",
                                                                             "DAV AST","Sweetheart Rose RVS Assorted",
                                                                             "2 White Ohara 2 Pink",
                                                                             "ROS WHT White and Cream Mix Pack",
                                                                             "ROS AST Discovery Pack"):
            #print(p)
            print(p['name'])
            good.append(p)
  
    return good

def process_line_prebook(line):
    if "Totals" in line:
        return None
    if "Bun" in line:
        print("bub")
        print(line)
        sep = line.index(' Bun ')
        name_grade = name = line[:sep].strip()
        name_grade = name[:name.rindex(' ')]
        mix_line = True # part of a mixed box
        num_string = '1'
        box_string = 'QB'
        box_price = ''
        unit_price = line.strip()[line.rindex(' '):].strip()[:-1]
        #get packing
        packing_string_a = line[:sep].strip()
        packing_string_a = packing_string_a[packing_string_a.rindex(' '):].strip()
        packing_string_b = line[sep + len(" Bun"):].strip()
        packing_string_b = packing_string_b[:packing_string_b.index(' ')]
        packing_string = str(int(packing_string_a) * int(packing_string_b))
        box_price = "%1.2f"% float(str(float(unit_price.strip('$')) * float(packing_string.strip('$'))))
        grade = name_grade[name_grade.rindex(' '):].strip()
        grade =name_grade[sep:].strip()
        grade = name_grade[name_grade.rindex(' '):].strip()
        name = name_grade[:name_grade.rindex(' ')].strip()

    else:
        adjustment = 0
        if len(line) < 100:
            adjustment = 10
            name_grade = line[:32 - adjustment].strip()
            print(line)
            sep = name_grade.rindex(' ')
            name = name_grade[:sep].strip()
            grade = name_grade[sep:].strip()
            mix_line = False
            num_string =line[32:36].strip()
            box_string = line[44 :47].strip()
            packing_string = line[71:75].strip()
            box_price = "%1.2f"% float(line.strip()[line.rindex(' '):].strip())
            unit_price = line[62:68].strip()

        else:
            name_grade = line[:34 - adjustment].strip()
            print(line)
            sep = name_grade.rindex(' ')
            name = name_grade[:sep].strip()
            grade = name_grade[sep:].strip()
            mix_line = False
            num_string = line[52-adjustment:56-adjustment].strip()
            box_string = line[64-adjustment:67-adjustment].strip()
            packing_string = line[97-adjustment:101-adjustment].strip()
            box_price = "%1.2f"% float(line.strip()[line.rindex(' '):].strip())
            unit_price = line[89-adjustment:97-adjustment].strip()
            #unit_price = unit_price[unit_price.rindex(' '):].strip()[:-1]
    if num_string == '':
        print(line)
        name_grade = line[:46].strip()
        sep = name_grade.rindex(' ')
        name = name_grade[:sep].strip()
        grade = name_grade[sep:].strip()
        mix_line = False
        num_string = line[47:50].strip()
        box_string = line[57:60].strip()
        packing_string = line[91:95].strip()
        box_price = "%1.2f"% float(line.strip()[line.rindex(' '):].strip())
        unit_price = line[82:90].strip()

    unit_price = unit_price.strip('$')
    unit_price = unit_price.strip()
    unit_price = "%1.2f"% float(unit_price)

    return {'name': name, 'grade': grade, "mix_line": mix_line, 'quantity': num_string, "box_type": box_string,
            "packing": packing_string, 'box_price': "%1.2f"% float(box_price.strip('$')), "unit_price": unit_price.strip('$')}

def process_line(line):
    if ' x ' in line:
        sep = line.index(' x ')
        name_grade = line[:sep].strip()
        mix_line = False
        #get_num of boxes
        print(line)
        try:
            sep = line.rindex('-') + 1
        except:
            sep = line.rindex('O') + 1
        num_string = line[sep:].strip()
        sep2 =num_string.index(' ')
        num_string = num_string[:sep2]
        # get box type
        try:
            sep = line.rindex('-') + 1
        except:
            sep = line.rindex('O') + 1
        box_string = line[sep:].strip()
        sep2 = box_string.index(' ')
        box_string = box_string[sep2:].strip()
        sep3 = box_string.index(' ')
        box_string = box_string[:sep3].strip()
        # get packing
        lindex = line.rindex(box_string) + len(box_string)
        packing_string = line[lindex:].strip()
        packing_string = packing_string [:packing_string.index(' ')].strip()
        #get price
        box_price = line.strip()[line.rindex(' '):].strip()
        unit_price = line[:line.rindex(box_price)].strip()
        unit_price = unit_price[unit_price.rindex(' '):].strip()[:-1]

        packing_string = str(int(int(packing_string) / int(num_string)))


    elif " Bun. " in line:
        print("here")
        sep = line.index(' Bun. ')
        name_grade = name = line[:sep].strip()
        name_grade = name[:name.rindex(' ')]
        mix_line = True # part of a mixed box
        num_string = '1'
        box_string = 'QB'
        box_price = ''
        unit_price = line.strip()[line.rindex(' '):].strip()[:-1]
        #get packing
        packing_string_a = line[:sep].strip()
        packing_string_a = packing_string_a[packing_string_a.rindex(' '):].strip()
        packing_string_b = line[sep + len(" Bun."):].strip()
        packing_string_b = packing_string_b[:packing_string_b.index(' ')]
        packing_string = str(int(packing_string_a) * int(packing_string_b))
        box_price = str(float(unit_price.strip('$')) * float(packing_string.strip('$')))
    else:
        print(line)
        name_grade = line
        num_string = '999'
        box_string = "HB"
        packing_string = ''
        box_price = ''
        unit_price = ''
        mix_line = False



    grade = name_grade[name_grade.rindex(' '):].strip()
    name = name_grade[:name_grade.rindex(' ')].strip()

    return {'name':name, 'grade':grade, "mix_line":mix_line, 'quantity' : num_string, "box_type": box_string,
            "packing":packing_string, 'box_price': "%1.2f"% float(box_price.strip('$').replace(',','')), "unit_price":unit_price.strip('$')}

def match_f2(data_type, data):
    filename = 'convert/' +data_type + '.pic'
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            file_data = pickle.load(file)
    else:
        file_data = {}
    if data in file_data:
        return file_data[data]
    else:
        d = get_data_from_user(data)
        file_data[data] = d
        with open(filename, 'wb') as file:
            pickle.dump(file_data,file)
    return file_data[data]

def remove_entry(data_type,item):
    filename = 'convert/' + data_type + '.pic'
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            file_data = pickle.load(file)
        del file_data[item]
        with open(filename, 'wb') as file:
            pickle.dump(file_data,file)






def get_data_from_user(data):
    print("enter data")
    return input(data)

def process_komet_invoice_without_purchase(input_filename,output_filename = r"output/out.txt",read_format="-table"):
    invoice_text = get_text(input_filename)

    invoice_text = invoice_text.replace('at\n\n', 'at ')
    invoice_rows = invoice_text.split('\n')
    invoice_date = find_info("Invoice Date", invoice_rows)
    invoice_date = datetime.strptime(invoice_date, "%m/%d/%Y")
    invoice_date = invoice_date + timedelta(days=2)
    invoice_date = invoice_date.strftime('%d/%m/%y')


    if "Prebook #" not in invoice_text:
        invoice_num = find_info("Invoice #", invoice_rows)
        invoice_type = "invoice"

    else:
        invoice_num = find_info("Prebook #", invoice_rows)
        invoice_type = "prebook"
    total = find_info("Totals", invoice_rows)
    supplier = get_supplier(invoice_rows)
    f2_supplier = match_f2('supplier', supplier)
    return (f2_supplier, invoice_num, invoice_date, total.strip('$').replace(',',''))



def process_komet_invoice(input_filename,output_filename = r"output/out.txt",read_format="-table"):
    invoice_text = get_text(input_filename)

    invoice_text = invoice_text.replace('at\n\n', 'at ')
    invoice_rows = invoice_text.split('\n')
    if "Prebook #" not in invoice_text:
        invoice_num = find_info("Invoice #", invoice_rows)
        invoice_type = "invoice"

    else:
        invoice_num = find_info("Prebook #", invoice_rows)
        invoice_type = "prebook"
    total = find_info("Totals", invoice_rows)
    supplier = get_supplier(invoice_rows)
    #print(invoice_num, total,supplier)
    purchases = get_product_to_purchase(invoice_rows,invoice_type)
    f2_supplier = match_f2('supplier',supplier)
    charge_words = ["Service Surcharge","Service Charges","Handling","Service Surcharge                                                    -                    -         -           -",'Service Surcharge                                              -                    -         -           -']
    for charge in charge_words:
        if charge in invoice_text:
            box_charge = find_info(charge, invoice_rows)
            box_charge = box_charge[box_charge.rindex('$') + 1:].replace(',','')
            float(box_charge)
            total_stems = find_info("Total stems:", invoice_rows)
            print(total_stems)
            try:
                total_stems = total_stems[:total_stems.index(',')]
            except:
                total_stems = 0
                for p in purchases:
                    total_stems += int(p['quantity']) * int(p['packing'])
                total_stems = str(total_stems)
            additional_charge = float(box_charge) / int(total_stems)
            break
        else:
            box_charge = 0
            additional_charge = 0
    for p in purchases:
        match_f2("product",(p['name'],p['grade']) )
        match_f2("box_size", p['box_type'])
    for p in purchases:
        if p['unit_price']:
            print(p['unit_price'])
            p['unit_price'] = float(p['unit_price'].strip('$'))
            p['unit_price'] += additional_charge
            p['unit_price'] = "%.2f" % p['unit_price'] 
    return (supplier, invoice_num, purchases)

def process_komet_header_info(input_filename,output_filename = r"output/out.txt",read_format="-table"):
    invoice_text = get_text(input_filename)

    invoice_text = invoice_text.replace('at\n\n', 'at ')
    invoice_rows = invoice_text.split('\n')
    if "Prebook #" not in invoice_text:
        invoice_num = find_info("Invoice #", invoice_rows)
        invoice_type = "invoice"

    else:
        invoice_num = find_info("Prebook #", invoice_rows)
        invoice_type = "prebook"
    total = find_info("Totals", invoice_rows)
    supplier = get_supplier(invoice_rows)
    #print(invoice_num, total,supplier)
    purchases = []
    f2_supplier = match_f2('supplier',supplier)
    charge_words = ["Service Charges","Handling","Fuel Surcharge","Service Surcharge                                                    -                    -         -           -"]
    for charge in charge_words:
        if charge in invoice_text:
            box_charge = find_info(charge, invoice_rows)
            box_charge = box_charge[box_charge.rindex('$') + 1:].replace(',','')
            float(box_charge)
            total_stems = find_info("Total stems:", invoice_rows)
            print(total_stems)
            try:
                total_stems = total_stems[:total_stems.index(',')]
            except:
                total_stems = 0
                for p in purchases:
                    total_stems += int(p['quantity']) * int(p['packing'])
                total_stems = str(total_stems)
            additional_charge = float(box_charge) / int(total_stems)
            break
        else:
            box_charge = 0
            additional_charge = 0
    for p in purchases:
        match_f2("product",(p['name'],p['grade']) )
        match_f2("box_size", p['box_type'])
    for p in purchases:
        print(p)
        p['unit_price'] = float(p['unit_price'].strip('$'))
        p['unit_price'] += additional_charge
    return (supplier, invoice_num, purchases)



def create_json(data, date, shipment_code):
    command = "scripts/enter_shipment_mix2.f2s"
    # command = "scripts/print_purchase_details.f2s"
    f2_system = "f2Canada"
    awb = "GROUND"

    logistical_route = "MIA-YYZ (truck)"
    invoice_num = data[1]
    f2_data = []
    for p in data[2]:
        quantity = int(p["quantity"])
        while quantity > 0:
            f2_data.append({"assortment": match_f2("product", (p['name'],p['grade'])), "box_size": match_f2("box_size", p["box_type"]),
             "price": p["unit_price"], "quantity": 1, "packing": p["packing"], "supplier": match_f2("supplier",data[0])})
            quantity -= 1

    '''f2_data = [{"assortment": "flxmagti0", "box_size": "H10",
                "price": "1.85", "quantity": 17, "packing": 25, "supplier": supplier}]'''
    make_json(command, f2_system, date, awb, shipment_code, logistical_route, match_f2("supplier",data[0]), invoice_num, f2_data)


def make_json(command,f2_system, date, awb, shipment_code, logistical_route,supplier,invoice_num, f2_data):
    data = {
        "command": command,
        "system": f2_system,
        "parameters": {"date": date, "awb": awb, "shipment_code": shipment_code,
                       "logistical_route": logistical_route, "supplier": supplier, "invoice_num": invoice_num},
        "f2_data": f2_data
    }
    request_type = command[command.rindex('/') + 1:].strip('.f2s').strip()
    filename = next_filename(request_type)
    with open(r'D:\PycharmProjects\fm_ecuador\messages\%s' % filename, 'w') as file:
        json.dump(data, file)

def next_filename(request_type):
    with open(r'D:\PycharmProjects\fm_ecuador\settings\current_number.txt','r') as file:
        num = int(file.readline().strip())
    with open(r'D:\PycharmProjects\fm_ecuador\settings\current_number.txt', 'w') as file:
        file.write(str(num + 1))
    return '%012d_%s.json' % (num,request_type)

if __name__ == "__main__":
    pass

    #
    # while True:
    #
    #     #input_filename = r"D:\PycharmProjects\invoice_printer\invoices\Rosaprima International, LLC\19-04-18-Invoice #269835.pdf"
    #     input_filename = input("Filename: ")
    #
    #     time.sleep(1)
    #     print()
    #
    #     data = process_komet_invoice(input_filename)
    #     print(data)
    #     create_json(data, "13/05/18", "20-MIA")
    #     os.startfile(input_filename)
    #     #os.startfile(input_filename)
    #     '''invoice_rows = invoice_text.split('\n')
    #     invoice_text = get_text(input_filename)
    #     box_charge = find_info("Service Charges", invoice_rows)
    #     box_charge = box_charge[box_charge.rindex('$') + 1:]
    #     float(box_charge)
    #     total_stems = find_info("Total stems:", invoice_rows)
    #     total_stems = total_stems[:total_stems.index(',')]
    #     print(float(box_charge)/int(total_stems))
    #     '''
