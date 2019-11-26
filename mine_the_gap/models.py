from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models as gismodels


class Filenames(models.Model):
    actual_data_filename = models.CharField(max_length=50, null=True)
    sensor_metadata_filename = models.CharField(max_length=50, null=True)
    estimated_data_filename = models.CharField(max_length=50, null=True)
    region_metadata_filename = models.CharField(max_length=50, null=True)



class Sensor(gismodels.Model):
    geom = gismodels.PointField(null=False)
    name = models.CharField(max_length=50, db_index=True, null=True)
    extra_data = JSONField(null=True)

    @property
    def popup_content(self):
        return {'sensor_id': self.id,
                'name': self.name,
                'extra_data': self.extra_data}




class Actual_data(gismodels.Model):
    timestamp = models.CharField(max_length=30, null=False)
    sensor = models.ForeignKey(Sensor, null=True, on_delete=models.CASCADE)

    @property
    def join_sensor(self):
        return {'timestamp': self.timestamp,
                'name': self.sensor.name,
                'sensor_id': self.sensor_id,
                'geom': self.sensor.geom.coords,
                'sensor_extra_data': self.sensor.extra_data}

    @property
    def join_sensor_lite(self):
        return {'timestamp': self.timestamp,
                'name': self.sensor.name,
                'sensor_id': self.sensor_id}


class Actual_value(gismodels.Model):
    actual_data = models.ForeignKey(Actual_data, null=True, on_delete=models.CASCADE)
    measurement_name = models.CharField(max_length=30, null=False, db_index=True)
    value = models.FloatField(null=True)

    @property
    def join_sensor(self):
        try:
            fvalue = float(self.value)
        except:
            fvalue = None
        result = self.actual_data.join_sensor
        result.update({'measurement_name': self.measurement_name,
                       'value': fvalue,
                       'actual_data_id': self.actual_data_id})
        return result

    @property
    def join_sensor_lite(self):
        try:
            fvalue = float(self.value)
        except:
            fvalue = None
        result = self.actual_data.join_sensor_lite
        result.update({'measurement_name': self.measurement_name,
                       'value': fvalue})
        return result




class Region(gismodels.Model):
    region_id = models.CharField(max_length=30, primary_key=True)
    geom = gismodels.MultiPolygonField(null=False)
    extra_data = JSONField(null=True)

    def __unicode__(self):
        return self.region_label

    @property
    def popup_content(self):
        return {'region_id': self.region_id, 'extra_data': self.extra_data}

    @property
    def adjacent_regions(self):
        return Region.objects.filter(geom__touches=self.geom)




class Estimated_data(gismodels.Model):
    timestamp = models.CharField(max_length=30, null=False)
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    @property
    def join_region(self):
        return {'timestamp': self.timestamp,
                'region_id': self.region_id,
                'geom': self.region.geom.coords,
                'region_extra_data': self.region.extra_data}

    @property
    def join_region_lite(self):
        return {'timestamp': self.timestamp,
                'region_id': self.region_id}


class Estimated_value(gismodels.Model):
    estimated_data = models.ForeignKey(Estimated_data, null=True, on_delete=models.CASCADE)
    measurement_name = models.CharField(max_length=30, null=False, db_index=True)
    value = models.FloatField(null=True)
    extra_data = JSONField(null=True)

    @property
    def join_region(self):
        try:
            fvalue = float(self.value)
        except:
            fvalue = None
        result = self.estimated_data.join_region
        result.update({'measurement_name': self.measurement_name,
                       'value': fvalue,
                       'estimated_data_id': self.estimated_data_id,
                       'extra_data': self.extra_data})
        return result

    @property
    def join_region_lite(self):
        try:
            fvalue = float(self.value)
        except:
            fvalue = None
        result = self.estimated_data.join_region_lite
        result.update({'measurement_name': self.measurement_name,
                       'value': fvalue})
        return result