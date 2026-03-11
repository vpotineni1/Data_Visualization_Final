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


st.write("The previous section established that the COVID-19 rental recovery was deeply uneven across New York City's" \
" community districts. Two potential reasons for this were poverty rates and housing development. This " \
" raises a more fundamental question of whether districts with weaker rent recovery actually benefit residents by keeping housing costs down?" \
" To isolate the direct effect of rent changes, we compare how rent burdens changed across districts between 2019 and 2022, holding" \
" household income constant at 2019 levels. If weaker recovery helped residents, we would expect those districts to show the " \
" smallest increases in rent burden or even potential improvements in affordability.")

st.header("Figure 7: Changes in Housing Affordability Varied Across Community Districts")

st.altair_chart(rent_burden_visualization(rental_data, streeteasy_data,income_data, housing_data), use_container_width=True)

st.caption("Note: Income from 2019 is used for both periods to isolate the effect of rent changes on housing affordability. ")

st.caption("Figure 7 compares rent recovery between 2020 and 2022 with the change in rent-to-income ratio between 2019 and 2022 for" \
" each community district. Blue points indicate strong recovery districts, red points indicate weak recovery districts, and gray points" \
" represent all other districts. The regression line shows a clear positive relationship as districts with stronger" \
" rent recovery also saw larger increases in rent burden. The bar chart identifies the ten districts where affordability worsened most," \
" all of which experienced above-average rent recovery.")

st.write("Figure 7 reveals a clear and positive relationship between rent recovery and rent burden increase, as the stronger a district's" \
" rent recovery, the larger the increase in its rent-to-income ratio. The ten districts where affordability worsened most all experienced" \
" above-average rent recovery. The two most extreme cases are districts 101 and 303. District 101 saw rent recovery of almost 90% " \
" and a rent burden increase of nearly 29%. District 303 followed with a rent burden increase of approximately 17 percentage points. Notably," \
" both of these districts were identified as strong recovery districts in Figure 4, confirming that the strongest rebounding neighborhoods " \
" also experienced worsening affordability. ")

st.write("In contrast, the weak recovery districts shown in red cluster near zero on both axes. Their rent recovery was very minimal and their rent burden" \
" change was also near zero. District 407, for example, had a rent recovery of roughly 5% and saw virtually no change in rent burden. " \
" On the surface this might appear to be a positive outcome for residents. However, this reflects stagnant market conditions rather than " \
" improved affordability. Rents in these districts remained depressed not because residents were protected, but because housing" \
" demand never fully returned following the pandemic shock.")

st.write("This reveals the double-edged nuance of New York City's uneven recovery. Weaker rent recovery did not mean better outcomes for residents. Rather, " \
" especially as discussed in Figures 4 and 5, it signaled depressed demand, limited investment, and stunted economic activity. Meanwhile," \
" stronger recovery came at a direct cost to residents in the form of higher rent burdens. The pandemic produced two distinct types of " \
" hardship across the city. The first is high-income districts that became significantly less affordable, while lower-income districts remained" \
" economically depressed. Both represent the main types of recovery that took place after the economic shock caused by the pandemic.")

st.markdown("---")
st.header("Conclusion")

st.write("The COVID-19 pandemic did not affect New York City's rental market uniformly. While all boroughs experienced a sharp demand shock in 2020, which was" \
" reflected by falling rents and rising inventory levels, the subsequent recovery was deeply uneven across community districts. Some neighborhoods, especially" \
" in Manhattan, rebounded strongly and surpassed their pre-pandemic rent levels in 2022. Others, especially those in the lower-income areas of the Bronx, remained" \
" well below their pre-pandemic baseline.")


st.write("When looking at the central question of this narrative, it is clear that the COVID-19 pandemic produced a deeply uneven housing recovery across" \
" New York City's community districts. Two factors help explain part of the variation in rent recovery. First, socioeconomic vulnerability (measured by" \
" poverty rates) was inversely associated with rent recovery. Second, housing development also played a role as districts with higher completion rates during" \
" the recovery period were also more likely to see stronger rent rebounds. ")


st.write("One of the most nuanced findings of this report, however, was the affordability analysis. A weaker rent recovery did not translate into better outcomes" \
" for residents in lower-income districts. While those neighborhoods avoided the largest increases in rent burden, this was not a sign of resilience. Rather, it" \
" reflected depressed housing demand, limited investment, and stunted economic activity. Meanwhile, districts that recovered strongly saw rent burdens" \
" rise sharply as rents outpaced incomes. The pandemic thus produced two outcomes. High-income districts became much less affordable, and lower-income districts" \
" remained economically depressed. Both of these outcomes represent the lack of equitable recovery. ")


st.markdown("Below are four limitations with regards to this analysis:")
st.markdown("1. This analysis was not meant to prove causality. While the relationships between the variables are easily seen in the charts," \
" this analysis was not meant to prove causality, and thus should not be taken that way. In order to prove causality, a more in-depth analysis " \
" should take place.")
st.markdown("2. To keep this report concise, only two explanatory factors are examined (poverty and housing development)," \
" other important factors such as proximity to transit, demographic shifts, and more were not included" \
" in order to keep the report concise.")
st.markdown("3. The analysis was kept to 2019-2022, which captures the short-term trends of the pandemic" \
" but fails to capture the long-term trends. This was done to keep the report concise.")
st.markdown("4. A significant amount of data was missing for districts in Staten Island and some districts in the Bronx, thus they were removed from the analysis" \
" which is why some districts do not appear in the analysis.")


st.markdown("---")
st.caption("For full details on data sources, variable definitions, and methodological choices, please see the Methods and References Page.")