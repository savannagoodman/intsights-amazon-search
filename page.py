import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException


class HomePage(object): 
    
    SEARCH_BAR_ID = "twotabsearchtextbox"
    SEARCH_BUTTON_CLASSNAME = "nav-input"
    NAV_CART_BUTTON_ID = "nav-cart"

    def __init__(self, driver):
        self.driver = driver

    def search(self, search_query):
        search_bar_element = self.driver.find_element_by_id(self.SEARCH_BAR_ID)
        search_bar_element.clear()
        search_bar_element.send_keys(search_query)
        time.sleep(3)
        self.driver.find_element_by_class_name(self.SEARCH_BUTTON_CLASSNAME).click()

    def go_to_cart(self):
        self.driver.find_element_by_id(self.NAV_CART_BUTTON_ID).click()


class SearchResultsPage(object):

    RESULT_COUNT_ID = "s-result-count"
    RESULTS_ID = "s-results-list-atf"
    ITEM_LIST_CSS_SELECTOR = "ul.s-result-list li.s-result-item"
    NAME_CSS_SELECTOR = "h2:last-child"
    DATE_CSS_SELECTOR = ".a-size-small"
    PRICE_CSS_SELECTOR = ".sx-price.sx-price-large"
    STARS_CLASS_NAME = "a-icon-alt"
    NEXT_PAGE_ID = "pagnNextString"
    ITEM_NUMBER_ID = "result_{}"

    def __init__(self, driver):
        self.driver = driver

    def get_all_data_list(self, item):
        return item.text.split('\n')

    def get_name(self, item):
        try:
            name_element = item.find_element_by_css_selector(self.NAME_CSS_SELECTOR)
            name_str = name_element.text.encode('utf-8')
        except NoSuchElementException: 
            name_element = None
            name_str = 'INFORMATION UNAVAILABLE'
        return name_element, name_str

    def get_date(self, item):
        try:
            date_element = item.find_element_by_css_selector(self.DATE_CSS_SELECTOR)
            date_str = date_element.text.encode('utf-8')
        except NoSuchElementException:
            date_element = None
            date_str = 'INFORMATION UNAVAILABLE'
        return date_element, date_str

    def get_author(self, item, all_data_list):
        try:
            author_str = [a[3:] for a in all_data_list if a.find('by') == 0][0]
        except NoSuchElementException:
            author_str = 'INFORMATION UNAVAILABLE'
        author_element = None
        return author_element, author_str
                
    def get_price(self, item, all_data_list):
        try:
            price_element = item.find_element_by_css_selector(self.PRICE_CSS_SELECTOR)
            price_str = price_element.text.encode('utf-8')
        except NoSuchElementException:
            try:
                price = [t for t in all_data_list if t.find('$') == 0][0]
                price_str = price[:price.find('(')]
                price_element = None
            except:
                try:
                    price_str = [t for t in all_data_list if t == 'Free'][0]
                    price_element = None
                except:
                    price_str = 'INFORMATION UNAVAILABLE'
                    price_element = None
        return price_element, price_str

    def get_stars(self, item):
        try:
            stars_element = item.find_element_by_class_name(self.STARS_CLASS_NAME)
            stars_str = stars_element.get_attribute('textContent')
        except NoSuchElementException:
            stars_element = None
            stars_str = 'INFORMATION UNAVAILABLE'
        return stars_element, stars_str

    def get_reviews(self, item, all_data_list):
        reviews_str = 'INFORMATION UNAVAILABLE'
        reviews_element = None
        for value in all_data_list:
            if value.isdigit():
                reviews_str = value
                break
            else:
                continue
        return reviews_element, reviews_str

    def get_indent(self):
        try:
            result_count = self.driver.find_element_by_id(self.RESULT_COUNT_ID)
            indent = int(result_count.text.split('-')[0]) - 1
        except NoSuchElementException:
            indent = 0
        return indent        

    def get_single_item(self, item_number = None):
        results_element = self.driver.find_element_by_id(self.RESULTS_ID)
        item_list_element = results_element.find_elements_by_css_selector(self.ITEM_LIST_CSS_SELECTOR)
        if item_number:
            item_element = item_list_element[item_number]
        else:
            item_element  = item_list_element[0]
        return item_element

    def go_to_item(self, item):
        name_element, name_str = self.get_name(item)
        name_element.click()
        #    slow browser causes popup to display after a few seconds
        time.sleep(10)
        return name_str

    def get_all_items(self):
        all_items = []
        """get results from first 4 pages"""
        for page in range(4):
            page_results = self.extract_page(page)
            all_items.extend(page_results)
        return all_items

    def extract_page(self, page):
        page_results = []
        results_element = self.driver.find_element_by_id(self.RESULTS_ID)
        item_list_element = results_element.find_elements_by_css_selector(self.ITEM_LIST_CSS_SELECTOR)
        for item_element in item_list_element:
            item_data = self.extract_element(item_element)
            page_results.append(item_data)    
        next_page = self.driver.find_element_by_id(self.NEXT_PAGE_ID)
        next_page.click()
        time.sleep(5)
        return page_results

    def extract_element(self, item_element):
        all_data_list = self.get_all_data_list(item_element)
        name_element, name_str = self.get_name(item_element)
        date_element, date_str = self.get_date(item_element)
        author_element, author_str = self.get_author(item_element, all_data_list)
        price_element, price_str = self.get_price(item_element, all_data_list)
        stars_element, stars_str = self.get_stars(item_element)
        reviews_element, reviews_str = self.get_reviews(item_element, all_data_list)
        item_data = (name_str, date_str, author_str, price_str, stars_str, reviews_str)
        return item_data


class ItemPage(object):
    
    ADD_TO_CART_BUTTON_ID = "submit.add-to-cart"
    FORMAT_TABLE_ID = "tmmSwatches"
    FORAMTS_CLASS_NAME = "a-button-text"
    POPUP_CLASS_NAME = "a-popover-wrapper"
    CLOSE_POPUP_BUTTON_ID = "p2dPopoverID-no-button"

    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self):
        try:
            self.driver.find_element_by_id(self.ADD_TO_CART_BUTTON_ID).click()
            return True
        except NoSuchElementException:
            self.click_paperback_format()
            popup_clear = self.popup_clear()
            if not popup_clear:
                try:
                    close_popup_button = self.driver.find_element_by_id(self.CLOSE_POPUP_BUTTON_ID)
                    close_popup_button.click()
                except:
                    return False
            self.driver.find_element_by_id(self.ADD_TO_CART_BUTTON_ID).click()
            return True

    def popup_clear(self):
        try:
            close_popup_button = self.driver.find_element_by_id(self.CLOSE_POPUP_BUTTON_ID)
            popup_clear = False
        except NoSuchElementException:
            popup_clear = True
        return popup_clear

    def click_paperback_format(self):
        format_table = self.driver.find_element_by_id(self.FORMAT_TABLE_ID)
        formats = format_table.find_elements_by_class_name(self.FORAMTS_CLASS_NAME)
        f = [f for f in formats if f.text[:f.text.find('\n')] == 'Paperback']
        if f == None:
            return Flase
        else:
            paperback_element = f[0]
            paperback_element.click()
            time.sleep(3)
            return True


class CartPage(object):

    def __init__(self, driver):
        self.driver = driver

    def is_item_in_cart(self, item_name):
        try:
            self.driver.find_element_by_link_text(item_name)
            return True
        except:
            return False
