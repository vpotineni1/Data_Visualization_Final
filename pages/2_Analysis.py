import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import altair as alt
from utils.data_loader import rental_data, mapping_data, housing_data, poverty_data, income_data, streeteasy_data

from charts.charts import (
    base_theme,
    choropleth,
    scatter_poverty,
    choropleth_mapping,
    ranked_bar
)

st.set_page_config(page_title="Story", layout="wide")
alt.themes.register("project", base_theme)
alt.themes.enable("project")

rental_data = rental_data()
housing_data = housing_data()
poverty_data = poverty_data()
income_data = income_data()
streeteasy_data = streeteasy_data()
mapping_data = mapping_data() 


st.title("Uneven Recovery Across New York City Neighborhoods")

st.write("The previous section showed that the COVID-19 pandemic caused a major shock to New York City neighborhoods. Rental prices quickly declined, while inventory levels rapidly increased." \
" Following this shock, was a gradual recovery in prices and invenntory levels. While examining borough level trends is eductional, it might hide important variations that occur within neighborhoods. In order" \
" to examine neighborhood level variation, the rest of the analysis will be focused on community districts. Community districts are government partitions of New York City, and offer an even deeper analysis into the" \
" rental market trends that occur in New York City. For example, some areas of the city may have experienced deeper rent declines or slower recoveries than others." \
" To understand how evenly the housing market recovered, we next examine changes in rental prices at the community district level. ")

st.header("Figure 3: Rent Declines and Recoveries Across Community Districts")

st.altair_chart(choropleth(rental_data, streeteasy_data, housing_data, mapping_data), use_container_width=True)

st.caption(" Figure 3 examines how the pandemic shock and subsequent recovery varied across New York City's community districts. The choropleth map" \
" shows the percentage decline in rental prices between 2019 and 2020, while the scatterplot compares each district's initial decline with the strength of its" \
" recovery between 2020 and 2022.")

st.write(" There are two main takeaways from Figure 3. First, rental declines varied widely across community districts in New York City. some disticts faced huge rent declines of more than 30%. For example," \
" community districts 305 and 302, which appear to be in Manhattan. While others, had smaller rent declines such as community districts 412 or 414, which are in Brooklyn, and had rent declines of less than 10%. " \
" Second, when we look at rent recovery, it appears to be extremely heterogenous, with some districts having very large rent prices, and others having very small rent price recoveries. For example, district 405, which is" \
" in Brooklyn had a rent recovery of almost 78%, while community District 412 only had a rent recovery of about 6%. ")

st.write(" While the map reveal that the recovery differed across districts, it is still diffucult to clearly identify which districts experienced the strongest and weakest" \
" recoveries. To better undestand the magnitude of these differences, the next figure ranks districts according to how much rents recovered between 2020 and 2022. This allows us to" \
" directly compare which neighborhoods rebounded the most and which continued to lag behind in recovery.")

st.header("Figure 4: Strongest and Weakest Rental Market Recoveries")

st.altair_chart(ranked_bar(rental_data, streeteasy_data, housing_data), use_container_width=True)

st.caption("Figure 4 ranks the community districts with the strongest and weakest rent recoveries between 2020 and 2022. Blue bars represent the districts where rents" \
" rebounded most strongly, while red bars highlight districts where recovery remained weak. This ranking makes it clear that some neighborhoods experienced rapid price " \
" rebounds while others lagged behind. This reinforces the idea that the housing recovery was extremely uneven across the city.  ")

st.write("The previous figures show that the effects of COVID-19 on New York City's rental market were far from uniform. Some community districts experienced sharp" \
" rent declines followed by strong recoveries, while others saw weaker rebounds. This raises an important question: what explains these differences across neighborhoods? One possible" \
" explanation lies in the socioeconomic characteristics of each district. In particular, poverty levels may influence how quickly and the magnitude to which housing markets recover" \
" from economic shocks.")

st.write(" To explore this relationship, the next visualization compares each district's poverty rate with the strength of its rental recovery between 2020 and 2022. Poverty rate serves as a proxy for" \
" socioeconomic vulnerability, allowing us to examine whether economically disadvantged neighborhods experienced different recovery patterns than 'richer' districts.")

st.header("Figure 5: Rent Recovery vs. Poverty Rate")

st.altair_chart(scatter_poverty(rental_data, streeteasy_data, housing_data, poverty_data), use_container_width=True)

st.caption(" Note: Poverty rates were used as a proxy for socioeconomic vulnerability.")

st.caption(" From Figure 5, there is an inverse relationship between recovery in rent price from 2020-2022 with poverty rate. Specifically, as poverty rate increases, it seems as if the rent price recovery in those districts tend to be smaller. " \
" While there are some outliers such as district 303 and district 101, the regression line shows that the average relationship is inverse. Thus, districts with lower poverty rates tend to cluster toward stronger recoveries, while districts with" \
" higher poverty rates are more likely to experience weaker rent recoveries.    ")

st.write(" This pattern indicates that the housing market recovery was not only geographically uneven, but also closely tied to underlying socioeconomic" \
" inequalities across neighborhoods. Districts with lower socioeconomic vulnerability appear to have rebounded more quickly and in a larger magnitude following the pandemic" \
" then more vulnerable communities that experienced smaller, and most likely slower recoveries. ")

st.write(" When we focus on the districts that were identified in Figure 4, the relationship becomes even more clear. For example, we can focus on comumunity districts 305 and 306  " \
" that had very strong recoveries and very small poverty rates at 11.8% and 9.0 % respectively. Moreover, when we look at districts with small rent recoveries such as 403 and 407, they both had " \
" much larger poverty rates at around 22%. Thus, while the relationship is not perfect for the 10 districts we focused on, on average, the regression line does show that as poverty rate increases," \
" thr rent recovery does seem to decrease as well. Moreover, the quadrant plot on the right makes this pattern especially clear. Nearly all weak recovery districts fall in the lower-right quadrant," \
" above the median poverty rate and below the median rent recoverty, while strong-recovery districts cluster in the upper-left. ")

st.write(" With that being said, the relationship is not completely clear between rent recovery and socioeconomic vulnerability. Poverty rates do not completely explain why some districts" \
" recovered in a larger magnitude than others. Thus, there must be another factor that plays an important role in influencing rent recoveries.")

st.write(" Specifically, the next chart will be focusing on housing development. According to Novogradac 2022, construction can leard to higher rent prices due to the increasing costs" \
" of construction, labor, and supplies following the pandemic. Thus, the next section of analysis will focus on housing development as a potential factor. New construction" \
" and real estate investment vary significantly across New York City, and neighborhoods that experienced most development during the recovery period may have seen different" \
" housing market dynamics. ")

st.write(" The next visualization examines housing development across community districts between 2020 and 2022. Specifically, it measures the housing completion rate. This is the number " \
" of newly completed housing units relative to the existing housing stock. This metric highlights where new construction was concentrated during the post-COVID recovery period. ")

st.header("Figure 6: Housing Development")

st.altair_chart(choropleth_mapping(rental_data, streeteasy_data, housing_data, mapping_data), use_container_width=True)

    
st.caption(" The choropleth maps housing completion rates across community districts, and the scatterplot compares them to rent recovery between 2020 and 2022.  ")

st.write("Housing construction during the COVID period varied widely across NYC districts. Some districts added relatively large numbers of new " \
" housing units compared to their existing housing stock, while others saw very little development. When comparing development with rental market recovery," \
" a relationship emerges. Several districts that experienced weaker rent recovery also saw relatively little new construction. ")

st.write("When we focus on the districts that had a strong vs. weak recovery that were identified in Figure 4, a pattern emerges, particularly among weak-recovery districts. All the districts that had weak recoveries" \
" such as 210, 112, and 403 had very little housing completion and also did not have large rent recoveries. When we look at the districts that had large rent recoveries, such " \
" as 303, 305, and 201, they had almost double the completion rate. However, the relationship is not perfect, which indicates that while housing development is an important factor" \
" it is not the only factor. There are other factors out there that explain why some districts recovered in terms of rent price at a larger magnitude than others.")

st.write("Taken together, these results, suggest that both socioeconomic vulnerability and housing development differences may have contributed to the uneven recovery" \
" of New York City's rental market. ")

st.write(" ")