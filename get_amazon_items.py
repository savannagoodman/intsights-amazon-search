# file name should be lower case
# no need for module per class
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from page import HomePage, SearchResultsPage, ItemPage, CartPage

class AmazonItems(object):

    URL = "http://www.amazon.com"

    def __init__(self, driver):
        self.driver = driver

    def go_to_amazon(self):
        #    maximize window in order to allow for all data to be visable
        self.driver.maximize_window() 
        self.driver.get(self.URL)

    def search_amazon(self, query):
        home_page = HomePage(self.driver)
        home_page.search(query)

    def get_items(self):
        search_results = SearchResultsPage(self.driver)
        all_items = search_results.get_all_items()
        return all_items

    def create_csv_data_file(self, all_items, csv_file_path):
        csv_file = open(csv_file_path, 'wb')
        writer = csv.writer(csv_file)
        writer.writerows(all_items)
        csv_file.close()

    def add_item_to_cart(self):
        search_results = SearchResultsPage(self.driver)
        item = search_results.get_single_item(10)
        #    search_results.go_to_item returns the item name
        go_to_item = search_results.go_to_item(item)
        item_page = ItemPage(self.driver)
        added = item_page.add_to_cart()
        if not added:
        	print 'Item is NOT in the cart. ADDING ITEM TO CART FAILED'.format(item_name)
        return go_to_item

    def check_item_in_cart(self, item_name):
        home_page = HomePage(self.driver)
        home_page.go_to_cart()
        cart_page = CartPage(self.driver)
        is_item_in_cart = cart_page.is_item_in_cart(item_name)
        if is_item_in_cart:
            print 'Selected item: \n {} \nis in the cart'.format(item_name)
            return True
        else:
            print 'Selected item: \n {} \nis NOT in the cart'.format(item_name)
            return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    r = AmazonItems(driver)
    r.go_to_amazon()
    query = 'software testing'
    r.search_amazon(query)
    all_items = r.get_items()
    r.create_csv_data_file(all_items, 'amazon_search_results.csv')    
    item_name = r.add_item_to_cart()
    r.check_item_in_cart(item_name)


