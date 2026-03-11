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


st.title("Uneven Recovery Across New York City Community Districts")

st.write("The previous section established that the COVID-19 pandemic caused a major shock to New York City neighborhoods. Rental prices quickly declined, while inventory levels rapidly increased." \
" Following this shock, rental prices and inventory levels began to gradually recover. While examining borough-level trends is educational, it might hide important variations that occur within neighborhoods. In order" \
" to examine neighborhood-level variation, the rest of the analysis will be focused on community districts. Community districts are administrative divisions of New York City, and offer an even deeper analysis into " \
" rental market trends. For example, some areas of the city may have experienced larger rent declines or slower recoveries than others." \
" To understand how evenly the housing market recovered, we next examine changes in rental prices at the community district level. ")

st.write("Note: Community Districts are three digit numbers, and the first digit corresponds to the borough they are in. 1 maps to the Bronx, 2 maps to Brooklyn, 3 maps to Manhattan, 4 maps to Queens, and 5 to Staten Island.")


st.write("The two measures used to measure the impact of the pandemic on rental markets were rent decline and rent recovery. Rent decline" \
" refers to the percentage drop between the median rent in 2019 and the lowest rent in 2020, capturing the immediate impact of the pandemic." \
" Rent recovery refers to the percentage increase in rent between 2020 and 2022 to capture the strength of rent rebounds. ")

st.header("Figure 3: Rent Declines and Recoveries Varied Widely Across Community Districts")

st.altair_chart(choropleth(rental_data, streeteasy_data, housing_data, mapping_data), use_container_width=True)

st.caption(" Figure 3 shows how rental price declines and subsequent recoveries varied across NYC community districts. The choropleth " \
" map displays the percentage decline in rent between 2019-2020 and recovery between 2020-2022. The scatterplot compares" \
" each district's initial decline with the strength of its recovery between 2020 and 2022. Together, these visualizations highlight the " \
" wide variation in rental market changes due to the economic shock caused by the pandemic. Moreover, this figure is interactive, so you can " \
" click a district on the choropleth and it will highlight on the scatterplot. ")

st.write(" There are two main takeaways from Figure 3. First, rental declines varied widely across community districts in New York City. Some districts faced huge rent declines of more than 30%. For example," \
" community districts 305 and 302, which are in Manhattan. While others, had smaller rent declines such as community districts 412 or 414, which are in Brooklyn, and had rent declines of less than 10%. " \
" Second, when we look at rent recovery, it appears to be extremely heterogeneous, with some districts having very large rent recoveries, and others having very small rent price recoveries. For example, district 405, which is" \
" in Brooklyn had a rent recovery of almost 78%, while community district 412 only had a rent recovery of about 6%. ")

st.write(" Although the map and scatterplot show substantial variation in both declines and recoveries, it is still difficult to identify which districts experienced the strongest and weakest" \
" recoveries. To better understand these differences, the next figure ranks community districts according to how rents in 2022 compare to their pre-pandemic levels"
" in 2019. This ranking makes it easier to see which neighborhoods rebounded the most and which continued to lag behind.")

st.header("Figure 4: Strongest and Weakest Rental Market Recoveries")

st.altair_chart(ranked_bar(rental_data, streeteasy_data, housing_data), use_container_width=True)

st.caption("Figure 4 ranks the community districts according to how strongly rents recovered relative to pre-pandemic levels. This metric is calculated" \
" by taking the ratio of the median rent price in 2022 to median rent price in 2019. This was done to see which districts had the largest rent recoveries relative to 2019 rent." \
" Blue bars represent the districts where rents  rebounded most strongly, while red bars highlight districts where recovery remained weak. Values above 1 indicate rents" \
" exceeded their pre-pandemic levels, while values below 1 indicate rents remained below pre-pandemic levels." )

st.write(" The 5 districts that had the strongest rent recovery, meaning their rents in 2022 were much larger than in 2019, are 101 (Bronx)," \
" 303, 305, 306 (Manhattan), and 201 (Brooklyn). The 5 that had the weakest rent recovery were 112, 111, 210, 403, and 407 (Queens). Considering that districts" \
" in the same borough both had strong and weak rental recoveries relative to 2019 levels that suggests geographic location alone does not explain why some" \
" districts rebounded more strongly than others. Thus, this raises an important question of what factors might explain these differences in recovery across" \
" community districts? " )

st.write(" One plausible explanation lies in the socioeconomic characteristics of each district. In particular, poverty levels may influence how strongly"
" local rental markets recover from economic shocks. For example, poorer districts, tend to be rent stabilized (Realini 2025), which might limit the extent to " \
" which rents in those districts recovered to pre-pandemic levels. To explore this relationship, the next visualization compares each district's poverty rate with the strength of its rental recovery between 2020 and 2022. Poverty rate serves as a proxy for" \
" socioeconomic vulnerability, allowing us to examine whether economically disadvantaged neighborhoods experienced different recovery patterns than 'richer' districts.")

st.write("In the following figures in the report, blue points highlight the districts with the strongest rent recovery, while red points highlight" \
" districts with the weakest recovery (identified in Figure 4). Focusing on these districts makes it easier to see how different socioeconomic and development factors" \
" relate to recovery patterns.")

st.header("Figure 5: Rent Recovery vs. Poverty Rate")

st.altair_chart(scatter_poverty(rental_data, streeteasy_data, housing_data, poverty_data), use_container_width=True)

st.caption("Figure 5 examines the relationship between poverty rate and rent recovery. The downward slope of the regression line indicates that there is an inverse relationship between recovery in rent price (2020-2022) with poverty rate. " \
" Specifically, as poverty rate increases, it seems as if the rent price recovery in those districts tend to be smaller. " \
" While there are some outliers such as district 303 and district 101, the overall patterns suggest that the average relationship is inverse, and districts with lower poverty rates" \
" tended to experience the strongest rent recoveries.")

st.write(" This pattern indicates that the housing market recovery was not only geographically uneven, but also closely tied to underlying socioeconomic" \
" inequalities across neighborhoods. Districts with lower socioeconomic vulnerability appear to have rebounded in a larger magnitude following the pandemic" \
" than more vulnerable communities that experienced smaller, and most likely slower recoveries. ")

st.write(" When we focus on the districts that were identified in Figure 4, the relationship becomes even clearer. For example, we can focus on community districts 305 and 306  " \
" that had very strong recoveries and very small poverty rates at 11.8% and 9.0% respectively. Moreover, when we look at districts with small rent recoveries such as 403 and 407, they both had " \
" much larger poverty rates at around 22%. Thus, while the relationship is not perfect for the 10 districts we focused on, on average, the regression line does show that as poverty rate increases," \
" the rent recovery does seem to decrease as well. Moreover, the quadrant plot on the right makes this pattern especially clear. Nearly all weak recovery districts fall in the lower-right quadrant," \
" above the median poverty rate and below the median rent recovery, while strong-recovery districts cluster in the upper-left. ")

st.write(" With that being said, the relationship is not completely clear between rent recovery and socioeconomic vulnerability. Poverty rates do not completely explain why some districts" \
" recovered in a larger magnitude than others as the relationship is not perfect. Thus, there must be another factor that plays an important role in influencing rent recoveries.")

st.write(" One potential factor is housing development. According to Novogradac (2022), construction can lead to higher rent prices due to the increasing costs" \
" of construction, labor, and supplies that followed the pandemic. Moreover, another strong argument that is made is that housing development may signal stronger economic" \
" activity in a district, which can increase demand and lead to higher rent prices. Thus, the next section of analysis will focus on housing development as a potential factor. New construction" \
" and real estate investment vary significantly across New York City, and neighborhoods that experienced the most development during the recovery period may have seen different" \
" housing market dynamics. ")

st.write(" The next visualization examines housing development across community districts between 2020 and 2022. Specifically, it measures the housing completion rate. This is the number " \
" of newly completed housing units relative to the existing housing stock. This metric highlights where new construction was concentrated during the post-COVID recovery period. ")

st.header("Figure 6: Housing Development")

st.altair_chart(choropleth_mapping(rental_data, streeteasy_data, housing_data, mapping_data), use_container_width=True)

st.caption(" Figure 6 displays a choropleth that maps housing completion rates across community districts, and the scatterplot compares them to rent recovery between 2020 and 2022. This figure is interactive" \
" so specific districts can be clicked on the map, and they will then be highlighted on the scatterplot. From this map, it is clear that different districts had different levels of development, but the most important" \
" takeaway is the clear relationship between housing completion rate and rental recovery. As the housing completion rate increases, on average, rental recovery" \
" also increases. ")

st.write("When we focus on the districts that had a strong versus weak recovery that were identified in Figure 4, a pattern emerges, particularly among weak-recovery districts. All the districts that had weak recoveries" \
" including 210, 112, and 403 had very little housing completion and also did not have large rent recoveries as they clustered in the bottom left corner of the plot. When we look at the districts that had large rent recoveries, such " \
" as 303, 305, and 201, they had almost double the completion rate at around 4%. However, the relationship is not perfect, which indicates that while housing development is an important factor" \
" it is not the only factor. There are other factors out there that explain why some districts recovered in terms of rent prices at a larger magnitude than others.")

st.write("Taken together, these results suggest that both socioeconomic vulnerability and housing development differences contributed to the uneven" \
" recovery of New York City's rental market. Districts with lower poverty rates and more active housing construction tended to rebound more strongly" \
" , while economically vulnerable districts with little new development lagged behind.")

st.write("This raises a more fundamental question: did stronger rent recovery actually make neighborhoods better or worse off in terms of affordability?" \
" To isolate the direct effect of rent changes alone, the next section compares how rent burdens changed across districts between 2019 and 2022," \
" holding household income constant at 2019 levels. This allows us to ask, purely as a result of how rent moved, whether residents" \
" end up paying a larger or smaller share of their income on rent by 2022. ")