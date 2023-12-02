from threading import Thread
import requests
import time

import json


def get(url):
    while True:
        try:
            return requests.get(url)
        except:
            pass


class Tenant:
    def __init__(self, json):
        self.json = json
        self.__process(json)

    def __process(self, json):
        self.name = json["name"].replace("  ", " ")

        address = json["addresses"][0]
        self.label = address["label"]
        self.postcode = address["postcode"]
        self.area = address["area"]

        if "dateOfBirth" in json:
            self.birth_date = json["dateOfBirth"]
        else:
            self.birth_date = None

        self.gs_page = json["links"][0]["href"]

        self.phone_number = json["phoneNumbers"]


class Address:
    def __init__(self, json):
        self.json = json
        self.__process(json)

    def __process(self, json):
        self.tentants = []


class Company:
    def __init__(self, json):
        self.json = json
        self.__process(json)

    def __process(self, json):
        self.eniro_id = json["eniroId"]
        self.name = json["name"]
        self.phones = json["phones"] if "phones" in json else []
        self.primary_number = json["phones"][0]["number"] if "phones" in json else None
        self.addresses = json["addresses"]
        self.categories = json["categories"]


class Person:
    def __init__(self, json):
        self.json = json
        self.__process(json)

    def __process(self, json):
        self.eniro_id = json["eniroId"]
        self.name = json["name"]
        self.first_name = json["name"]["firstName"]
        self.middle_name = json["name"]["middleName"]
        self.last_name = json["name"]["lastName"]
        self.full_name = " ".join(
            [
                part.strip()
                for part in [self.first_name, self.middle_name, self.last_name]
                if part is not None
            ]
        )
        self.phones = json["phones"]
        self.primary_number = json["phones"][0]["number"]
        self.addresses = json["addresses"]
        self.proffesion = json["proff"]
        self.legal_name = json["nameLegal"]
        self.birth_date = json["birthDate"]
        self.no_address = False
        self.no_full_address = False
        self.full_address = None

        if len(json["addresses"]) == 0:
            self.no_address = True
            return

        self.address_street_name = (
            json["addresses"][0]["streetName"]
            if json["addresses"][0]["streetName"] != None
            else ""
        )
        self.address_street_number = (
            json["addresses"][0]["streetNumber"]
            if json["addresses"][0]["streetNumber"] != None
            else ""
        )
        self.address_postal_code = (
            json["addresses"][0]["postalCode"]
            if json["addresses"][0]["postalCode"] != None
            else ""
        )
        self.address_postal_area = (
            json["addresses"][0]["postalArea"]
            if json["addresses"][0]["postalArea"] != None
            else ""
        )

        self.no_full_address = len(json["addresses"][0]["coordinates"]) == 0
        self.full_address = f"{self.address_street_name} {self.address_street_number} {self.address_postal_code} {self.address_postal_area}".replace(
            "  ", ""
        )


class GS_Response:
    def __init__(self, json):
        json = json["pageProps"]["initialState"]

        self.json = json
        self.__process(json)

    def __process(self, json):
        self.company_hits = json["hits"]["companies"]
        self.person_hits = json["hits"]["persons"]
        self.total_hits = self.company_hits + self.person_hits

        self.companies = []

        for company in json["companies"]:
            self.companies.append(Company(company))

        self.persons = []

        for person in json["persons"]:
            self.persons.append(Person(person))

        self.search_page = json["searchPage"]


class GuleSider:
    def __init__(self):
        self.max_pages = 100
        pass

    def __get_response(self, query, page, pages):
        if self.STOP != 0:
            return
        res = get(
            f"https://www.gulesider.no/_next/data/{self.data_token}/nb/search/{query}/persons/{page}.json?searchType=persons"
        )
        json = res.json()
        if "initialState" not in json["pageProps"]:
            self.STOP = -1
            return
        res = GS_Response(json)
        pages.append(res)
        self.completed_pages.append(page)
        self.completed_pages.sort()
        if res.search_page * 25 > res.total_hits and self.STOP == 0:
            self.STOP = page

    def search_address(self, address):
        url = f"https://mapsearch.eniro.com/search/search.json?index=wp&profile=no&q={address}&reverseLookup=true"

        res = get(url)

        json = res.json()["search"]

        tenants = []

        if "wp" in json:
            for item in json["wp"]["features"]:
                tenants.append(Tenant(item))

        return tenants

    def search(self, query, safe):
        pages = []

        self.STOP = 0
        self.completed_pages = []

        html = get("https://www.gulesider.no/{query}/bedrifter").text

        self.data_token = html[
            html.find("/_buildManifest.js") - 21 : html.find("/_buildManifest.js")
        ]

        threads = []

        for page in range(1, self.max_pages):
            if self.STOP == 0:
                th = Thread(target=self.__get_response, args=[query, page, pages])
                th.start()
                threads.append(th)

            time.sleep(0.05)

            if (
                self.STOP == -1
                or self.STOP != 0
                and (
                    len(self.completed_pages) > self.STOP
                    and self.completed_pages[self.STOP - 1] == self.STOP
                    or not safe
                )
            ):
                # print(f"Finished processing {self.STOP} pages in {round((time.time()-start)*1000)}ms!")
                break

        if safe and self.STOP != -1:
            for thread in threads:
                thread.join()

        return pages


if __name__ == "__main__":
    gule_sider = GuleSider()

    pages = gule_sider.search("Ballestas", False)

    for page in pages:
        for person in page.persons:
            print("FLN: " + person.full_name)
            print("TLF: " + person.primary_number)
