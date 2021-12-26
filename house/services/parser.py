import datetime
from dataclasses import dataclass
import typing
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


@dataclass
class House:
    commissioning_year: int or None
    number_of_floors: int
    last_modification_of_the_profile: datetime.datetime
    series_type_of_building_construction: str
    house_type: str
    house_is_emergency: bool
    cadastral_number: str
    floor_type: str
    load_bearing_wall_material: str


class Parser:
    federal_cities = ['Москва', 'Санкт-Петербург', 'Севастополь']
    __advanced_search_url = 'https://www.reformagkh.ru/search/houses-advanced'
    __regular_search_url = 'https://www.reformagkh.ru/'

    def __init__(self):
        option = webdriver.FirefoxOptions()
        option.set_preference('dom.webdriver.enabled', False)
        option.set_preference('dom.webnotifications.enabled', False)
        option.headless = True
        self.browser = webdriver.Firefox(options=option)

    def get_house(self, region: str, street: str, number: str, city: str = None) -> House:
        """
        The public method determines whether a city is federal. Calls the appropriate method.
        :param region:
        :param street:
        :param number:
        :param city:
        :return:
        """
        if region.capitalize() in self.federal_cities:
            return self._get_house_from_regular_search(region, street, number)
        return self._get_house_from_advanced_search(region, city, street, number)

    def _get_house_from_advanced_search(self, region, city, street, number) -> House or int:
        """
        Entering data in advanced search
        :param region:
        :param city:
        :param street:
        :param number:
        :return:
        """
        browser = self.browser
        browser.get(self.__advanced_search_url)
        # input region
        region_input = browser.find_element(by=By.XPATH,
                                            value='/html/body/section[2]/div/div/div/form/div/div[1]/input[1]')
        self.__input_text(region_input, region)
        # input city
        city_input = browser.find_element(by=By.XPATH, value='//*[@id="edit-settlement"]')
        self.__input_text(city_input, city)
        # input street
        street_input = browser.find_element(by=By.XPATH, value='//*[@id="edit-street"]')
        self.__input_text(street_input, street)
        # input house
        house_input = browser.find_element(by=By.XPATH, value='//*[@id="edit-house"]')
        self.__input_text(house_input, number)
        # click button
        browser.find_element(by=By.XPATH, value='/html/body/section[2]/div/div/div/form/div/button').click()
        # get house information
        house = self.__get_house_information()
        return house

    def _get_house_from_regular_search(self, region, street, number) -> House:
        """
        Entering data in regular search
        :param region:
        :param street:
        :param number:
        :return:
        """
        browser = self.browser
        browser.get(self.__regular_search_url)
        # input full string
        _input = browser.find_element(by=By.XPATH,
                                      value='/html/body/section[1]/div/div[3]/form/div[1]/input')
        self.__input_text(_input, f'{region}, {street}, {number}')
        house = self.__get_house_information()
        return house

    @staticmethod
    def __input_text(elem: webdriver, text: str):
        """
        Static method for entering text and selecting the first item from the drop-down list
        :param elem:
        :param text:
        :return:
        """
        elem.send_keys(text.capitalize())
        time.sleep(1)
        elem.send_keys(Keys.ARROW_DOWN)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)

    def __get_house_information(self) -> House:
        """
        The method gets a dictionary containing all the information about the house. Gathers an dataclass
        object House from it.
        :return:
        """
        self.__site_section_selection()
        house = self.__get_house_dict()
        return House(
            commissioning_year=int(house.get('Год ввода дома в эксплуатацию:')),
            number_of_floors=int(house.get('Количество этажей, ед:')),
            last_modification_of_the_profile=datetime.datetime.strptime(
                house.get('По данным Фонда ЖКХ информация последний раз актуализировалась:'), "%d.%m.%Y"),
            series_type_of_building_construction=house.get('Серия, тип постройки здания:'),
            house_type=house.get('Тип дома:'),
            house_is_emergency=house.get('Факт признания дома аварийным:', False),
            cadastral_number=house.get('кадастровый номер земельного участка'),
            floor_type=house.get('Тип перекрытий'),
            load_bearing_wall_material=house.get('Материал несущих стен'))

    def __site_section_selection(self):
        """
        Selecting the desired section of the site.
        :return:
        """
        self.browser.find_element(by=By.XPATH, value='/html/body/section[2]/div/table/tbody/tr/td[1]/a').click()

    def __get_house_dict(self) -> typing.Dict:
        """
        Collects all information from the home page.
        :return:
        """
        house_information = dict()
        # general information
        self.browser.find_element(by=By.XPATH, value='/html/body/section[4]/div/a[1]/span').click()
        general_information_block = self.browser.find_element(by=By.XPATH,
                                                              value='/html/body/section[5]/div[2]/div/div[2]/div['
                                                                    '1]/table/tbody '
                                                              ).find_elements(by=By.TAG_NAME, value='tr')
        general_inf = self.__parse_information_block(general_information_block)
        # structural elements of the house
        self.browser.find_element(by=By.XPATH, value='//*[@id="constructive-tab"]').click()
        structural_elements_block = self.browser.find_element(by=By.XPATH,
                                                              value='/html/body/section[5]/div[2]/div/div[2]/div['
                                                                    '2]/table/tbody '
                                                              ).find_elements(by=By.TAG_NAME, value='tr')
        structural_elements_inf = self.__parse_information_block(structural_elements_block)
        house_information.update(general_inf)
        house_information.update(structural_elements_inf)
        return house_information

    @staticmethod
    def __parse_information_block(block: webdriver) -> typing.Dict:
        """
        Gets a block with information about the house. Separates it for each item.
        :param block:
        :return:
        """
        inf_dict = dict()
        for _string in block:
            elem = _string.find_elements(by=By.TAG_NAME, value='td')
            information_strings = []
            for _ in elem:
                if len(_.text) != 0:
                    information_strings.append(_.text)
            try:
                inf_dict[information_strings[0]] = information_strings[1]
            except IndexError:
                pass
        return inf_dict
