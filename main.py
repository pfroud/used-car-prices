import requests
from bs4 import BeautifulSoup
from base64 import b64decode


class Car:
    def __init__(self, dealer, year, model, trim, miles, price):
        self.dealer = dealer
        self.year = year
        self.model = model
        self.trim = trim
        self.miles = miles
        self.price = price


def main():
    r = requests.get("https://www.toyotasunnyvale.com/used-inventory/index.htm?make=Toyota&model=Camry")
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    for div in soup.select("div.hproduct"):
        mileage = div.find(lambda e: e.text == "Mileage:").find_next_sibling("dd").get_text()
        car = Car("sunnyvale", int(div["data-year"]), div["data-model"], div["data-trim"], int(mileage),
                  float(b64decode(div["data-internetprice"])))

main()
