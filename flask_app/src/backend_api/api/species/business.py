import operator

from backend_api.models.species import (
    InvasiveSpecies,
    InvasiveSpeciesSchema,
    SpeciesObservedWaterbody,
    SpeciesObservedWaterbodySchema,
    SpeciesObservedGeoJsonSchema,
    SpeciesObservedWaterBodyNested,
    ImpactRelationship,
    Species
)
from backend_api.models.waterbody import WaterBodyGeoJson, WaterBodyGeoJsonSchema, Waterbody
from colour import Color as c
from backend_api import db
from sqlalchemy import asc, text
from backend_api.util.result import Result
import json
from flask import jsonify

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
        return []

table_species = Species()
class Node:
    def __init__(self, id):
        self.name = table_species.get_name_by_species_id(id).name
        self.id = str(id)
        self.img_url = None

class Link:
    source = None
    target = None

class graphDataStore:
    nodes = []
    links = []
    seen_nodes = set()

    def add_nodes(self, node):
        self.seen_nodes.add(node)
        n = Node(node)
        self.nodes.append(n.__dict__)

    def add_links(self, source, target):
        l = Link()
        l.source = str(source)
        l.target = str(target)
        self.links.append(l.__dict__)

class graphData:
    nodes = []
    links = []

def get_impact_network(id):
    table = ImpactRelationship()
    gd = graphDataStore()
    gd.add_nodes(id)

    def lookup_impacted_recurse(id_):
        impacted = table.find_species_impact_by_id(id_)
        for impact in impacted:
            if impact:
                impacted_id = impact.impacted_id
                if impacted_id not in gd.seen_nodes:
                    gd.add_nodes(impacted_id)
                    gd.add_links(id_, impacted_id)
                    lookup_impacted_recurse(impacted_id)
                else:
                    gd.add_links(id_, impacted_id)
                    continue
            else:
                break
    lookup_impacted_recurse(id)
    payload = graphData()
    payload.nodes = gd.nodes
    payload.links = gd.links
    return jsonify(payload.__dict__)






