from celery import shared_task
from house.models import House, LoadBearingWallMaterial
from house.services.parser import Parser
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException


@shared_task
def find_house(pk: int, region: str, street: str, number: str, city: str = None):
    """
    task for celery
    :param pk:
    :param region:
    :param street:
    :param number:
    :param city:
    :return:
    """
    for i in range(3):
        try:
            house_inf = Parser().get_house(region=region, city=city, street=street, number=number)
            house = House.objects.get(pk=pk)
            house.is_find = True
            house.commissioning_year = house_inf.commissioning_year
            house.number_of_floors = house_inf.number_of_floors
            house.last_modification_of_the_profile = house_inf.last_modification_of_the_profile
            house.series_type_of_building_construction = house_inf.series_type_of_building_construction
            house.house_type = house_inf.house_type
            house.house_is_emergency = house_inf.house_is_emergency
            house.cadastral_number = house_inf.cadastral_number
            house.floor_type = house_inf.floor_type
            material = LoadBearingWallMaterial.objects.get_or_create(material_type=house_inf.load_bearing_wall_material)
            house.load_bearing_wall_material = material
            house.save()
            break
        except (ElementNotInteractableException, NoSuchElementException):
            if i == 2:
                house = House.objects.get(pk=pk)
                house.is_find = False
                house.save()
