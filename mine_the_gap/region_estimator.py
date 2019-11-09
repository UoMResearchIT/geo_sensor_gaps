from .models import Actual_data, Region, Sensor
from abc import ABCMeta, abstractmethod


class Region_estimator(object):

    @abstractmethod
    def get_all_region_estimations(self, timestamp):
        pass


    def get_adjacent_regions(self, regions, ignore_regions):
        # Create an empty queryset for adjacent regions
        adjacent_regions = Region.objects.none()

        # Get all adjacent regions for each region
        for region in regions.iterator():
            adjacent_regions |= region.adjacent_regions

        # Return all adjacent regions as a querySet and remove any that are in the completed/ignore list.
        return Region.objects.filter(region_id__in= adjacent_regions).exclude(region_id__in=ignore_regions)