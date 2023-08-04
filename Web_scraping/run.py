from booking.booking import Booking
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

def run_automation():
    booking = Booking(teardown=False)
    booking.land_first_page()
    booking.implicitly_wait(20)

    booking.close_popup()
    booking.change_currency_usd()
    booking.place_to_go("Jakarta")
    booking.select_dates("2023-08-20", "2023-08-28")
    booking.select_adults(count=4)
    booking.click_select()

    return booking.current_url

def scrape(url):
    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, "lxml")

    with open("example.txt", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    listing = soup.find_all("div", attrs={"data-testid": "property-card"})

    print()
    
    for li in listing:
        li_info = {}

        review_score = li.find("div", class_="b5cd09854e d10a6220b4").text
        
        hotel_name = li.find("div", class_="fcab3ed991 a23c043802").text

        hotel_link = li.find("a", attrs={"data-testid": "title-link"})["href"]

        #hotel_price = li.find("span", class_="fcab3ed991 fbd1d3018c e729ed5ab6").text


        print(f"{hotel_name} has a score of {review_score}")
        print(f"link: {hotel_link}")
        print("")

current_url = run_automation()

time.sleep(10)

scrape(current_url)