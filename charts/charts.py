import geopandas as gpd
import json
import pandas as pd
import numpy as np
import altair as alt


def base_theme():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "legend": {"labelFontSize": 12, "titleFontSize": 14},
        }
    }

def pre_covid_data_transformation(rental_data : pd.DataFrame) -> pd.DataFrame:
    df = rental_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df['medianAskingRent'] > 0]
    df = df[['neighborhood','borough','date','discountShare', 'medianAskingRent', 'totalInventory']]
    df_monthly = (df.groupby(['borough', 'date'], as_index = False).agg({'discountShare':'mean', 'medianAskingRent':'median', 'totalInventory' : 'mean'}))
    df_baseline = df_monthly[df_monthly["date"].dt.year == 2019].groupby("borough").agg({'discountShare':'mean', 'medianAskingRent':'median', 'totalInventory' : 'mean'}).reset_index()
    df_monthly = df_monthly.merge(df_baseline, on = 'borough')
    df_monthly['price_index'] = (df_monthly['medianAskingRent_x'] / df_monthly['medianAskingRent_y'])
    df_monthly['difference_discounts'] = (df_monthly['discountShare_x'] - df_monthly['discountShare_y'])
    df_monthly['inventory_index'] = (df_monthly['totalInventory_x'] / df_monthly['totalInventory_y'])
    
    return df_monthly


def pre_covid_trends_chart(rental_data: pd.DataFrame) -> alt.Chart:

    chart_data = pre_covid_data_transformation(rental_data)

    chart_data = chart_data[chart_data['date'] < "2020-03-01"].copy()
    chart_data = chart_data.melt(
        id_vars=["borough", "date"],
        value_vars=["price_index", 'difference_discounts', "inventory_index"],
        var_name="metric",
        value_name="value")

    options = ['price_index', 'inventory_index']
    labels = ['Price Index', 'Inventory Index']
    input_dropdown = alt.binding_radio(options=options, labels=labels , name='Metric: ')
    
    select = alt.selection_point(fields = ['metric'], bind = input_dropdown, value = [{'metric': 'price_index'}])

    select2 = alt.selection_point(fields = ['borough'])

    
    chart= alt.Chart(chart_data, title = 'NYC Rental Market was Stable Pre-Pandemic').mark_line().encode(
        x = alt.X('date:T', title = 'Month'),
        y = alt.Y("value:Q", scale = alt.Scale(zero = False), title = 'Price/Inventory Index (2019 = 1)'),
        color = alt.Color('borough:N', title = 'Borough'),
        tooltip = [alt.Tooltip('borough:N', title = 'Borough'), alt.Tooltip('date:T', title = 'Month'), alt.Tooltip('value:Q', title = 'Index', format ='.2f' )],
        opacity = alt.condition(select2, alt.value(1), alt.value(0.2)),).add_params(select, select2).transform_filter(select).properties(width = 700, height = 400)

    return chart


def post_covid_trends_chart(rental_data: pd.DataFrame) -> alt.Chart:

    chart_data = pre_covid_data_transformation(rental_data)
    chart_data = chart_data[chart_data['date'] > "2020-01-01"].copy()


    select2 = alt.selection_point(fields = ['borough'])


    options = ['price_index', 'inventory_index']
    labels = ['Price Index', 'Inventory Index']
    input_dropdown = alt.binding_radio(options=options, labels=labels , name='Metric: ')

    select = alt.selection_point(fields = ['metric'], bind = input_dropdown, value = [{'metric': 'price_index'}])

    chart_data = chart_data.melt(
        id_vars=["borough", "date"],
        value_vars=["price_index", "inventory_index"],
        var_name="metric",
        value_name="value")
    
    covid_df = pd.DataFrame({'date' : ['2020-03-01'], 'label' : ['COVID-19 Shock']})

    

    line_covid = alt.Chart(covid_df).mark_rule(color = 'red').encode(x = 'date:T')

    covid_text = alt.Chart(covid_df).mark_text(
    align = 'left',
    dx = 7,
    dy = -110
    ).encode(
        x = 'date:T',
        text = 'label:N')


    structural_line = (alt.Chart(chart_data,  title = 'COVID-19 Triggered a Sharp Shock in NYC Rental Prices and Inventory').mark_line().encode(
        x=alt.X('date:T', title = 'Month'),
        y=alt.Y('value:Q', scale = alt.Scale(zero = False), title = 'Price/Inventory Index (2019 = 1)' ),
        color=alt.Color('borough:N'),
        tooltip = [alt.Tooltip('borough:N', title = 'Borough'), alt.Tooltip('date:T', title = 'Month'), alt.Tooltip('value:Q', title = 'Index', format ='.2f' )],
        opacity = alt.condition(select2, alt.value(1), alt.value(0.2)),).add_params(select, select2).transform_filter(select).properties(width = 700, height = 400)
    )
    
    chart = structural_line + line_covid + covid_text

    return chart

def choropleth_data_transformation(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame) -> pd.DataFrame:
    df = rental_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    mapping = streeteasy_data[['neighborhood', 'borough', 'communityDistrict']].drop_duplicates()
    df = df.merge(mapping, on = ['neighborhood', 'borough'], how = 'left')

    df = df[df['medianAskingRent'] >0]


    rentals_agg = df.groupby(['communityDistrict','year']).agg(
        rent_median = ("medianAskingRent", "median"),
        rent_min = ("medianAskingRent","min"),
        inventory_total = ("totalInventory", "sum"),
        ).reset_index()

    rentals_agg = rentals_agg.merge(housing_data, on = 'communityDistrict', how = 'left')

    baseline_2019 = rentals_agg[rentals_agg['year'] == 2019][['communityDistrict', 'rent_median']]
    baseline_2019.rename(columns = {'rent_median' : 'rent_median_2019'}, inplace = True)

    lowest_2020 = rentals_agg[rentals_agg['year'] == 2020][['communityDistrict', 'rent_min']]
    rent_2022 = rentals_agg[rentals_agg['year'] == 2022][['communityDistrict', 'rent_median']]
    rent_2022 .rename(columns = {'rent_median' : 'rent_median_2022'}, inplace = True)
    
    viz_summary = baseline_2019.merge(lowest_2020, on = 'communityDistrict', how = 'left')
    viz_summary = viz_summary.merge(rent_2022, on = 'communityDistrict', how ='left')

    
    viz_summary['decline_2019_2020'] = ((viz_summary['rent_min'] - viz_summary['rent_median_2019']) / viz_summary['rent_median_2019'])
    viz_summary['recovery_2020_2022'] = ((viz_summary['rent_median_2022'] - viz_summary['rent_min']) / viz_summary['rent_min'])

    viz_summary['communityDistrict'] = viz_summary['communityDistrict'].astype(int)


    viz_summary = viz_summary.replace([np.inf, -np.inf], np.nan)

    viz_summary = viz_summary.dropna(subset=["rent_median_2022", "rent_min", "rent_median_2019"])
    
    return viz_summary


def choropleth(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, mapping_data:pd.DataFrame ) -> alt.Chart:

    chart_data = choropleth_data_transformation(rental_data,streeteasy_data,housing_data)
    
    options = ["decline_2019_2020", "recovery_2020_2022"]
    labels = ["% Rent Decline (2019 - 2020)", "% Rent Recovery (2020 - 2022)"]
    
    input_dropdown = alt.binding_radio(options=options, labels=labels , name='Metric: ')
    select = alt.selection_point(fields = ['metric'], bind = input_dropdown, value = [{'metric': "decline_2019_2020"}])

    geo_features = mapping_data.__geo_interface__["features"]
    for feature in geo_features:
        feature["properties"]["communityDistrict"] = int(feature["properties"]["BoroCD"])

    CD_select = alt.selection_point(fields = ['communityDistrict'])
    
    choropleth = alt.Chart(alt.Data(values=geo_features)).mark_geoshape(stroke="black",strokeWidth=0.5).transform_lookup(lookup = 'properties.BoroCD',
                                                                                          from_ = alt.LookupData(chart_data, key = 'communityDistrict', fields = options + ['communityDistrict'])
                                                                 ).transform_fold(options, as_ = ['metric', 'value']).transform_filter(select).encode(
                                                                     color = alt.Color('value:Q', title = '% Change', scale = alt.Scale(scheme = 'redblue'), legend = alt.Legend(orient = 'left', format ='.0%' )),
                                                                     opacity = alt.condition(CD_select, alt.value(1), alt.value(0.2)),
                                                                     tooltip = [alt.Tooltip("properties.BoroCD:N", title = 'District'), alt.Tooltip("metric:N", title = "Metric"), alt.Tooltip("value:Q", format = ".2%", title = 'Value')]).add_params(select, CD_select).project(type = 'albers').properties(width = 600, height = 600)
    
    scatter = alt.Chart(chart_data).mark_circle(size = 100).encode(
        x = alt.X('decline_2019_2020:Q', title = "% Decline in Rent Price from 2019 - 2020", axis = alt.Axis(format = '%')),
        y = alt.Y('recovery_2020_2022:Q', title = '% Rent Recovery from 2020 - 2022', axis = alt.Axis(format = '%')),
        opacity = alt.condition(CD_select, alt.value(1), alt.value(0.2)),
        tooltip = alt.Tooltip('communityDistrict:N')).add_params(CD_select).properties(width = 600, height = 600)
    
    chart = (choropleth | scatter)

    return chart


def scatter_poverty(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, poverty_data:pd.DataFrame) -> alt.Chart:

    df4= poverty_data.copy()
    df4['poverty_rate'] = pd.to_numeric(df4['poverty_rate'], errors='coerce')

    chart_data = choropleth_data_transformation(rental_data,streeteasy_data,housing_data)

    chart_data = chart_data.merge(df4, on = 'communityDistrict', how = 'inner')

    poverty_median = chart_data["poverty_rate"].median()
    recovery_median = chart_data["recovery_2020_2022"].median() 

    top5_districts = [101,303, 305, 306, 201]
    bottom5_districts = [112,111,210,407,403]

    chart_data['recovery_group'] = 'Other'
    chart_data.loc[chart_data['communityDistrict'].isin(top5_districts),'recovery_group'] = 'Strong Recovery'
    chart_data.loc[chart_data['communityDistrict'].isin(bottom5_districts),'recovery_group'] = 'Weak Recovery'


    chart1 = alt.Chart(chart_data).mark_circle(size = 80).encode(
        x = alt.X("poverty_rate:Q", title = "Poverty Rate (%)", axis = alt.Axis(format = '%')),
        y = alt.Y("recovery_2020_2022:Q", title = '% Rent Recovery from 2020 - 2022', axis = alt.Axis(format = '%')),
        color = alt.Color("recovery_group:N", scale = alt.Scale(domain = ['Strong Recovery', 'Weak Recovery', 'Other'], range = ['blue', 'red', 'gray']),legend = alt.Legend(title = 'Recovery Group')),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip("poverty_rate:Q", format=".1%", title = 'Poverty Rate'), alt.Tooltip("recovery_2020_2022:Q", format=".2%", title = '% Rent Recovery')]
        ).properties(height = 400, width = 400)
    
    line = alt.Chart(chart_data).transform_regression("poverty_rate", "recovery_2020_2022").mark_line(color = 'black').encode(
        x = "poverty_rate:Q",
        y = "recovery_2020_2022:Q"
    )

    chart2 = alt.Chart(chart_data).mark_circle(size = 80).encode(
        x = alt.X("poverty_rate:Q", title = "Poverty Rate (%)", axis = alt.Axis(format = '%')),
        y = alt.Y("recovery_2020_2022:Q", title = '% Rent Recovery from 2020 - 2022', axis = alt.Axis(format = '%')),
        color = alt.Color("recovery_group:N", scale = alt.Scale(domain = ['Strong Recovery', 'Weak Recovery', 'Other'], range = ['blue', 'red', 'gray']), legend = alt.Legend(title = 'Recovery Group')),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip("poverty_rate:Q", format=".1%", title = 'Poverty Rate'), alt.Tooltip("recovery_2020_2022:Q", format=".2%", title = '% Rent Recovery')]
        ).properties(height = 400, width = 400)

    
    xline = alt.Chart(pd.DataFrame({"y":[recovery_median]})).mark_rule().encode(y="y:Q")
    yline = alt.Chart(pd.DataFrame({"x":[poverty_median]})).mark_rule().encode(x="x:Q")

    chart1_final = chart1 + line

    chart2_final = chart2 + xline + yline

    chart_final = (chart1_final | chart2_final)
    
    return chart_final



def choropleth_mapping(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, mapping_data:pd.DataFrame) -> alt.Chart:

    chart_data = choropleth_data_transformation(rental_data,streeteasy_data,housing_data)
    
    choropleth_data = chart_data.copy()
    choropleth_data = choropleth_data.merge(housing_data, on = "communityDistrict")
    choropleth_data["communityDistrict"] = choropleth_data["communityDistrict"].astype(int)

    top5_districts = [101,303, 305, 306, 201]
    bottom5_districts = [112,111,210,407,403]

    choropleth_data['recovery_group'] = 'Other'
    choropleth_data.loc[choropleth_data['communityDistrict'].isin(top5_districts),'recovery_group'] = 'Strong Recovery'
    choropleth_data.loc[choropleth_data['communityDistrict'].isin(bottom5_districts),'recovery_group'] = 'Weak Recovery'

    geo_features = mapping_data.__geo_interface__["features"]
    for feature in geo_features:
        feature["properties"]["communityDistrict"] = int(feature["properties"]["BoroCD"])

    CD_select = alt.selection_point(fields=['communityDistrict'])

    choropleth = alt.Chart(alt.Data(values=geo_features)).mark_geoshape(stroke="black",strokeWidth=0.5
            ).transform_lookup(lookup = 'properties.communityDistrict', from_ = alt.LookupData(choropleth_data, key = 'communityDistrict', fields = ['completion_rate', 'communityDistrict'])
            ).encode(
                color = alt.Color('completion_rate:Q', title = 'Housing Completion Rate', legend = alt.Legend(orient = 'left', format = '.0%')),
                opacity = alt.condition(CD_select, alt.value(1), alt.value(0.3)),
                tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip('completion_rate:Q', format = '.2%', title = 'Completion Rate' )]
            ).project(type = 'albers').add_params(CD_select).properties(width = 400, height = 500)
    
    line = alt.Chart(choropleth_data).transform_regression("completion_rate", "recovery_2020_2022").mark_line(color = 'black').encode(
        x = "completion_rate:Q",
        y = "recovery_2020_2022:Q"
    )
    
    scatter = alt.Chart(choropleth_data).mark_circle(size = 80).encode(
        x = alt.X("completion_rate:Q", title = '% Housing Completion Rate (2020 - 2022)',  axis = alt.Axis(format = '%')),
        y = alt.Y("recovery_2020_2022", title = '% Rental Recovery (2020 - 2022)',  axis = alt.Axis(format = '%')),
        color = alt.Color("recovery_group:N", scale = alt.Scale(domain = ['Strong Recovery', 'Weak Recovery', 'Other'], range = ['blue', 'red', 'gray']), legend = alt.Legend(title = 'Recovery Group')),
        opacity = alt.condition(CD_select, alt.value(1), alt.value(0.2)),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip("completion_rate:Q", format=".1%", title = 'Completion Rate'), alt.Tooltip("recovery_2020_2022:Q", format=".2%", title = '% Rent Recovery')]
        ).properties(width = 600, height = 600)
    
    scatter = scatter + line

    chart = (choropleth | scatter)
    return chart
    


def rent_burden_transformation(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, income_data:pd.DataFrame) -> pd.DataFrame:

    df = rental_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df['date'].dt.year
    
    mapping = streeteasy_data[['neighborhood', 'borough', 'communityDistrict']].drop_duplicates()
    df = df.merge(mapping, on = ['neighborhood', 'borough'], how = 'left')

    df = df[df['medianAskingRent'] > 0]

    rent_year = df.groupby(['communityDistrict','year'])['medianAskingRent'].median().reset_index(name = "median_rent")

    rent_2019 = rent_year[rent_year['year'] == 2019]
    rent_2022 = rent_year[rent_year['year'] == 2022]

    income_rent_2019 = rent_2019.merge(income_data, on ='communityDistrict', how = 'inner')
    income_rent_2022 = rent_2022.merge(income_data, on ='communityDistrict', how = 'inner')
        

    income_rent_2019['ratio_2019'] = (income_rent_2019['median_rent'] * 12) / income_rent_2019['Median_Household_Income']
    income_rent_2022['ratio_2022'] = (income_rent_2022['median_rent'] * 12) / income_rent_2022['Median_Household_Income']

    income_rent = income_rent_2019.merge(income_rent_2022, on = 'communityDistrict', how = 'inner')

    income_rent['change'] = income_rent['ratio_2022'] - income_rent['ratio_2019']  

    return income_rent
    

def rent_burden_visualization(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, income_data:pd.DataFrame, housing_data:pd.DataFrame) -> alt.Chart:

    recovery_data = choropleth_data_transformation(rental_data, streeteasy_data, housing_data)

    income_rent = rent_burden_transformation(rental_data, streeteasy_data, income_data)
    
    income_rent = income_rent.merge(recovery_data[['communityDistrict', 'recovery_2020_2022']], on = 'communityDistrict', how = 'left')

    top5_districts = [101,303, 305, 306, 201]
    bottom5_districts = [112,111,210,407,403]

    income_rent['recovery_group'] = 'Other'
    income_rent.loc[income_rent['communityDistrict'].isin(top5_districts),'recovery_group'] = 'Strong Recovery'
    income_rent.loc[income_rent['communityDistrict'].isin(bottom5_districts),'recovery_group'] = 'Weak Recovery'

    top10 = income_rent.sort_values('change', ascending=False).head(10)
    filter_out = ~income_rent['communityDistrict'].isin(top10['communityDistrict'].tolist())
    outside_10 = income_rent[filter_out]

    base_scatter = alt.Chart(income_rent).mark_circle(size = 80).encode(
        x = alt.X('recovery_2020_2022:Q', title='% Rent Recovery  (2022 - 2019)', axis = alt.Axis(format = '%')),
        y= alt.Y('change:Q', title='Change in Rent-to-Income Ratio (2022 - 2020)', axis = alt.Axis(format = '%')),
        tooltip=[alt.Tooltip('communityDistrict:N', title='District'), alt.Tooltip('change:Q', title = '% Change in Rent Burden', format='.1%'), alt.Tooltip("recovery_2020_2022:Q", title = '% Rent Recovery', format = '.1%') ], 
        color = alt.Color("recovery_group:N", scale = alt.Scale(domain = ['Strong Recovery', 'Weak Recovery', 'Other'], range = ['blue', 'red', 'gray']), legend = alt.Legend(title = 'Recovery Group')),
        )
    
    trend = alt.Chart(income_rent).transform_regression('recovery_2020_2022', 'change').mark_line().encode(
        x = 'recovery_2020_2022:Q',
        y = 'change:Q')
    
    scatter = (base_scatter + trend).properties(width = 500, height = 500)
    
    bars = alt.Chart(top10).mark_bar().encode(
        x=alt.X('change:Q', title='Increase in Rent-to-Income',  axis = alt.Axis(format = '%')),
        y=alt.Y('communityDistrict:N', sort='-x', title='District'),
        color = alt.Color("recovery_group:N", scale = alt.Scale(domain = ['Strong Recovery', 'Weak Recovery', 'Other'], range = ['blue', 'red', 'gray']), legend = alt.Legend(title = 'Recovery Group')),
        tooltip=[alt.Tooltip('communityDistrict'), alt.Tooltip('change:Q', title = '% Change in Rent Burden', format='.1%')]
        ).properties(width=650, height=500, title='Top 10 Districts Where Affordability Worsened Most')

    full_chart = (scatter | bars)
    full_chart 

    return full_chart


def ranked_bar(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame) -> alt.Chart:

    df = rental_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df['year'] = df['date'].dt.year

    mapping = streeteasy_data[['neighborhood', 'borough', 'communityDistrict']].drop_duplicates()
    df = df.merge(mapping, on = ['neighborhood', 'borough'], how = 'left')

    df = df[df['medianAskingRent'] > 0]

    rents = df.groupby(['communityDistrict','year'])['medianAskingRent'].median().reset_index()

    rents = rents[rents['year'] != 2020]
    rents = rents[rents['year'] != 2021]
    
    rent_pivot = rents.pivot(index = 'communityDistrict', columns = 'year', values = 'medianAskingRent').reset_index()
    rent_pivot.rename(columns = {2019 : 'base_year'}, inplace = True)
    rent_pivot.rename(columns = {2022 : 'final_year'}, inplace = True)
    
    rent_pivot['metric'] = rent_pivot['final_year']/rent_pivot['base_year']
    
    rent_pivot = rent_pivot.dropna()
    
    rent_pivot = rent_pivot.sort_values('metric', ascending= False)
    
    top5 = rent_pivot.head(5).copy()
    bottom5 = rent_pivot.tail(5).copy()
    
    top5['group'] = 'Top Recovery'
    bottom5['group'] = 'Weakest Recovery'
    
    combined = pd.concat([top5,bottom5])
    
    chart = alt.Chart(combined).mark_bar().encode(
        x = alt.X('metric:Q', title = '2022 Rent Relative to 2019', axis = alt.Axis(format = '.2f')),
        y = alt.Y('communityDistrict:N', sort = '-x', title = 'Community District'),
        color = alt.Color('group:N', scale = alt.Scale(domain = ['Top Recovery', 'Weakest Recovery'], range = ['blue', 'red']), legend = alt.Legend(title = 'Recovery Group')),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip('metric:Q', title = 'Recovery Ratio')]
        ).properties(width = 650, height = 500)
    
    return chart