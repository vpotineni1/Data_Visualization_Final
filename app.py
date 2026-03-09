import streamlit as st
from PIL import Image

st.set_page_config(page_title="New York City Housing Market - Vishal Potineni, Mike Gladden, Rylan Kruep", layout="wide")


st.title("Did the COVID-19 Pandemic Produce an Uneven Housing Recovery across New York City Community Districts?")


st.image('images/NYC_000021208828-2100-980.jpg', use_container_width = True)

st.write(" The New York City housing market is one of the most expensive and closely watched housing markets in the United States. Housing costs represent a major share of household expenses " \
" in the city, changes in rental prices can have significant consequences for residents across different neighborhoods.")

st.write(" The COVID-19 pandemic produced one of the most dramatic disruptions to the United States economy in recent history. As the pandemic began in early 2020, many residents left the city (U.S. News, 2020), which" \
" led to the demand for housing decreasing. Rental prices declined across much of New York City, while vacancies increased. By 2022, however, rental demand returned and prices began to recover (Off the MRKT, 2024). " \
" Thus, for this specific exploration, the specific time period that will be considered post-pandemic is 2020 - 2022, which captures both the initial pandemic shock and the early stages of the " \
" housing amrket recovery.  ")

st.write(" While the overall trajectory of the housing market is well documented across the boroughs, an important question that this report aims to answer" \
" is if all neighborhoods experienced the pandemic shock and recovery in the same way? Economic shocks often affect neighborhoods differently depending on" \
" local economic conditions, housing supply, demographic factors and more. As a result, some neighborhoods might have recovered more quickly than others, while some " \
" still experienced lingering effects of the pandemic.")

st.markdown(" This project explores how the COVID-19 pandemic reshaped rental markets across New York City by answering three questions:")
            
st.markdown("1. How did the COVID-19 Pandemic affect NYC rental prices and housing supply?")

st.markdown("2. Did all neighborhoods recover equally, in terms of time and magnitude, and if not why?")

st.markdown("3. What do these changes reveal about housing affordability across the city?")

st.write("We begin by examining borough-level rental trends before and fter the pandemic, which establishes the baseline conditions and scale of the shock.")

#TALK ABOUT DATASET HERE PROBABLY

