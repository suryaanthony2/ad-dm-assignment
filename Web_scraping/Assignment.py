from bs4 import BeautifulSoup
import requests

def find_cars():
    url = "https://www.mobbi.id/cari-mobil?q=%3Arelevance%3AproductStatus%3ASiap%2BPakai%3AGrade%3Amobbi%2BCertified%2BA%3AGrade%3Amobbi%2BCertified%2BB%3AGrade%3Amobbi%2BCertified%2BC&utm_source=sem&utm_medium=PaidSearch-SEM&utm_campaign=SEM_union_mo88i_selling_brand_mobbi&utm_content=SEM_union_mo88i_selling_brand_mobbi+&utm_term=mobbi&network=g&matchtype=e&adposition=&device=c&gclid=Cj0KCQjw2qKmBhCfARIsAFy8buI_5tDWgBdp3MSjUAXSh-uUFFPTRYlgmCmRQWyBM-Ogbj0jBA89VHoaAglWEALw_wcB"

    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, "lxml")
    
    cars = soup.find_all('div', class_="featured-car-product for-compare-button no-rounded-bottom")

find_cars()