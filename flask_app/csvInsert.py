from backend_api import create_app, db
from sqlalchemy import create_engine
import pandas as pd
import os

# engine = create_engine('sqlite:///backend_api_dev.db')
engine = create_engine(f"postgresql://flask-app:capstone-db-user-!@localhost:5432/core-db")

# waterbody_geojson_df = pd.read_csv('../csv-data/waterbody_geojsonsv2.csv')
# waterbody_geojson_df.to_sql(
#     'waterbody_geojson',
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
#
# waterbodies_df = pd.read_csv('../csv-data/waterbodies.csv')
# waterbodies_df.to_sql(
#     'waterbody',
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
# species_df = pd.read_csv('../csv-data/prod_data/species.csv')
# species_df.to_sql(
#     'species',
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
# invaders_df = pd.read_csv('../csv-data/prod_data/invasive_species.csv')
# invaders_df.to_sql(
#     'invasive_species',
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
# species_observed_df = pd.read_csv('../csv-data/prod_data/species_observed.csv')
# species_observed_df.to_sql(
#     'species_observed',
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
# impact_rel_df = pd.read_csv('../csv-data/prod_data/impact_rel.csv')
# impact_rel_df.to_sql(
#     'impact_rel',
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
# target_invasive_dropdown_df = pd.read_csv('../csv-data/prod_data/target_dropdown_impacter.csv')
# target_invasive_dropdown_df.to_sql(
#     "target_dropdown_impacter",
#     con=engine,
#     index=False,
#     if_exists='replace'
# )
#
# target_impacted_dropdown_df = pd.read_csv('../csv-data/prod_data/target_dropdown_impacted.csv')
# target_impacted_dropdown_df.to_sql(
#     "target_dropdown_impacted",
#     con=engine,
#     index=False,
#     if_exists='replace'
# )

target_data_rel_df = pd.read_csv('../csv-data/prod_data/target_data_rel.csv')
target_data_rel_df.to_sql(
    "target_data_rel",
    con=engine,
    index=False,
    if_exists='replace'
)
