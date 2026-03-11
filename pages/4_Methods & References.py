import streamlit as st



st.header("Datasets")

st.markdown("In this analysis, 5 different datasets were utilized:" )

st.markdown("The first dataset came from StreetEasy, which is a leading NYC real estate website" \
" that aggregates rental and sales data. For this analysis the dataset was aggregated to the community district" \
" level (mapping from neighborhood to community district was done manually) and used to construct two key mentrics including median asking rent and rental inventory. These" \
" variables were used to construct the price and inventory index, and also forms the basis for calculating the rent" \
" decline and rent recovery metrics. ")

st.markdown("The second dataset is the NYC Community District GeoJSON from the NYC Department of City Planning. This" \
" was used to make the choroopleth maps in the report. ")

st.markdown("The third dataset is the NYC Housing Devlopment Data from the NYC Department of City Planning. This dataset" \
" provides information on new housing construction and completion across New York City community districts. This dataset" \
" was used to compute the housing completion rate for Figure 6. ")

st.markdown("The fourth dataset is the Poverty Rates by Community Districts also from the NYC Department of City Planning." \
" This dataset was manually created as there was not one combined list online, so we had to manually go through the community districts" \
" on the website and make the datset. ")

st.markdown("The fifth dataset is median household income by Communtiy District which is from Keeping Track Online. Like the above, there was not " \
" a downloadable list, so we manually scraped the income data onto a .csv file. ")

st.header("Metrics Calculated:")

st.write("Price Index: Measures how median rent in a given month compares to the district's median rent in 2019 ")
st.write("Inventory Index: Measures how average inventory in a given month compares to the district's average inventory in 2019 ")
st.write("Rent Decleine (2019-2020): This metric measures the percentage decrease in median rent between the 2019 baseline and the lowest" \
" median rent observed during 2020. This metric was calculated to capture the percentage by which rent declined from 2019, and thus put the shock " \
" into context.")
st.write("Rent Recovery (2020-2022): Rent Recovery measures the percentage increase in median rent between the district's lowest recorded rent in 2020" \
" and its median rent in 2022. This metric was calculated to capture the percentage by which rent recovered in the immediate aftermath of the pandemic.")
st.write("Housing Completion Rate: The number of newly completed housing units between 2020 and 2022 divided by the existing housing stock in the district." \
" This was metric was designed to capture the magnitude of housing development that occured during the recovery period.")



st.header("References")

st.write("Dataset Links:")

st.markdown(" * Buffa, P. (2022, June 28). Observable. Observable. https://observablehq.com/@observablehq/streeteasy-real-estate-data?collection=@observablehq/datasets")

st.markdown(" * (2025). Nyc.gov. https://www.nyc.gov/content/planning/pages/resources/datasets/community-districts")

st.markdown(" * City. (2021, January 23). Housing Database by Community District. Cityofnewyork.us. https://data.cityofnewyork.us/Housing-Development/Housing-Database-by-Community-District/dbdt-5s7j/data_preview")

st.markdown(" * NYC Community District Profiles. (n.d.). Communityprofiles.planning.nyc.gov. https://communityprofiles.planning.nyc.gov/")

st.markdown("* Median Incomes. (2026). Cccnewyork.org. https://data.cccnewyork.org/data/table/66/median-incomes#66/107/131/abbr/d")

st.write("References for Articles:")

st.markdown (" * Realini, D. P. (2025, November 15). How the Past Decade has Changed in the New York City Rental Market. Medium. https://medium.com/@paulrealini/how-the-past-decade-has-changed-in-the-new-york-city-rental-market-4b5a8e5e2a16")

st.markdown ("Hubbard, K. (2020). New York City’s Falling Rents Reflect the Pain of COVID-19. US News & World Report; U.S. News & World Report. https://www.usnews.com/news/cities/articles/2020-10-15/new-york-citys-falling-rents-reflect-the-trauma-of-covid-19")

st.markdown ("Lindy, J. (2024, August 21). Off The MRKT. Off the MRKT. https://www.offthemrkt.com/lifestyle/the-evolution-of-rental-prices-in-manhattan-over-the-last-decade")

