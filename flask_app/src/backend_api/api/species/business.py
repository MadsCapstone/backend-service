import operator

from backend_api.models.species import (
    InvasiveSpecies,
    InvasiveSpeciesSchema,
    SpeciesObservedWaterbody,
    SpeciesObservedWaterbodySchema,
    SpeciesObservedGeoJsonSchema,
    SpeciesObservedWaterBodyNested,
    ImpactRelationship,
    Species,
    ImpacterRelationshipTarget,
    ImpacterDropdown,
    ImpactedDropdown,
    ImpacterDropdownSchema,
    ImpactedDropdownSchema
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
    print(payload)
    if payload:
        return payload
    else:
        return []

""" Defines the code for business logic of building Network Invasives"""
table_species = Species()
table_impact_rel = ImpactRelationship()
class Node:
    def __init__(self, id):
        self.name = table_species.get_name_by_species_id(id).name
        self.id = str(id)
        self.img_url = None
        self.neighbors = []
        self.links = []
        self.impacted = [{'impacted': i.impacted_id, 'impacter': i.impacter_id} for i in table_impact_rel.find_species_impact_by_id(self.id)]
        self.__update_child_nodes()
        self.__update_child_links()

    def __update_child_nodes(self):
        for impact in self.impacted:
            self.neighbors.append(impact['impacted'])

    def __update_child_links(self):
        for impact in self.impacted:
            l = Link()
            l.source = impact['impacter']
            l.target = impact['impacted']
            self.links.append(l.__dict__)

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


def get_target_invasive_dropdown():
    invasive_table = ImpacterDropdown()
    invasive_schema = ImpacterDropdownSchema()
    data = invasive_table.get_all_impacters()
    schema = {
        'uid':[],
        'impacter':[]
    }
    for entry in data:
        schema['uid'].append(entry.uid)
        schema['impacter'].append(entry.impacter)
    return jsonify(schema)


def get_target_impacted_dropdown():
    impacted_table = ImpactedDropdown()
    impacted_schema = ImpactedDropdownSchema()
    data = impacted_table.get_all_impacted()
    schema = {
        'uid':[],
        'impacted':[]
    }
    for entry in data:
        schema['uid'].append(entry.uid)
        schema['impacted'].append(entry.impacted)

    return jsonify(schema)


class ImpactRelDef:
    def __init__(self, data, query_type):
        self.schema = {
            'r': [],
            'theta': [],
            'mode': "text",
            'text': [],
            'text_font':{
                'color':[],
                'size':[]
            }
        }

        for entry in data:
            self.schema['r'].append(entry.radius)
            if query_type == "impacter":
                self.schema['theta'].append(entry.theta)
                self.schema['text'].append(entry.impacted)
                self.schema['text_font']['color'].append('black')
                self.schema['text_font']['size'].append(8)
            if query_type == "impacted":
                self.schema['theta'].append(entry.theta_two)
                self.schema['text'].append(entry.impacter)
                self.schema['text_font']['color'].append('black')
                self.schema['text_font']['size'].append(8)
        self.schema['r'].extend([0.5, 1.5, 2.5])
        self.schema['theta'].extend([90,90,90])
        self.schema['text'].extend(['first','second','third'])
        self.schema['text_font']['color'].extend(['lightgray','lightgray','lightgray'])
        self.schema['text_font']['size'].extend([12,12,12])

    def get_schema(self):
        return self.schema


def get_target_relationship_data(name, query_type):
    target_data_rel = ImpacterRelationshipTarget()
    if query_type=="impacter":
        data = target_data_rel.find_relationship_by_impacter_name(name)
    if query_type=="impacted":
        data = target_data_rel.find_relationship_by_impacted_name(name)
    ird = ImpactRelDef(data, query_type)
    payload = ird.get_schema()
    payload = jsonify(payload)
    return payload


def get_impact_network_full():
    pass


