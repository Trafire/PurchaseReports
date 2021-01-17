from autof2.navigation import navigation
from autof2.interface import window

def print_distribution_report(date,supplier):
    window.get_window()
    navigation.to_distribution_report(date,supplier, "laserprinter")

def run_distribution_report(date,supplier):
    window.get_window()
    navigation.to_distribution_report(date,supplier, "screen")    



