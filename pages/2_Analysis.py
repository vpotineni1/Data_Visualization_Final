import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import altair as alt
from utils.data_loader import rental_data, mapping_data, housing_data, poverty_data, income_data, streeteasy_data

from charts.charts import (
    base_theme,
    pre_covid_trends_chart,
    post_covid_trends_chart,
    choropleth,
    scatter_poverty,
)

st.set_page_config(page_title="Story", layout="wide")
alt.themes.register("project", base_theme)
alt.themes.enable("project")

rental_data = rental_data()
housing_data = housing_data()
poverty_data = poverty_data()
income_data = income_data()
streeteasy_data = streeteasy_data()

#mapping_data = mapping_data() #Figure out why this is not working


st.header("NEED TO DO: Figure 3: CHOROPLETH GOES HERE")

st.write("Figure 1 and 2 in the introduction displayed overall impacts by borough. However, we know that COVID did not affect everyone proportionately. Did COVID-19 impact some districts more than others? Specifically, considering we are looking at the before" \
" and after of the pandemic, did some districts experience a greater rent decline or rent recovery?")


st.caption(" NEED TO DO: THIS CAPTION WILL BE A SHORT DESCRIPTION OF THE GRAPH, AND HOW TO INTERPRET THE VARIABLES ")


st.header("Figure 4: NEED TO INSERT A RANKED BAR CHART THAT DISPLAYS WHICH DISTRICTS TOOK THE LONGEST AND SHORTEST TO RECOVER")

st.write("The previous figures show that the effects of COVID-19 on New York City's rental market were far from uniform. Some community districts experienced sharp" \
" rent declines followed by strong recoveries, while others saw weaker rebounds. This raises an important question: what explains these differences across neighborhoods? One possible" \
" explanation lies in the socioeconomic characteristics of each district. In particular, poverty levels may influence how quickly and the magnitude to which housing markets recover" \
" from economic shocks.")



st.write(" To explore this relationship, the next visualization compares each district's poverty rate with the strength of its rental recovery between 2020 and 2022. By comparing these two variables, we can examine" \
" whether poorer neighborhoods experienced weaker rent recoveries.")

st.header("Figure 5: Rent Recovery vs. Poverty Rate")

st.altair_chart(scatter_poverty(rental_data, streeteasy_data, housing_data, poverty_data), use_container_width=True)

st.caption(" Note: Poverty rates were used as a proxy for socioeconomic vulnerability.")

st.caption(" From Figure 5, there is a clear inverse relationship between recovery in rent price from 2020-2022 with poverty rate. Specifically, as poverty rate increases, it seems as if the rent price recovery in those districts had been much smaller.   ")

st.write(" This pattern indicates that the housing market recovery was not only geographically uneven, but also closely tied to underlying socioeconomic" \
" inequalities across neighborhoods.")

st.write(" While the last figure focused on the demand-side explanation (income differences), we move onto development patterns as another possible explanation. Specifically, " \
" real estate development also differs across community districts, with some districts receiving far more investment and new housing construction than others during the recovery" \
" period.")

st.write(" The map below shows the housing completion rate between 2020 and 2022 across New York City community districts. By measuring new housing" \
" completions relative to the existing housing stock, this metric captures where real estate development was concentrated during the post-COVID period.")

st.header("NEED TO INSERT FIGURE 6: HOUSING DEVELOPMENT, THIS WILL BE A CHOROPELTH WITH AN INTERACTIVE SCATTERPLOT")

st.caption(" Housing Construction during the COVID period varied widely across NYC community districts. Some districts added relatively new housing units, relative " \
" to their existing housing stock.  ")

st.write("Some districts with weaker rental recovery also saw relatively little new housing development during the pandemic, which might suggest" \
" that limited housing supply stunted growth and may have slowed recovery. ")

st.write(" While housing supply may have played a role in shaping recovery patterns, these differences ultimately raise a broader question: how affordable" \
" was rent for residents in different community distrcits? ")
