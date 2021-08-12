from backend_api.models.species import (
    InvasiveSpecies,
    InvasiveSpeciesSchema,
    SpeciesObservedWaterbody,
    SpeciesObservedWaterbodySchema,
    SpeciesObservedGeoJsonSchema
)
from backend_api.models.waterbody import WaterBodyGeoJson, WaterBodyGeoJsonSchema
from colour import Color as c
from backend_api import db

def get_invasive_species():
    invasive = InvasiveSpecies()
    invasive_schema = InvasiveSpeciesSchema()
    all_invasive = invasive.get_all()
    all_invasive = invasive_schema.dump(species, many=True)
    return all_invasive

def get_color_scale(max_):
    red = c("red")
    yellow = c("yellow")
    colors = red.range_to(yellow, max_)
    return {i+1:c for i,c in enumerate(colors)}


def get_species_observations_geojsons(id):
    #create db session (a bit different from what we normally do)
    session = db.session

    data = session.query(SpeciesObservedWaterbody).filter_by(species_id=id).join(WaterBodyGeoJson).all()
    data = [{'species_observed': x[0], 'waterbody_geojsons': x[1]} for x in data]
    schema = SpeciesObservedGeoJsonSchema()
    return schema.dump(data, many=True)
    # # get all observatsions of the species from database
    # sow = SpeciesObservedWaterbody()
    # species_obs = sow.find_invasive_waterways_by_species_id(id)
    #
    # # get their waterbody ids
    # waterbody_ids = [i.waterbody_id for i in species_obs]
    # wbgeojson = WaterBodyGeoJson()
    # geojsontest = wbgeojson.find_by_ids(waterbody_ids)
    # geojsonschema = WaterBodyGeoJsonSchema()
    # all_geojsons = [geojsonschema.dump(i) for i in geojsontest]
    # return all_geojsons