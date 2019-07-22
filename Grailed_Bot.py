from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import csv


class Grailed_Bot(object):

    def __init__(self, item, shoe_sizes, top_sizes, pants_sizes, tailoring_sizes, accesories_sizes, item_type):

        self.grailed_url = 'https://www.grailed.com'
        self.item = item
        self.shoe_sizes = shoe_sizes
        self.top_sizes = top_sizes
        self.pants_sizes = pants_sizes
        self.tailoring_sizes = tailoring_sizes
        self.accesories_sizes = accesories_sizes
        self.item_type = item_type

        chromedriver = "C:\\Users\\Lu\\Downloads\\chromedriver_win32\\chromedriver.exe"
        self.driver = webdriver.Chrome(chromedriver)

    def input_user_specs(self):

        # clicks drop down menu so that user can input their sizes
        size_drop_down_button = self.driver.find_element_by_xpath(
            '//*[@id="shop"]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]')
        size_drop_down_button.click()

        time.sleep(3)

        # hides the footer which sometimes covers up the sizes we want to click
        annoying_footer = self.driver.find_element_by_xpath('//*[@id="trust_sticky_footer"]/div')
        self.driver.execute_script("arguments[0].style.visibility='hidden'", annoying_footer)

        # hides the header which sometimes covers up the sizes we want to click
        annoying_header = self.driver.find_element_by_xpath('//*[@id="globalHeader"]/div/div[1]/div[2]')
        self.driver.execute_script("arguments[0].style.visibility='hidden'", annoying_header)

        # hides another header which covers up sizes
        another_annoying_header = self.driver.find_element_by_xpath('//*[@id="globalHeader"]/div/div[1]')
        self.driver.execute_script("arguments[0].style.visibility='hidden'", another_annoying_header)

        # Opens drop downs where users can input their sizes
        size_type_options = self.driver.find_element_by_class_name('sizes-wrapper')
        size_type_buttons = size_type_options.find_elements_by_class_name('filter-category-item-header')
        time.sleep(3)

        # inputs relevant user sizes
        if self.item_type == "Tops" or self.item_type == "Outerwear":
            size_type_buttons[0].click()
            tops_sizes = self.driver.find_element_by_xpath(
                '//*[@id="shop"]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/div/span[1]/div[2]')
            tops_sizes_list = tops_sizes.find_elements_by_class_name('active-indicator')

            for top_size in tops_sizes_list:
                if top_size.text in self.top_sizes:
                    top_size.click()
                time.sleep(1)

        elif self.item_type == "Footwear":
            size_type_buttons[2].click()
            footwear_sizes = self.driver.find_element_by_xpath(
                '//*[@id="shop"]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/div/span[3]/div[2]')
            footwear_sizes_list = footwear_sizes.find_elements_by_class_name('active-indicator')

            for footwear_size in footwear_sizes_list:
                if footwear_size.text in self.shoe_sizes:
                    footwear_size.click()
                time.sleep(1)

        elif self.item_type == "Bottoms":
            size_type_buttons[1].click()
            pants_sizes = self.driver.find_element_by_xpath(
                '//*[@id="shop"]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/div/span[2]/div[2]')
            pants_sizes_list = pants_sizes.find_elements_by_class_name('active-indicator')

            for pant_size in pants_sizes_list:
                if pant_size.text in self.pants_sizes:
                    pant_size.click()
                time.sleep(1)

        elif self.item_type == "Tailoring":
            size_type_buttons[3].click(0)
            tailoring_sizes = self.driver.find_element_by_xpath(
                '//*[@id="shop"]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/div/span[4]/div[2]')
            tailoring_sizes_list = tailoring_sizes.find_elements_by_class_name('active-indicator')

            for tailoring_size in tailoring_sizes_list:
                if tailoring_size.text in self.tailoring_sizes:
                    tailoring_size.click()
                time.sleep(1)

        else:
            size_type_buttons[4].click()
            accessories_sizes = self.driver.find_element_by_xpath(
                '//*[@id="shop"]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/div/span[5]/div[2]')
            accessories_sizes_list = accessories_sizes.find_elements_by_class_name('active-indicator')

            for accessories_size in accessories_sizes_list:
                if accessories_size.text in self.accesories_sizes:
                    accessories_size.click()
                time.sleep(2)

    def scrape_product(self):

        urls = []
        prices = []
        descriptions = []
        shipping_costs = []
        user_ratings = []

        item = self.item

        with open(item + '.csv', 'w', newline='', encoding='utf-8') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(
                ['Product Number', 'Price ($)', 'Shipping Price ($)', 'Total Price ($)', 'Description', 'Seller Rating',
                 'URL'])

        self.driver.get(self.grailed_url)

        # Searches for item in search bar
        search_input = self.driver.find_element_by_id("globalheader_search")
        time.sleep(2)
        search_input.send_keys(item)

        time.sleep(2)

        search_button = self.driver.find_element_by_xpath('//*[@id="globalHeader"]/div/div[1]/div[2]/div[1]/button')
        search_button.click()

        time.sleep(5)

        if self.item_type != "None of the above":
            self.input_user_specs()

        # script which auto scrolls until very end of the page so that all products will load
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while (match == False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True

        time.sleep(2)

        # parses html for each feed item to get the URLs
        feed_items = self.driver.find_elements_by_class_name('feed-item')
        for feed_item in feed_items:
            soup = BeautifulSoup(feed_item.get_attribute("innerHTML"), 'lxml')
            link = soup.find('a')
            if link == None:
                break
            finallink = "https://www.grailed.com" + (link.get('href'))
            urls.append(finallink)

        for url in urls:
            self.driver.get(url)
            price = self.get_product_price(url)
            prices.append(price)

            description = self.get_product_description(url)
            descriptions.append(description)

            shipping_cost = self.get_shipping_price(url)
            shipping_costs.append(shipping_cost)

            user_rating = self.get_user_rating(url)
            user_ratings.append(user_rating)

            listing_number = get_listing_number(url)

            with open(item + '.csv', 'a', newline='', encoding='utf-8') as add_file:
                csv_writer = csv.writer(add_file)
                csv_writer.writerow(
                    [listing_number, price, shipping_cost, int(price) + int(shipping_cost), description, user_rating,
                     url])

        self.driver.close()
        return prices, shipping_costs, descriptions, user_ratings, urls

    def get_product_price(self, url):

        time.sleep(2)

        price = "Not Available"

        try:
            price = self.driver.find_elements_by_class_name("-price _has-drops").text
        except:
            pass

        try:
            price = self.driver.find_element_by_class_name("-price").text
        except:
            pass

        if price != "Not Available":
            price = int(price[1:])

        return price

    def get_product_description(self, url):

        time.sleep(2)

        description = "Not Available"

        try:
            description = self.driver.find_element_by_class_name('listing-description')

        except:
            pass

        if description != "Not Available":
            soup = BeautifulSoup(description.get_attribute("innerHTML"), 'lxml')
            paragraphs = soup.findAll('p')
            description = []
            for paragraph in paragraphs:
                description.append(paragraph.getText())

            final_description = "\n".join(description)

        return final_description

    def get_shipping_price(self, url):

        shipping_price = 0

        time.sleep(2)

        try:
            shipping_price = self.driver.find_element_by_class_name('-shipping-cost').text
        except:
            pass

        if shipping_price == "N/A":
            shipping_price = 0

        if shipping_price != 0:
            shipping_price = int(shipping_price[2:])

        return shipping_price

    def get_user_rating(self, url):

        user_feedback = "Not Available"

        #self.driver.get(url)
        time.sleep(2)

        # hides the footer which sometimes covers the user rating
        annoying_footer = self.driver.find_element_by_xpath('//*[@id="trust_sticky_footer"]/div')
        self.driver.execute_script("arguments[0].style.visibility='hidden'", annoying_footer)

        # Hovers over the stars which will allow the user rating to pop up
        try:
            user_rating_button = self.driver.find_element_by_xpath(
                '/html/body/div[7]/div[2]/div[1]/div[3]/div[6]/div[2]/a[1]/div')
            hover = ActionChains(self.driver).move_to_element(user_rating_button)
            hover.perform()

        except:
            pass

        time.sleep(2)

        try:
            user_feedback = self.driver.find_element_by_class_name('react-tooltip-lite').get_attribute('innerHTML')
        except:
            pass

        if user_feedback != "Not Available":
            slash_index = user_feedback.find("/")
            user_feedback = float(user_feedback[0:slash_index])
        return user_feedback

class Product_Tracker(Grailed_Bot):

    def __init__(self, listingnumber):
        self.listingnumber = listingnumber
        self.url = 'https://www.grailed.com/listings/' + str(listingnumber)

        chromedriver = "C:\\Users\\Lu\\Downloads\\chromedriver_win32\\chromedriver.exe"
        self.driver = webdriver.Chrome(chromedriver)

    def scrape_product(self):
        self.driver.get(self.url)

        print(self.url)
        price = self.get_product_price(self.url)

        description = self.get_product_description(self.url)

        shipping_cost = self.get_shipping_price(self.url)

        user_rating = self.get_user_rating(self.url)

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")

        with open(self.listingnumber + '.csv', 'a', newline='', encoding='utf-8') as add_file:
            csv_writer = csv.writer(add_file)
            csv_writer.writerow(
                [str(current_time), price, shipping_cost, int(price) + int(shipping_cost), description,
                 user_rating])

        self.driver.close()


# function to get the listing number of a product
def get_listing_number(url):
    listingnumber = ""
    index = 0

    for i in range(0, len(url)):
        if url[i].isdigit():
            index = i
            break

    for i in range(index, len(url)):
        if url[i].isdigit():
            listingnumber += url[i]
        else:
            break

    return listingnumber


# generates a csv file for a product with the corresponding listing number
def generate_csv(listingnumber):
    with open(listingnumber + '.csv', 'w', newline='', encoding='utf-8') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(
            ['date', 'price', 'shipping price', 'total price', 'description', 'user rating'])
