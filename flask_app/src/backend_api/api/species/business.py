import operator

from backend_api.models.species import (
    InvasiveSpecies,
    InvasiveSpeciesSchema,
    SpeciesObservedWaterbody,
    SpeciesObservedWaterbodySchema,
    SpeciesObservedGeoJsonSchema,
    SpeciesObservedWaterBodyNested
)
from backend_api.models.waterbody import WaterBodyGeoJson, WaterBodyGeoJsonSchema, Waterbody
from colour import Color as c
from backend_api import db
from sqlalchemy import asc, text
from backend_api.util.result import Result

def get_invasive_species():
    invasive = InvasiveSpecies()
    invasive_schema = InvasiveSpeciesSchema()
    all_invasive = invasive.get_all()
    all_invasive = invasive_schema.dump(all_invasive, many=True)
    return all_invasive

def get_color_scale(data):
    if len(data) == 0:
        return False
    else:
        red = c("red")
        yellow = c("yellow")
        max_ = []
        for i in data:
            max_.append(i['distance'])
        if len(max_)>0:
            colors = red.range_to(yellow, max(max_)+1)
            colors = {i: c.hex for i, c in enumerate(colors)}
            new_data = []
            for i in data:
                color = colors[i['distance']]
                i['color'] = color
                new_data.append(i)
            return new_data
        else:
            return False


def get_species_observations(id):
    table = SpeciesObservedWaterbody()
    data = table.find_invasive_waterways_by_species_id(id)
    schema = SpeciesObservedWaterbodySchema()
    payload = schema.dump(data, many=True)
    payload = get_color_scale(payload)
    if payload:
        return payload
    else:
        return {}

