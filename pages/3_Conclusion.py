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
    rent_burden_visualization
)

st.set_page_config(page_title="Story", layout="wide")
alt.themes.register("project", base_theme)
alt.themes.enable("project")


rental_data = rental_data()
housing_data = housing_data()
poverty_data = poverty_data()
income_data = income_data()
streeteasy_data = streeteasy_data()


st.write("The previous chart highlights how uneven the housing recovery was across community districts. While " \
"some neighborhoods returned to pre-pandemic rent levels relatively quickly, others took signficantly longer to recover." \
"These differences in rent recovery also have important implications for housing affordability. The chart below" \
"examines how rent burdens have changed across distrcits by comparing rents relative to local incomes before and" \
"after the pandemic.")

st.header("Figure 7: Changes in Housing Affordability Varied Across Income Levels")

st.altair_chart(rent_burden_visualization(rental_data, streeteasy_data, housing_data,income_data), use_container_width=True)

st.caption("Note: Income from 2019 is used for both periods to isolate the effect of rent changes on housing affordability")

st.caption("DESCRIBE THE CHART")

st.write("PUT TAKEAWAY FROM IT HERE: This should essentially talk about the nuance of it, and how it is a double-edged sword. Essentially," \
" rent recovery was smaller in poorer neighborhoods, which is actually not necessarily a bad thing. This means the rent burden is smaller, " \
" however, it also means that economic development in that error stunted post-COVID, which is not necessarily the best for the long-term development" \
" of the area.")


st.write("WILL WRITE A PARAGRAPH OR TWO FOR THE CONCLUSION")

st.write("DESCRIBE THE LIMITATIONS OF THE ANALSYIS")