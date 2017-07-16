import requests
from bs4 import BeautifulSoup
from base64 import b64decode
import re


class Car:
    def __init__(self, dealer, year, model, trim, miles, price, vin):
        self.dealer = dealer
        self.year = year
        self.model = model
        self.trim = trim
        self.miles = miles
        self.price = price
        self.vin = vin

    def __str__(self):
        return f"{self.year} {self.model} {self.trim}, {self.miles}mi, ${self.price} from {self.dealer} VIN={self.vin}"


def main():
    # scrape_website_type_used_inventory()
    # scrape_website_type_vehicle_category()
    # scrape_website_type_used_tp()
    scrape_website_type_searchused_aspx()


def scrape_website_type_searchused_aspx():
    def add_cars_from_url(base, url):
        print(f"scraping {url} ...", end="", flush=True)
        headers_dict = {"User-agent": "Python requests"}
        r = requests.get(url, headers=headers_dict)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        cars_on_this_url = []
        for div in soup.select("div.row.srpVehicle"):
            price = re.sub("[^0-9]", "", div.select("span.primaryPrice")[0].get_text())
            miles = re.sub("[^0-9]", "", div.select("li.mileageDisplay")[0].get_text().split(": ")[1])
            vin = re.sub("[^0-9]", "", div.select("li.vinDisplay")[0].get_text().split(": ")[1])
            vehicle_title = div.select("h2.vehicleTitle")[0].get_text().strip()
            split_on_space = vehicle_title.split(" ")
            if split_on_space[2] == "Camry":
                model = split_on_space[2]
            elif split_on_space[2] == "Accord":
                model = split_on_space[2] + " " + split_on_space[3]
            year = split_on_space[0]
            trim = vehicle_title.split(model)[1].strip()
            new_car = Car(base, year, model, trim, int(miles), int(price), vin)
            # print(f"added {new_car}")
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars from " + base)
        all_cars.extend(cars_on_this_url)

    for base in ["honda-rc", "andersonhonda"]:
        add_cars_from_url(base, "http://www." + base + ".com/searchused.aspx?Make=Honda&Model=Accord+Sedan&pn=100")
    add_cars_from_url(base, "http://www.honda-rc.com/searchused.aspx?Make=Honda&Model=Accord+Sdn&pn=100")
    add_cars_from_url("capitoltoyota", "http://www.capitoltoyota.com/searchused.aspx?Make=Toyota&Model=Camry&pn=100")

    print(f"Done - {len(all_cars)} total cars scraped")


def scrape_website_type_used_tp():
    def add_cars_from_url(base, url):
        print(f"scraping {url} ...", end="", flush=True)
        headers_dict = {"User-agent": "Python requests"}
        r = requests.get(url, headers=headers_dict)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        cars_on_this_url = []
        for div in soup.select("div.srp_vehicle_item_container"):
            try:
                price = int(div.select('meta[itemprop="price"]')[0]["content"])
            except IndexError:
                price = -1

            try:
                item_offered = div.select('span[itemprop="itemOffered"]')[0]
            except IndexError:
                item_offered = div.select('span[itemprop="about"]')[0]
            year = item_offered.select('meta[itemprop="vehicleModelDate"]')[0]["content"]
            model = item_offered.select('meta[itemprop="model"]')[0]["content"]
            vin = item_offered.select('meta[itemprop="vehicleIdentificationNumber"]')[0]["content"]
            miles = re.sub("[^0-9]", "", div.select(
                "div.vehicle_details_cols span.details-overview_data")[0].get_text())
            trim = item_offered.select('meta[itemprop="name"]')[0]["content"].split(model)[1].strip()

            new_car = Car(base, year, model, trim, int(miles), int(price), vin)
            # print(f"added {new_car}")
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars")
        all_cars.extend(cars_on_this_url)

    for base in ["fremonttoyota", "pierceytoyota"]:
        add_cars_from_url("base", "http://www." + base + ".com/search/used-toyota-camry/tp-mk63-md300/c:50/")
    add_cars_from_url("larryhopkinshonda",
                      "http://www.larryhopkinshonda.com/search/used-honda-accord/tp-mk23-md124/c:50/")

    add_cars_from_url("larryhopkinshonda",
                      "http://www.larryhopkinshonda.com/search/used-honda-accord/tp-mk23-md124/c:50/")

    print(f"{len(all_cars)} cars scraped")


def scrape_website_type_vehicle_category():
    def add_cars_from_url(base, url, is_toyota):
        print(f"scraping {url} ...", end="", flush=True)
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        cars_on_this_url = []
        for article in soup.select("article"):
            if is_toyota:
                price = re.sub("[^0-9]", "", article.select("tr.vehicle-math-price td.value")[0].get_text())
                vin = article.select("span.vehicle-details-specs")[0].get_text().split("|")[2].replace("VIN:", "") \
                    .strip()
            else:
                price = re.sub("[^0-9]", "", article.select("p.vehicle-price-final span.value")[0].get_text())
                vin = article.select("span.description")[0].get_text().split("|")[2].replace("VIN:", "").strip()
            new_car = Car(base, int(article["data-model-year"]), article["data-model"], article["data-model-trim"],
                          int(article["data-mileage"]), int(price), vin)
            # print(f"added {new_car}")
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars")
        all_cars.extend(cars_on_this_url)

    add_cars_from_url("southbayhonda",
                      "http://www.southbayhonda.com/vehicle-category/used-vehicles/?make=Honda&model=Accord", False)
    add_cars_from_url("citytoyota",
                      "http://www.citytoyota.com/vehicle-categories/used-vehicles/used-cars/?make=Toyota&model=Camry",
                      True)
    print(f"{len(all_cars)} cars scraped")


def scrape_website_type_used_inventory():
    def add_cars_from_url(base, url):
        print(f"scraping {url} ...", end="", flush=True)
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        cars_on_this_url = []
        for div in soup.select("div.hproduct"):
            mileage = re.sub("[^0-9]", "", div.find(lambda e: e.text == "Mileage:").find_next_sibling("dd").get_text())
            new_car = Car(base, int(div["data-year"]), div["data-model"], div["data-trim"], int(mileage),
                          round(float((b64decode(div["data-internetprice"])))), div["data-vin"])
            # print(f"added {new_car}")
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars")
        all_cars.extend(cars_on_this_url)

        links_to_next_page = soup.select('ul.pagination a[rel="next"]')
        if links_to_next_page:
            add_cars_from_url(base, url.split("?")[0] + links_to_next_page[0]["href"])

    for url_base in ["melodytoyota", "toyotasunnyvale", "toyota101", "sftoyota", "autonationtoyotahayward"]:
        add_cars_from_url(url_base, "http://www." + url_base + ".com/used-inventory/index.htm?make=Toyota&model=Camry")

    for url_base in ["hondaofstevenscreek", "autonationhondafremont", "autonationhondafremont", "hondaofserramonte",
                     "sfhonda", "hondaofhayward"]:
        add_cars_from_url(url_base, "http://www." + url_base + ".com/used-inventory/index.htm?make=Honda&model=Accord")
    print(f"{len(all_cars)} cars scraped")


all_cars = []
main()
