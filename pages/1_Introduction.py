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


st.title("Introduction")
st.header("NEED TO FILL OUT")
st.markdown("Start off talking about the NYC housing market, the motivation, the dataset, and the central question/theme of analysis")


st.header("Figure 1: Pre-Covid Baseline Trends")

st.write("Before diving into the analysis, it is important to analyze the NYC housing market before the pandemic in order to demonstrate its stability ")

st.altair_chart(pre_covid_trends_chart(rental_data), use_container_width=True)


st.caption("Figure 1 displays two metrics including price index and inventory index. The baseline for the price index is the median rent price for the year 2019 for each of the boroughs, and the baseline for inventory index is the average volume of rentals available in 2019 for"
" each of the boroughs. The price index is calculated by taking the median rent price for that month/the median rent price in the year 2019, while the inventory index is calculated by taking the inventory for that month/the average inventory in 2019. This means that if the value is above 1"
" price or inventory had increased compared to 2019 or if the value is below 1, price or inventory had decreased. With the price index, we see that the Queens, Brooklyn, and Manhattan seem to have increasing price indexes right before COVID, which means median rent prices had been increasing." \
" On the other hand, the rent price seemed to be in line with the baseline rent price in the Bronx as the price index is consistently around 1. " \
" The inventory index captures the number of available rental listings relative to the 2019 baseline. In early 2019, inventory levels across boroughs generally remain close to or slightly above their baseline levels. " \
" However, inventory begins to gradually decline throughout the year across most boroughs, particularly in Brooklyn and the Bronx. By late 2019 and early 2020, inventory levels fall noticeably below their baseline levels, " \
" indicating that the number of available rental units on the market was decreasing slowly before the onset of COVID-19." )

st.write("With the above chart, there are three main takeaways. First, the New York City housing market seems to have been doing well as prices were slowly increasing in most of the boroughs. Second, inventory levels had been slowly decreasing, which is consistent with high demand from" \
" consumers. Lastly,this chart shows that pre-COVID, the New York City housing market had been stable and growing economically. Thus, it seemed like an ideal market. However, this all changed once the COVID-19 pandemic had hit. ")


st.header("Figure 2: Post-Covid Baseline Trends")

st.write("As demonstrated above, before the COVID Pandemic, the New York City housing market served as a stable and growing market with price levels slowly increasing and inventory levels slowly decreasing. In March of 2020, the COVID Pandemic had officially been declared in the United States" \
" which proved to serve as economic shock to the New York City housing market.")


st.altair_chart(post_covid_trends_chart(rental_data), use_container_width=True)

st.caption("In Figure 2, the baseline is still 2019, to allow for an apples to apples comparison with the last chart. In this chart, March 2020 is considered the start date of the pandemic in the United States," \
" and the shock effects on the NYC housing market is very easily seen. With price index, in all four boroughs, the rent prices start to decrease rapidly, and it is not until over a year later, that they start to rapidly recover. " \
" Further, when looking at inventory levels, they greatly increased, which means that a greater supply of apartments became available . " )


st.write("COVID-19 had proved to be an economic shock to the New York City housing market. It had caused rent price levels to decrease, while increasing supply of rent properties. With that being said, " \
" it would be interesting to delve deeper into this shock. While these charts display the overall effect of the pandemic, it would be interesting to understand the effects of the COVID-19 pandemic on the housing market" \
" at the community district level. ")
