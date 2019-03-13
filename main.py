import requests
from bs4 import BeautifulSoup
from base64 import b64decode
import re
import json


class Car:
    def __init__(self, dealer, year, model, trim, miles, price, vin):
        self.dealership_name = dealer
        self.model_year = year
        self.model_name = model
        self.trim_level_name = trim
        self.odometer_miles = miles
        self.price = price
        self.vin = vin

    def __str__(self):
        return f"{self.model_year} {self.model_name} {self.trim_level_name}, {self.odometer_miles}mi, ${self.price} from {self.dealership_name} VIN={self.vin}"

    def get_csv_row(self):
        return f"{self.model_year},{self.model_name},{self.trim_level_name},{self.odometer_miles},{self.price},{self.dealership_name},{self.vin}\n"


def main():
    """
    Automatically scrapes data about used Camrys and Accords from the websites of dealerships in the San Fransisco Bay
    Area.

    Some dealerships use the same software to run their online listings. We can identify this because the website URLs
    have similar structures. 
    """
    all_cars = []
    scrape_type_used_inventory(all_cars)
    scrape_type_vehicle_category_used_vehicles(all_cars)
    scrape_type_used_tp(all_cars)
    scrape_type_searchused_dot_aspx(all_cars)
    scrape_capitol_honda(all_cars)
    scrape_ocean_honda_burlingame(all_cars)
    scrape_putnam_toyota(all_cars)

    with open("output.csv", "w") as f:
        f.write("year,model,trim,miles,price,dealer,vin\n")
        for car in all_cars:
            f.write(car.get_csv_row())


def scrape_putnam_toyota(all_cars):
    """
    Scrapes used Camry listings from the Putnam Toyota website and adds them to the given list of cars.

    :param all_cars: list of cars scraped so far in this run.
    """
    url = "http://www.putnamtoyota.com/toyota-used-cars-bay-area/refineChange/1/100/~/VehicleType_~Price1_~Make_Toyota~Model_/Model/Camry"
    dealer = "putnamtoyota"
    print(f"scraping {url} ...", end="", flush=True)
    request = requests.get(url, headers={"User-agent": "Python requests"})
    request.raise_for_status()
    soup = BeautifulSoup(request.text, "html.parser")

    cars_on_this_url = []
    for div in soup.select("div.vehicleRow"):
        price = re.sub("[^0-9]", "", div.select("span.special-price-value")[0].get_text())
        if not price:
            continue
        miles = re.sub("[^0-9]", "", div.select("div.vehicleInfo span")[1].get_text().replace(",", ""))
        vin = div.select("input")[0]["value"].split("/")[-1:][0]

        info = div.select("h2")[0].get_text().split(" ")
        year = info[0]
        model = info[2]
        trim = " ".join(info[3:])

        new_car = Car(dealer, year, model, trim, int(miles), int(price), vin)
        cars_on_this_url.append(new_car)

    print(f"got {len(cars_on_this_url)} cars from " + dealer)

    # other_pages = soup.select("div.pagination-control li:not(.label):not(.active) a")
    # if other_pages:
    #     other_pages_top_only = other_pages[:len(other_pages) / 2]

    all_cars.extend(cars_on_this_url)


def scrape_ocean_honda_burlingame(all_cars):
    """
    Scrapes used Accord listings from the Ocean Honda of Burlingame website and adds them to the given list of cars.

    :param all_cars: list of cars scraped so far in this run.
    """
    # url = "https://oceanhondaburlingame.com/wp-content/plugins/rev-trunk/_ajax.php?condition=used&make=Honda&model=Accord+Sedan&json=true&show=10&offset=0"
    url = "https://oceanhondaburlingame.com/wp-content/plugins/r3/_ajax.php?json=true&output=victory-inventory-index&stock=57R04610,57R04607,57R06007,57R04617,57R05039,57R07026,57R05002,57R05030&sort=year-DESC"
    dealer = "oceanhondaburlingame"
    print(f"scraping {url} ...", end="", flush=True)
    request = requests.get(url, headers={"User-agent": "Python requests"})
    request.raise_for_status()
    soup = BeautifulSoup(json.loads(request.text)["view"], "html.parser")

    cars_on_this_url = []
    for div in soup.select("div.col-md-12.mobList"):
        year = div.select("span.year")[0].get_text()
        model = div.select("span.model")[0].get_text()
        price = div.select("span.price")[0].get_text().replace(",", "")
        miles = div.select("span.mileage")[0].get_text().replace(",", "")
        trim = div.select("span.listModel")[0].get_text()
        vin = div.select("li")[2].get_text().replace("VIN: ", "")  # check this

        new_car = Car(dealer, year, model, trim, int(miles), int(price), vin)
        cars_on_this_url.append(new_car)

    print(f"got {len(cars_on_this_url)} cars from " + dealer)

    all_cars.extend(cars_on_this_url)


def scrape_capitol_honda(all_cars):
    """
    Scrapes used Accord listings from the Capitol Honda website and adds them to the given list of cars.

    :param all_cars: list of cars scraped so far in this run.
    """
    url = "http://www.capitolhonda.com/inventory.aspx?_used=true&_cpo=true&_makef=honda&_model=accord+sedan"
    dealer = "capitolhonda"
    print(f"scraping {url} ...", end="", flush=True)
    request = requests.get(url)
    request.raise_for_status()
    soup = BeautifulSoup(request.text, "html.parser")

    cars_on_this_url = []
    for div in soup.select("div.srp-vehicle-block"):
        name = div.select("h2.ebiz-vdp-title a")[0].get_text().split(" ")
        year = name[0]
        model = name[2]
        trim = div.select("h3.ebiz-vdp-subtitle")[0].get_text()

        price = re.sub("[^0-9]", "", div.select("h4.money-sign-disp")[0].get_text())
        vin = div.select("li")[6].get_text().replace("VIN #: ", "")
        miles = re.sub("[^0-9]", "", div.select("li.mileage-units")[0].get_text().split(": ")[1])

        new_car = Car(dealer, year, model, trim, int(miles), int(price), vin)
        cars_on_this_url.append(new_car)

    print(f"got {len(cars_on_this_url)} cars from " + dealer)

    # other_pages = soup.select("div.pagination-control li:not(.label):not(.active) a")
    # if other_pages:
    #     other_pages_top_only = other_pages[:len(other_pages) / 2]

    all_cars.extend(cars_on_this_url)


def scrape_type_searchused_dot_aspx(all_cars):
    """
    Scrapes used car listings from dealership websites which have "searchused.aspx" in the URL.

    Four dealerships are scraped:
    * Anderson Honda
    * Honda Redwood City, which has since been renamed Primo Honda
    * Capitol Toyota

    :param all_cars: list of cars scraped so far in this run.
    """

    def add_cars_from_url(dealership_name, url):
        """
        Scrapes cars from a dealership website where the URL contains "searchused.aspx", and adds them to the list of
        all cars scraped in this run.

        :param dealership_name: name of the dealer
        :param url: location of the webpage to scrape
        """
        print(f"scraping {url} ...", end="", flush=True)
        request = requests.get(url, headers={"User-agent": "Python requests"})
        request.raise_for_status()
        soup = BeautifulSoup(request.text, "html.parser")

        cars_on_this_url = []
        for div in soup.select("div.row.srpVehicle"):
            price = None
            if dealership_name == "andersonhonda":
                price = re.sub("[^0-9]", "", div.select("li.internetPrice span.pull-right")[0].get_text())
            else:
                price = re.sub("[^0-9]", "", div.select("span.primaryPrice")[0].get_text())
            miles = re.sub("[^0-9]", "", div.select("li.mileageDisplay")[0].get_text().split(": ")[1])
            vin = div.select("li.vinDisplay")[0].get_text().split(": ")[1]
            vehicle_title = div.select("h2.vehicleTitle")[0].get_text().strip()
            split_on_space = vehicle_title.split(" ")
            if split_on_space[2] == "Camry":
                model = split_on_space[2]
            elif split_on_space[2] == "Accord":
                model = split_on_space[2] + " " + split_on_space[3]
            year = split_on_space[0]
            trim = vehicle_title.split(model)[1].strip()
            new_car = Car(dealership_name, year, model, trim, int(miles), int(price), vin)
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars from " + dealership_name)
        all_cars.extend(cars_on_this_url)

    add_cars_from_url("andersonhonda",
                      "http://www.andersonhonda.com/searchused.aspx?Make=Honda&Model=Accord+Sedan&pn=100")

    # honda-rc.com lists "Accord Sedan" and "Accord Sdn" separately, which is silly
    add_cars_from_url("honda-rc", "http://www.honda-rc.com/searchused.aspx?Make=Honda&Model=Accord+Sedan&pn=100")
    add_cars_from_url("honda-rc", "http://www.honda-rc.com/searchused.aspx?Make=Honda&Model=Accord+Sdn&pn=100")

    add_cars_from_url("capitoltoyota", "http://www.capitoltoyota.com/searchused.aspx?Make=Toyota&Model=Camry&pn=100")


def scrape_type_used_tp(all_cars):
    """
    Scrapes used car listings from dealership websites with URLs of the form:
    http://www.<domain>.com/search/used-<make_name>-<model_name>/tp-mk<make_code>-md<model_code>/c:<results_per_page>/

    where:
    * <domain> is "fremonttoyota", "pierceytoyota", or "larryhopkinshonda"
    * <make_name> is "toyota" or "honda"
    * <model_name> is "camry" or "accord"
    * <make_code> and <model_code> are chosen by the dealership
    * <results_per_page> is how many search results to display at a time, maximum 50

    I don't know what "tp" in the URL stands for.

    :param all_cars: list of cars scraped so far in this run.
    """

    def add_cars_from_url(base, url):
        """
        Scrapes cars from a dealership website where the URL contains "/tp-mk". See parent function for detailed
        description of the form of the URL.

        :param dealership_name: name of the dealer
        :param url: location of the webpage to scrape
        """
        print(f"scraping {url} ...", end="", flush=True)
        request = requests.get(url, headers={"User-agent": "Python requests"})
        request.raise_for_status()
        soup = BeautifulSoup(request.text, "html.parser")

        cars_on_this_url = []
        for div in soup.select("div.srp_vehicle_item_container"):
            try:
                price = int(div.select('meta[itemprop="price"]')[0]["content"])
            except IndexError:
                continue

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
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars")
        all_cars.extend(cars_on_this_url)

    for dealer in ["fremonttoyota", "pierceytoyota"]:
        add_cars_from_url(dealer, "http://www." + dealer + ".com/search/used-toyota-camry/tp-mk63-md300/c:50/")

    add_cars_from_url("larryhopkinshonda",
                      "http://www.larryhopkinshonda.com/search/used-honda-accord/tp-mk23-md124/c:50/")


def scrape_type_vehicle_category_used_vehicles(all_cars):
    """
    Scrapes used car listings from dealership websites which have "/vehicle-categories/used-vehicles/" in the URL.

    Two dealerships are scraped:
    * South Bay Honda
    * City Toyota

    :param all_cars: list of cars scraped so far in this run.
    """

    def add_cars_from_url(base, url, is_toyota):
        """
        Scrapes cars from a dealership website where the URL contains "/vehicle-categories/used-vehicles/", and adds
        them to the list of all cars scraped in this run.

        :param dealership_name: name of the dealer
        :param url: location of the webpage to scrape
        """
        print(f"scraping {url} ...", end="", flush=True)
        request = requests.get(url)
        request.raise_for_status()
        soup = BeautifulSoup(request.text, "html.parser")

        cars_on_this_url = []
        for article in soup.select("article"):
            if is_toyota:
                price = int(re.sub("[^0-9]", "", article.select("tr.vehicle-math-price td.value")[0].get_text()))
                vin = article.select("span.vehicle-details-specs")[0].get_text().split("|")[2].replace("VIN:", "") \
                    .strip()
            else:
                price = int(re.sub("[^0-9]", "", article.select("p.vehicle-price-final span.value")[0].get_text()))
                vin = article.select("span.description")[0].get_text().split("|")[2].replace("VIN:", "").strip()
            new_car = Car(base, int(article["data-model-year"]), article["data-model"], article["data-model-trim"],
                          int(article["data-mileage"]), price, vin)
            if price > 1000000:
                print(f"skipping {new_car} because price too high")
                continue
            cars_on_this_url.append(new_car)

        print(f"got {len(cars_on_this_url)} cars")
        all_cars.extend(cars_on_this_url)

    add_cars_from_url("southbayhonda",
                      "http://www.southbayhonda.com/vehicle-category/used-vehicles/?make=Honda&model=Accord", False)
    add_cars_from_url("citytoyota",
                      "http://www.citytoyota.com/vehicle-categories/used-vehicles/used-cars/?make=Toyota&model=Camry",
                      True)


def scrape_type_used_inventory(all_cars):
    """
    Scrapes used car listings from dealership websites which have "/used-inventory/" in the URL.

    Two dealerships are scraped:
    * South Bay Honda
    * City Toyota

    :param all_cars: list of cars scraped so far in this run.
    """

    def add_cars_from_url(base, url):
        """
        Scrapes cars from a dealership website where the URL contains "/used-inventory/", and adds
        them to the list of all cars scraped in this run.

        :param dealership_name: name of the dealer
        :param url: location of the webpage to scrape
        """
        print(f"scraping {url} ...", end="", flush=True)
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        cars_on_this_url = []
        for div in soup.select("div.hproduct"):
            mileage = int(
                re.sub("[^0-9]", "", div.find(lambda e: e.text == "Mileage:").find_next_sibling("dd").get_text()))
            new_car = Car(base, int(div["data-year"]), div["data-model"], div["data-trim"], mileage,
                          round(float((b64decode(div["data-internetprice"])))), div["data-vin"])
            if mileage < 10:
                print(f"skipping {new_car} because mileage too low")
                continue
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


main()
