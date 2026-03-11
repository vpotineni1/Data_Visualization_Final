import streamlit as st
from PIL import Image

st.set_page_config(page_title="New York City Housing Market - Vishal Potineni, Mike Gladden, Rylan Kruep", layout="wide")


st.title("The Uneven Recovery of New York City's Rental Market After COVID-19")


st.image('images/NYC_000021208828-2100-980.jpg', use_container_width = True)

st.write(" The New York City housing market is one of the most expensive and closely watched housing markets in the United States. Considering that housing costs represent a major share of household expenses " \
" in the city, changes in rental prices can have significant consequences for residents across different neighborhoods.")

st.write(" One of the largest changes in rental prices that had occurred in New York City was the COVID-19 pandemic, which produced one of the most dramatic disruptions to the United States economy in recent history. As the pandemic began in early 2020, many residents left the city (U.S. News, 2020), which" \
" led to the demand for housing decreasing. Rental prices declined across much of New York City, while vacancies increased. By 2022, however, rental demand returned and prices began to recover (Off the MRKT, 2024). " \
" Thus, the specific time period that will be considered for the recovery is 2020 - 2022, which captures both the initial pandemic shock and the early stages of the " \
" housing market recovery.  ")

st.write(" While the overall trajectory of the housing market is well documented across the boroughs, an important question that this report aims to answer" \
" is whether all neighborhoods experienced the pandemic shock and recovery in the same way? Economic shocks often affect neighborhoods differently depending on" \
" local economic conditions, housing supply, demographic factors and more. As a result, some neighborhoods might have recovered more quickly than others, while some " \
" still experienced lingering effects of the pandemic.")

st.markdown(" With that in mind, this project explores how the COVID-19 pandemic reshaped rental markets across New York City by answering three questions:")
            
st.markdown("1. How did the COVID-19 pandemic affect NYC rental prices and housing supply?")

st.markdown("2. Did all neighborhoods recover equally in magnitude, and if not, why?")

st.markdown("3. What do these changes reveal about housing affordability across the city?")


st.write("This analysis draws on five datasets covering the period 2019 to 2022. This includes rental market data from StreetEasy, the housing database from the Department of City Planning (2025)," \
" income data by community district from Keeping Track Online, poverty rate data by community district from NYC City Planning, and GeoJSON data to map the NYC community districts from NYC Planning. Together these datasets allow" \
" for a comprehensive analysis of how the pandemic affected rental markets across New York City community districts between 2019 and 2022. ")

st.write("A key metric that is used throughout this report is rent recovery, which is defined as the percentage increase" \
" in median asking rent between a district's lowest recorded rent in 2020 and its median rent in 2022. This captures how much" \
" of the pandemic-era rent decline each district recouped during the early recovery period. A district with a higher" \
" rent recovery rebounded more strongly from the initial pandemic shock, while a district with a lower recovery rate" \
" saw rents remain closer to their pandemic lows by 2022.")

st.write("With a few clarifications out of the way, we begin by examining borough-level rental trends before and after the pandemic, which establishes the baseline conditions and the scale of the shock" \
" before zooming to community district differences in the analysis section.")


st.markdown("- - - ")
st.caption("Note: For more information about the datasets and methodology used in this report, please see the Methods & References Page. The metrics and dataset are talked" \
" about briefly in this report, however, most of the discussion takes place in the Methods & References Page.")