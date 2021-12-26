import typing
from house.models import House, Region, City, LoadBearingWallMaterial


def house_analysis():
    """
    The function collects the results of executing analysis functions.
    :return:
    """
    count = _count_of_found()
    count_bricks = _count_of_objects_for_brick()
    max_numbers = _max_number_of_floors()
    return count, count_bricks, max_numbers


def _count_of_found() -> dict:
    """
    The function determines the number of all objects, found and not found.
    :return:
    """
    all_houses = House.objects.all()
    count_all_houses = all_houses.count()
    count_find = all_houses.filter(is_find=True).count()
    count_not_find = count_all_houses - count_find
    return {'all': count_all_houses, 'find': count_find, 'not_find': count_not_find}


def _count_of_objects_for_brick() -> typing.List[dict]:
    """
    The function determines the number of objects with brick bearing wall material for each region.
    :return:
    """
    count_for_regions = list()
    all_regions = Region.objects.all()
    all_houses = House.objects.all()
    brick = LoadBearingWallMaterial.objects.all().filter(material_type='Кирпичный').first()
    for region in all_regions:
        try:
            count = all_houses.filter(region=region.pk, load_bearing_wall_material=brick.pk).count()
            count_for_regions.append({region.region_name: count})
        except:
            count_for_regions.append({region.region_name: 0})
    return count_for_regions


def _max_number_of_floors() -> typing.List[dict[dict]]:
    """
    Determines the maximum number of floors for each structural wall material in each city.
    :return:
    """
    all_houses = House.objects.all().select_related('load_bearing_wall_material').filter(is_find=True)
    all_cities = City.objects.all()
    all_materials = LoadBearingWallMaterial.objects.all()
    result = list()
    for city in all_cities:
        cities_dict = dict()
        materials_dict = dict()
        for material in all_materials:
            houses = all_houses.filter(city=city.pk, load_bearing_wall_material=material.pk)
            max_floors = max([house.number_of_floors for house in houses])
            materials_dict[material] = max_floors
        cities_dict[city.city_name] = materials_dict
        result.append(cities_dict)
    return result
