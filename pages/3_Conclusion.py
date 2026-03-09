import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import altair as alt
from utils.data_loader import rental_data, mapping_data, housing_data, poverty_data, income_data, streeteasy_data

from charts.charts import (
    base_theme,
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
" some neighborhoods returned to pre-pandemic rent levels relatively quickly, others took signficantly longer to recover." \
" These differences in rent recovery also have important implications for housing affordability. The chart below" \
" examines how rent burdens have changed across districts by comparing rents relative to local incomes before and" \
" after the pandemic.")

st.header("Figure 7: Changes in Housing Affordability Varied Across Community Districts")

st.altair_chart(rent_burden_visualization(rental_data, income_data), use_container_width=True)

st.caption("Note: Income from 2019 is used for both periods to isolate the effect of rent changes on housing affordability")

st.caption("Figure 7 compares how housing affordability changed across community districts between 2019 and 2022. The scatterplot shows each" \
" district's median household income against the change in its rent to income ratio. The bar chart highlights the top ten districts wherer affordability" \
" worsened the most. Notably, the districts where affordability worsened the most such as 101 and 303 are also the same high-income, strong-recovery" \
" districts that was identified in figure 4. ")

st.write("Figure 7 reveals a very important and somewhat counterintuitive findings. The districts where housing affordabiltiy worsened the most such as 101 and 303" \
" are the same high-income and strong recovery districts that we identified earlier. Meanwhile, lower-income districts that saw weaker rent recoveries experienced" \
" smaller increases in rent burden on average. While this might seem like a positive outcome for poorer neighborhoods, it reflects a double-edged sword. Weaker rent recovery" \
" might be a sign of reduced investment, economic activity, and development. These neighborhoods might have avoided worsened affordability as their markets due to the lack of economic activity" \
" and development. ")


st.write("WILL WRITE A PARAGRAPH OR TWO FOR THE CONCLUSION")

st.write("DESCRIBE THE LIMITATIONS OF THE ANALSYIS")