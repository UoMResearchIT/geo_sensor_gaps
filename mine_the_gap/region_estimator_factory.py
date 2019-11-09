# Polymorphic factory methods.
from __future__ import generators
from mine_the_gap.diffusion_estimator import Diffusion_estimator
from mine_the_gap.distance_simple_estimator import Distance_simple_estimator


class Region_estimator_factory:
    factories = {}



    def add_factory(id, region_estimator_factory):
        Region_estimator_factory.factories.put[id] = region_estimator_factory
    add_factory = staticmethod(add_factory)

    # A Template Method:
    def create_region_estimator(method_name):
        class_name = get_classname(method_name)
        if class_name not in Region_estimator_factory.factories:
            Region_estimator_factory.factories[class_name] = eval(class_name + '.Factory()')
        return Region_estimator_factory.factories[class_name].create()

    create_region_estimator = staticmethod(create_region_estimator)



def get_classname(method_name):
    if method_name == 'diffusion':
        return 'Diffusion_estimator'
    elif method_name == 'distance-simple':
        return 'Distance_simple_estimator'


