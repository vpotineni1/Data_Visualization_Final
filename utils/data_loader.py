import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import altair as alt

@st.cache_data
def rental_data():
    rental_data = pd.read_csv("data/rentals.csv")
    rental_data['date'] = pd.to_datetime(rental_data['date'])
    return rental_data

@st.cache_data
def mapping_data():
    community_districts = gpd.read_file("data/nycd.shp")
    community_districts = community_districts.to_crs(epsg=4326)
    community_districts['BoroCD'] = community_districts['BoroCD'].astype(int)
    return community_districts


@st.cache_data
def housing_data():
    housing = pd.read_csv("data/Housing_Database_by_Community_District_20260222.csv")
    housing.rename(columns={'commntydst': 'communityDistrict'}, inplace=True)

    completion_columns = ["comp2020", "comp2021", "comp2022"]
    housing_new = housing[['communityDistrict', 'comp2020', 'comp2021', 'comp2022', 'cenunits20']]

    housing_new['comp2020'] = housing_new['comp2020'].str.replace(',', '')
    housing_new['comp2021'] = housing_new['comp2021'].str.replace(',', '')
    housing_new['comp2022'] = housing_new['comp2022'].str.replace(',', '')
    housing_new['cenunits20'] = housing_new['cenunits20'].str.replace(',', '')  

    housing_new['comp2020']= pd.to_numeric(housing_new['comp2020'], errors='coerce')
    housing_new['comp2021']= pd.to_numeric(housing_new['comp2021'], errors='coerce')
    housing_new['comp2022']= pd.to_numeric(housing_new['comp2022'], errors='coerce')
    housing_new['cenunits20']= pd.to_numeric(housing_new['cenunits20'], errors='coerce')


    housing_new["covid_completions"] = housing_new['comp2020'] + housing_new['comp2021'] + housing_new['comp2022']
    housing_new['completion_rate'] = housing_new["covid_completions"]  / housing_new['cenunits20']
    housing_new['communityDistrict'] = housing_new['communityDistrict'].astype(int)


    return housing_new

@st.cache_data
def poverty_data():
    poverty_rate = pd.read_csv("data/poverty_rate.csv")
    poverty_rate['poverty_rate'] = poverty_rate['poverty_rate'].str.replace('%', '')
    poverty_rate['poverty_rate'] = pd.to_numeric(poverty_rate['poverty_rate'], errors='coerce')
    poverty_rate['poverty_rate'] = poverty_rate['poverty_rate'] / 100
    return poverty_rate


@st.cache_data
def income_data():
    income_cd = pd.read_csv("data/income_CD.csv")
    income_cd = income_cd.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5' ], axis = 1)
    income_cd.rename(columns = {"communityDistrict\t" : 'communityDistrict'}, inplace = True)
    income_cd['Median_Household_Income'] = income_cd['Median_Household_Income'].astype(int)
    return income_cd


def streeteasy_data():
    streeteasy = pd.read_csv("data/streeteasy.csv")
    streeteasy['date'] = pd.to_datetime(streeteasy['date'])
    return streeteasy

