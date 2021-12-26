from django.db import models


class House(models.Model):
    region = models.ForeignKey(to='Region', on_delete=models.DO_NOTHING)
    city = models.ForeignKey(to='City', on_delete=models.DO_NOTHING)
    street = models.CharField(max_length=255, null=False, blank=False)
    number = models.CharField(max_length=255, null=False, blank=False)
    is_find = models.BooleanField(null=True)
    commissioning_year = models.IntegerField(null=True)
    number_of_floors = models.IntegerField(null=True)
    last_modification_of_the_profile = models.DateTimeField(null=True)
    series_type_of_building_construction = models.CharField(max_length=255, null=True)
    house_type = models.CharField(max_length=255, null=True)
    house_is_emergency = models.BooleanField(null=True)
    cadastral_number = models.CharField(max_length=255, null=True)
    floor_type = models.CharField(max_length=255, null=True)
    load_bearing_wall_material = models.ForeignKey(to='LoadBearingWallMaterial', on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'houses'
        unique_together = ['region', 'city', 'street', 'number']


class Region(models.Model):
    region_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'regions'


class City(models.Model):
    city_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'cities'


class LoadBearingWallMaterial(models.Model):
    material_type = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'materials'
