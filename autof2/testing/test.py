import unittest
from autof2.navigation import navigation
from autof2.purchase import purchase
from autof2.readf2 import parse
from autof2.interface import window
from orders import orders

class TestNavigationMethods(unittest.TestCase):

    def test_navigation_main(self):
        navigation.to_main()
        screen = parse.process_scene(window.get_window())
        self.assertTrue(parse.identify_screen(screen,'Main Menu'))

    def test_navigation_purchase_list(self):
        navigation.to_purchase_list()
        screen = parse.process_scene(window.get_window())
        self.assertTrue(parse.identify_screen(screen, 'Advanced'))

class TestPurchasingMethods(unittest.TestCase):
    def setUp(self):
        self.date = '01/01/29'
        self.supplier = "CAROSA"
        self.purchases = [
            {'f2_code':"gebwhgr", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebvenga", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebsnowb", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebsilvr", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebsilve", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebpole", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebolymp", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebinspr", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebicy", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebicebr", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebbal", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebLovei", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebKILIA w", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebAvem", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebartis", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier},
            {'f2_code':"gebSuraa", 'price': 0.65, 'quantity': 1, 'packing':150, 'supplier': self.supplier}
        ]
        for p in self.purchases:
            p['client'] = "CT*EMB"
        self.starting_value = purchase.get_purchase_amount(self.supplier, self.date)




    def test_insert_purchase(self):
        purchase.purchase_list(self.purchases, self.date)
        amount_purchased = add_purchases(self.purchases)
        new_value = purchase.get_purchase_amount(self.supplier, self.date)
        self.assertTrue(abs(self.starting_value + amount_purchased - new_value) < 2)

    def test_orders(self):
        orders.enter_order(self.date, self.purchases)


def add_purchases(purchases):
    i = 0
    for p in purchases:
        i += p['price'] * p['packing'] * p['quantity']
    return i

if __name__ == '__main__':
    unittest.main()