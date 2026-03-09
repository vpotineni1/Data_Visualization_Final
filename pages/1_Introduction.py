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
)

st.set_page_config(page_title="Story", layout="wide")
alt.themes.register("project", base_theme)
alt.themes.enable("project")

rental_data = rental_data()
housing_data = housing_data()
poverty_data = poverty_data()
income_data = income_data()
streeteasy_data = streeteasy_data()


st.title("The COVID-19 Shock to New York City's Rental Market")

st.write("To understand how the COVID-19 pandemic affected New York City's rental market, we first examine overall rental market trends before and after the start of " \
" the pandemic. Looking at borough-level data helps establish the broader market conditions that existed prior to COVID-19 and illustrates the magnitude of the shock" \
" that followed.")

st.header("Figure 1: Pre-Covid Market Conditions")

st.write(" Figure 1 shows rental price trends and inventory trends across the city's boroughs during the period immediately before the pandemic.")

st.altair_chart(pre_covid_trends_chart(rental_data), use_container_width=True)


st.caption("Figure 1 displays two normalized metrics including the price index and inventory index. The price index measures monthly median rent relative to each borough's average rent " \
" in 2019. The inventory index measures the number of rental listings relative to the average number of listings in 2019. An index value of 1 represents the 2019 baseline, values above 1" \
" indicate higher level than the baseline, and values below 1 indicate lower levels. " )

st.write("Several patterns emerge from the figure. Rental prices in Manhattan, Brooklyn, and Queens were gradually increasing before the pandemic, while prices in the Bronx " \
" remained relatively stable around the baseline level. At the same time, the number of available rental listings was slowly declining across most boroughs. ")

st.write("Taking these insights together, these trends suggest that the New York City housing market was relatively strong prior to COVID-19. It was characterized by rising rental prices, " \
" and tightening housing supply, which was driven by strong demand. ")

st.write(" However, this all changed once the COVID-19 pandemic had hit. The pandemic quickly disrupted these trends. As lockdowns began, people left the city, which led " \
" to housing demand declining sharply. The next chart illustrates how these changes affected rental prices and housing supply across New York City")


st.header("Figure 2: Post-Covid Baseline Trends")

st.altair_chart(post_covid_trends_chart(rental_data), use_container_width=True)

st.caption("Figure 2 utilizes the same 2019 baseline to allow for a direct comparison with the pre-pandemic chart. In this chart, March 2020 is considered the start date of the pandemic in the United States as this was when a national" \
" emergency was declared. Rental prices declined rapidly across all four boroughs, and at the same time, inventory levels greatly increased, which means that a greater supply of apartments became available. These trends are consistent with the sudden drop in housing demand during the early stages " \
" of the pandemic. " )

st.write("Taken together, these charts illustrate a clear picture of the pandemic. Specifically, New York City had a relatively stable housing market before the pandemic, followed by a sharp " \
" demand shock in 2020 and a gradual recovery in the years that followed. ")

st.write("While these borough-level trends clearly show the overall impact of the pandemic on the rental market, they may hide important differences across neighborhoods. Did all" \
" areas of New York City experience the same recovery in rental prices and inventory, or did some districts rebound faster or in a larger magnitude than others? The next section " \
" examines these patterns at the community district level." )