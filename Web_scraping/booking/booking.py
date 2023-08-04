import types
import typing
from selenium import webdriver
import booking.constants as const
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Booking(webdriver.Chrome):
    def __init__(self, teardown=True):
        options = Options()
        if teardown == False:
            options.add_experimental_option("detach", True)
        super(Booking, self).__init__(options=options)

    def land_first_page(self):
        self.get(const.BASE_URL)

    def close_popup(self):
        popup = self.find_element(
            By.CSS_SELECTOR,
            'button[class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 ae1678b153"]'
        )
        popup.click()

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