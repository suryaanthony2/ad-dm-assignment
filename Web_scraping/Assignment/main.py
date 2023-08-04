from mobbi import Mobbi
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import pandas as pd

columns = ['car_brand',
           'car_model', 
           'car_variant', 
           'car_price', 
           'car_transmission', 
           'car_mileage',
           'car_year',
           'car_location',
           'car_link'
           ]

df = pd.DataFrame(columns=columns)

def find_cars(cars):
    df = pd.DataFrame(columns=columns)
    for car in cars:
        car_info = {}
        car_brand = car.get_attribute('data-product-brand')
        if car_brand == None:
            continue
        car_model = car.get_attribute('data-product-category')
        car_variant = car.get_attribute('data-product-variant')
        car_price = int(float(car.get_attribute('data-product-price')))
        car_transmission = car.get_attribute('data-product-transmission')
        car_mileage = int(car.get_attribute('data-product-mileage'))
        car_year = int(car.get_attribute('data-product-year'))
        car_location = car.get_attribute('data-product-location')
        car_link = car.find_element(
            By.TAG_NAME,
            "a"
        ).get_attribute('href')

        car_info['car_brand'] = car_brand
        car_info['car_model'] = car_model
        car_info['car_variant'] = car_variant
        car_info['car_price'] = car_price
        car_info['car_transmission'] = car_transmission
        car_info['car_mileage'] = car_mileage
        car_info['car_year'] = car_year
        car_info['car_location'] = car_location
        car_info['car_link'] = car_link

        df.loc[len(df)] = car_info
    return df

mobbi = Mobbi(teardown=False)

mobbi.land_first_page()
mobbi.close_popup()
mobbi.select_brand(1)
mobbi.inf_scroll()
cars = mobbi.get_elements()

df = find_cars(cars)
df.to_csv("out.csv", index=False)