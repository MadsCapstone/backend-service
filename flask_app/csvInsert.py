from backend_api import create_app, db
from sqlalchemy import create_engine
import pandas as pd
import os

# engine = create_engine('sqlite:///backend_api_dev.db')
engine = create_engine(f"postgresql://flask-app:capstone-db-user-!@localhost:5432/core-db")

waterbody_geojson_df = pd.read_csv('../csv-data/waterbody_geojsonsv2.csv')
waterbody_geojson_df.to_sql(
    'waterbody_geojson',
    con=engine,
    index=False,
    if_exists='replace'
)


waterbodies_df = pd.read_csv('../csv-data/waterbodies.csv')
waterbodies_df.to_sql(
    'waterbody',
    con=engine,
    index=False,
    # if_exists='replace'
)

species_df = pd.read_csv('../csv-data/key_to_species.csv')
species_df.to_sql(
    'species',
    con=engine,
    index=False,
    if_exists='replace'
)

invaders_df = pd.read_csv('../csv-data/species_invaders.csv')
invaders_df.to_sql(
    'invasive_species',
    con=engine,
    index=False,
    if_exists='replace'
)

species_observed_df = pd.read_csv('../csv-data/observed_species_with_name.csv')
species_observed_df.to_sql(
    'species_observed',
    con=engine,
    index=False,
    if_exists='replace'
)

impact_rel_df = pd.read_csv('../csv-data/impacter_impacted_relationship.csv')
impact_rel_df.to_sql(
    'impact_rel',
    con=engine,
    index=False,
    if_exists='replace'
)


