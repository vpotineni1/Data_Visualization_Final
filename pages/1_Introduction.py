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

st.write("Before examining whether the recovery was uneven across neighborhoods, it is important to establish what the NYC rental market looked like" \
" before the pandemic and how severe the initial shock was. This section examines borough-level trends in rental prices and inventory between 2019 and 2022," \
" which provides the foundation for the community-district level analysis that will follow.")

st.write("Throughout this section, two normalized metrics are used to track rental market conditions across boroughs. The price index measures each borough's " \
" monthly median rent relative to its median rent in 2019. A value of 1.0 means rents are at the 2019 baseline, values above 1.0 indicate rents are higher than baseline" \
" , and values below 1.0 indicate rents have fallen below it. The inventory index uses the same logic but measures the number of available rental listings rather" \
" than price. Together, these metrics allow for a direct comparison of both cost and supply conditions before and after the pandemic. ")

st.header("Figure 1: Pre-Covid Market Conditions")

st.write(" Figure 1 shows rental price trends and inventory trends across the city's boroughs during the period immediately before the pandemic.")

st.altair_chart(pre_covid_trends_chart(rental_data), use_container_width=True)

st.caption("Figure 1 displays borough-level rental market conditions in New York City from January 2019 to February 2020, which is right before the " \
" pandemic. Rental prices in Manhattan, Brooklyn, and Queens showed a gradual upward trend over this period, while inventory levels slowly declined, indicating" \
" a strong tightening market driven by strong demand heading into the early stages of 2020. The metric toggle below the chart allows you to switch between" \
" the Price and Inventory Index.")

st.write("These trends suggest that the New York City housing market was relatively strong prior to COVID-19. It was characterized by rising rental prices, " \
" and tightening housing supply, which was driven by strong demand. ")

st.write("However, this all changed once the COVID-19 pandemic had hit. The pandemic quickly disrupted these trends. As lockdowns began, people left the city, which led " \
" to housing demand declining sharply. The next chart illustrates how these changes affected rental prices and housing supply across New York City")


st.header("Figure 2: Post-Covid Baseline Trends")

st.altair_chart(post_covid_trends_chart(rental_data), use_container_width=True)

st.caption("Figure 2 utilizes the same 2019 baseline to allow for a direct comparison with the pre-pandemic chart. In this chart, March 2020 is considered the start date of the pandemic in the United States as this was when a national" \
" emergency was declared. Rental prices declined rapidly across all four boroughs, and at the same time, inventory levels greatly increased, which means that a greater supply of apartments became available. These trends are consistent " \
"with the sudden drop in housing demand during the early stages of the pandemic. " )

st.write("Taken together, these charts illustrate a clear picture of the pandemic. Specifically, New York City had a relatively stable housing market before the pandemic, followed by a sharp " \
" demand shock in 2020 and a gradual recovery in the years that followed. ")

st.write("While these borough-level trends clearly show the overall impact of the pandemic on the rental market, they may hide important differences across neighborhoods. Did all" \
" areas of New York City experience the same recovery in rental prices and inventory, or did some districts rebound faster or in a larger magnitude than others? The next section " \
" examines these patterns at the community district level." )