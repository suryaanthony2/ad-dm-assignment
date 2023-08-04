import types
import typing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://www.mobbi.id/"

class Mobbi(webdriver.Chrome):
    def __init__(self, teardown=True):
        options = Options()
        if teardown == False:
            options.add_experimental_option("detach", True)
        super(Mobbi, self).__init__(options=options)

    def land_first_page(self):
        self.get(url)

    def close_popup(self):
        popup = self.find_element(
            By.ID,
            'btnwClear'
        )
        popup.click()

    def click_textbox(self):
        text_element = self.find_element(
            By.XPATH,
            '//*[@id="headerNonIbid"]/li/div/div/form/div/div[1]/input[1]'
        )
        text_element.click()

    def select_brand(self, index):
        brand_element = self.find_element(
            By.XPATH,
            f'//*[@id="list-brand-search"]/li[{index}]/a'
        )
        brand_element.click()

    def inf_scroll(self):
        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = self.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_page(self,scroll_height=200):
        self.execute_script(f"window.scrollBy(0, {scroll_height})")


    def get_elements(self):
        car_elements = self.find_elements(
            By.CSS_SELECTOR,
            'div[class="featured-car-product for-compare-button no-rounded-bottom"]'
        )
        return car_elements

    def get_elements_link(self, cars):
        car_elements_link = map(lambda el: el.find_element(By.TAG_NAME, 'a'), cars)
        return car_elements_link

    def get_car_information(self):
        car_info = {}

        try:
            second_card_information = self.find_element(
                By.XPATH,
                '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/ul/li[2]'
            )
        except:
            return None

        time.sleep(2)
        
        self.scroll_page(scroll_height=1000)

        time.sleep(2)

        car_brand = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/p'
        ).text

        car_price = self.find_element(
            By.XPATH,
            '//*[@id="data360"]/div/div[3]/div/div[2]/div/label'
        ).text

        car_model = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/p'
        ).text

        car_variant = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[3]/div[1]/div/div[2]/p'
        ).text

        car_year = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/p'
        ).text

        car_transmission = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/p'
        ).text

        car_mileage = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[3]/div[2]/div/div[2]/p'
        ).text

        car_color = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[1]/div[4]/div[2]/div/div[2]/p'
        ).text

        second_card_information.click()

        car_location = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/p'
        ).text

        car_engine_capacity = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[2]/div[3]/div[1]/div/div[2]/p'
        ).text

        car_fuel = self.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/main/div[17]/section[1]/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/p'
        ).text

        car_info['car_brand'] = car_brand
        car_info['car_model'] = car_model
        car_info['car_variant'] = car_variant
        car_info['car_price'] = car_price
        car_info['car_transmission'] = car_transmission
        car_info['car_mileage'] = car_mileage
        car_info['car_year'] = car_year
        car_info['car_color'] = car_color
        car_info['car_location'] = car_location
        car_info['car_engine_capacity'] = car_engine_capacity
        car_info['car_fuel'] = car_fuel

        return car_info
    
    def car_page(self, index):
        car_page = self.find_element(
                By.XPATH,
                f'/html/body/div[2]/div/main/div[16]/div/div/div/section[1]/div[3]/div[1]/div[3]/div[2]/div[3]/div[{index}]/div'
        )
        car_brand = car_page.get_attribute('data-product-brand')
        if car_brand == None:
            return False
        return car_page

    def go_back(self):
        self.back()

    def get_number_of_cars(self):
        num_cars = self.find_element(
            By.XPATH,
            '//*[@id="search-results-details"]/div/div/div[2]/div[1]/div/div[1]/span'
        ).text
        num_cars = int(num_cars.split(" ")[0])
        return num_cars

    def change_currency_usd(self):
        currency_element = self.find_element(
            By.CSS_SELECTOR, 
            'button[data-testid="header-currency-picker-trigger"]'
        )
        currency_element.click()
        selected_currency_element = self.find_element(
            By.CSS_SELECTOR, 
            'button[class="fc63351294 ea925ef36a bf97d4018a ae8177da1f cddb75f1fd"]'
        )
        selected_currency_element.click()
        
    def place_to_go(self, place):
        place_input_text = self.find_element(
            By.ID,
            ":rc:"
        )
        place_input_text.send_keys(place)
        self.implicitly_wait(20)
        suggestion = self.find_element(
            By.XPATH,
            f"//li//div[contains(text(), {place})]/ancestor::div[@role='button']"
        )

        print(f"//li//div[contains(text(), {place})]/ancestor::div[@role='button']")
        suggestion.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            By.XPATH,
            f'//span[@data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.find_element(
            By.XPATH,
            f'//span[@data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(
            By.CSS_SELECTOR,
            'button[data-testid="occupancy-config"]'
        )
        selection_element.click()

        decrease_adult = self.find_element(
            By.CSS_SELECTOR,
            'button[class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 cd7aa7c891"]'
        )

        increase_adult = self.find_element(
            By.CSS_SELECTOR,
            'button[class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 d64a4ea64d"]'
        )
        while True:
            decrease_adult.click()

            adult_count_element = self.find_element(
                By.ID,
                'group_adults'
            )
            adult_count = adult_count_element.get_attribute('value')

            if int(adult_count) == 1:
                break

        for _ in range(count - 1):
            increase_adult.click()

    def click_select(self):
        search_element = self.find_element(
            By.CSS_SELECTOR,
            'button[class="fc63351294 a822bdf511 d4b6b7a9e7 cfb238afa1 c938084447 f4605622ad aa11d0d5cd"]'
        )
        search_element.click()