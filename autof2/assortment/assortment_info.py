import os
class Assortment:
    extention = '.f2a'
    # we can use this to select different orders of columns in F2
    assortment_order= [("f2_code","category","product_name","colour","grade","quality","quantity"),]
    def __init__(self, filepath,category):

        # create filepath if it doesn't exist
        if not os.path.isdir(filepath):
            os.makedirs(filepath)

        self.filepath = filepath
        self.category = category
        self.assortment = []
        self.lookup = {}
        if  filepath[-1] not in ('\\','/'):
##            self.filepath.replace('/','\\')
            self.filepath += '\\'
        self.filename = self.filepath + category + Assortment.extention
        if category in ('test',): #immplement column order by category
            self.assortment_order_index = 0
        else:
            self.assortment_order_index = 0

    def create_file(self,assortment_order_index = 0):
        self.assortment_order_index = assortment_order_index
        if not os.path.isfile(self.filename):
            with open(self.filename,'w') as file:
                file.write(self.category + '\n')
                file.write(str(assortment_order_index) + '\n')
            self.add_product(self.assortment_order[assortment_order_index])  
    
    def add_product(self,product):
        if os.path.isfile(self.filename):
            with open(self.filename,'a') as file:
                for c in product:
                    file.write(str(c))
                    file.write('\t')
                file.write('\n')
    def add_from_assortment(self,product):
        if os.path.isfile(self.filename):
            with open(self.filename,'a') as file:
                for c in Assortment.assortment_order[self.assortment_order_index]:
                    file.write(str(product[c]))
                    file.write('\t')
                file.write('\n')
        
    def read_file(self):
        with open(self.filename,'r') as file:
            category = file.readline().strip()
            self.assortment_order_index = int(file.readline().strip())
            headers = file.readline().strip()
            line = file.readline().strip()
            while line:
                product={}
                index=0
                for l in line.split('\t'):
                    product[Assortment.assortment_order[self.assortment_order_index][index]] = l.strip()
                    index += 1
                if product not in self.assortment:
                    self.assortment.append(product)
                    self.lookup[product['f2_code']] = product
                line = file.readline().strip()
            
    def compact_file(self):
        if os.path.isfile(self.filename):
            self.read_file()
            os.remove(self.filename)
            self.create_file(self.assortment_order_index)
            for a in self.assortment:
                self.add_from_assortment(a)         


    
        
                 
                 
                 
                 
                 
        
        
        
        
        
                
        

