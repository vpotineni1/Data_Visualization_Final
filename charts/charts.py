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

    
    chart= alt.Chart(chart_data, title = 'Before the Pandemic, NYC Rental Prices and Inventory were Stable Across NYC Boroughs').mark_line().encode(
        x = alt.X('date:T', title = 'Month'),
        y = alt.Y("value:Q", scale = alt.Scale(zero = False), title = 'Index (Baseline = 1)'),
        color = alt.Color('borough:N', title = 'Borough'),
        tooltip = [alt.Tooltip('borough:N', title = 'Borough'), alt.Tooltip('date:T', title = 'Month'), alt.Tooltip('value:Q', title = 'Index', format ='.2f' )],
        opacity = alt.condition(select2, alt.value(1), alt.value(0.2)),).add_params(select, select2).transform_filter(select).properties(width = 700, height = 400)

    return chart


def post_covid_trends_chart(rental_data: pd.DataFrame) -> alt.Chart:

    chart_data = pre_covid_data_transformation(rental_data)
    chart_data = chart_data[chart_data['date'] > "2020-01-01"].copy()


    select2 = alt.selection_point(fields = ['borough'])


    options = ['price_index', 'difference_discounts', 'inventory_index']
    labels = ['Price Index', 'Difference in Discounts', 'Inventory Index']
    input_dropdown = alt.binding_radio(options=options, labels=labels , name='Metric: ')

    select = alt.selection_point(fields = ['metric'], bind = input_dropdown, value = [{'metric': 'price_index'}])

    chart_data = chart_data.melt(
        id_vars=["borough", "date"],
        value_vars=["price_index", 'difference_discounts', "inventory_index"],
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


    structural_line = (alt.Chart(chart_data,  title = 'COVID-19 Triggeed a Shrp Shock in NYC Rental Prices and Inventory').mark_line().encode(
        x=alt.X('date:T', title = 'Month'),
        y=alt.Y('value:Q', scale = alt.Scale(zero = False), title = 'Index (Baseline = 1)' ),
        color=alt.Color('borough:N'),
        tooltip = [alt.Tooltip('borough:N', title = 'Borough'), alt.Tooltip('date:T', title = 'Month'), alt.Tooltip('value:Q', title = 'Index', format ='.2f' )],
        opacity = alt.condition(select2, alt.value(1), alt.value(0.2)),).add_params(select, select2).transform_filter(select).properties(width = 700, height = 400)
    )
    
    chart = structural_line + line_covid + covid_text

    return chart


def choropleth_data_transformation(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame) -> pd.DataFrame:
    df = rental_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    mapping = streeteasy_data[['neighborhood', 'borough', 'communityDistrict']].drop_duplicates()
    df = df.merge(mapping, on = ['neighborhood', 'borough'], how = 'left')
    rentals_agg = df.groupby(['communityDistrict','date']).agg({
        "discountShare" : "mean",
        "medianAskingRent" : "median",
        "totalInventory" : "sum",}).reset_index()
    rentals_agg['year'] = rentals_agg['date'].dt.year
    rentals_agg = rentals_agg.merge(housing_data, on = 'communityDistrict', how = 'left')

    baseline_2019 = rentals_agg[rentals_agg['year'] == 2019].groupby('communityDistrict')['medianAskingRent'].mean().reset_index(name = 'rent_2019')
    lowest_2020 = rentals_agg[rentals_agg['year'] == 2020].groupby('communityDistrict')['medianAskingRent'].min().reset_index(name = 'rent_2020_low')
    rent_2022 = rentals_agg[rentals_agg['year'] == 2022].groupby('communityDistrict')['medianAskingRent'].mean().reset_index(name = 'rent_2022')
    
    disc_2019 = rentals_agg[rentals_agg['year'] == 2019].groupby('communityDistrict')['discountShare'].mean().reset_index(name = 'discount_2019')
    disc_2020 = rentals_agg[rentals_agg['year'] == 2020].groupby('communityDistrict')['discountShare'].mean().reset_index(name = 'discount_2020')
    
    viz3_summary = baseline_2019.merge(lowest_2020, on = 'communityDistrict')
    viz3_summary = viz3_summary.merge(rent_2022, on = 'communityDistrict')
    viz3_summary = viz3_summary.merge(disc_2019, on = 'communityDistrict')
    viz3_summary = viz3_summary.merge(disc_2020, on = 'communityDistrict')
    
    viz3_summary['decline_2019_2020'] = ((viz3_summary['rent_2020_low'] - viz3_summary['rent_2019']) / viz3_summary['rent_2019'])
    viz3_summary['recovery_2020_2022'] = ((viz3_summary['rent_2022'] - viz3_summary['rent_2020_low']) / viz3_summary['rent_2020_low'])
    viz3_summary['disc_change'] = ((viz3_summary['discount_2020'] - viz3_summary['discount_2019']))
    viz3_summary['communityDistrict'] = viz3_summary['communityDistrict'].astype(int)
    viz3_summary = viz3_summary.dropna(subset = ['rent_2019', 'rent_2020_low', 'rent_2022', 'discount_2019','discount_2020','decline_2019_2020', 'recovery_2020_2022', 'disc_change'])
    columns = ['rent_2019', 'rent_2020_low', 'rent_2022', 'discount_2019','discount_2020','decline_2019_2020', 'recovery_2020_2022', 'disc_change']
    viz3_summary  = viz3_summary[np.isfinite(viz3_summary[columns]).all(axis = 1)]
    viz3_summary = viz3_summary[(
        (viz3_summary['rent_2019'] > 0) & (viz3_summary['rent_2020_low'] > 0) & (viz3_summary['rent_2022'] > 0 ))]
    
    return viz3_summary


def choropleth(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, mapping_data:pd.DataFrame ) -> alt.Chart:

    chart_data = choropleth_data_transformation(rental_data,streeteasy_data,housing_data)
    
    options = ["decline_2019_2020", "recovery_2020_2022"]
    labels = ["% Rent Decline (2019 - 2020)", "% Rent Recovery (2020 - 2022)"]
    
    input_dropdown = alt.binding_radio(options=options, labels=labels , name='Metric: ')
    select = alt.selection_point(fields = ['metric'], bind = input_dropdown, value = [{'metric': "decline_2019_2020"}])

    CD_select = alt.selection_point(fields = ['communityDistrict'])
    
    choropleth = alt.Chart(mapping_data).mark_geoshape(stroke="black",strokeWidth=0.5).transform_lookup(lookup = 'BoroCD',
                                                                                          from_ = alt.LookupData(chart_data, key = 'communityDistrict', fields = options + ['communityDistrict'])
                                                                 ).transform_fold(options, as_ = ['metric', 'value']).transform_filter(select).encode(
                                                                     color = alt.Color('value:Q', title = '% Change', scale = alt.Scale(scheme = 'redblue'), legend = alt.Legend(orient = 'left')),
                                                                     opacity = alt.condition(CD_select, alt.value(1), alt.value(0.2)),
                                                                     tooltip = [alt.Tooltip("BoroCD:N", title = 'District'), alt.Tooltip("metric:N", title = "Metric"), alt.Tooltip("value:Q", format = ".2%", title = 'Value')]).add_params(select).project(type = 'albers').properties(width = 600, height = 600)
    
    scatter = alt.Chart(chart_data).mark_circle(size = 100).encode(
        x = alt.X('decline_2019_2020:Q', title = "% Decline in Rent Price from 2019 - 2020", axis = alt.Axis(format = '%')),
        y = alt.Y('recovery_2020_2022:Q', title = '% Rent Recovery from 2020 - 2022', axis = alt.Axis(format = '%')),
        color = alt.condition(CD_select, alt.value("red"), alt.value("lightgray")),
            tooltip = alt.Tooltip('communityDistrict:N')).add_params(CD_select).properties(width = 400, height = 400)
    
    chart = (choropleth | scatter).properties(title =  alt.TitleParams(text = "Rent Declines and Recoveries Varied Widely Across NYC Community Districts", anchor = 'middle'))

    return chart


def scatter_poverty(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, poverty_data:pd.DataFrame) -> alt.Chart:
    df4= poverty_data.copy()
    df4['poverty_rate'] = pd.to_numeric(df4['poverty_rate'], errors='coerce')

    chart_data = choropleth_data_transformation(rental_data,streeteasy_data,housing_data)
    
    chart_data = chart_data.merge(df4, on = 'communityDistrict', how = 'inner')

    poverty_median = chart_data["poverty_rate"].median()
    recovery_median = chart_data["recovery_2020_2022"].median() 

    chart1 = alt.Chart(chart_data).mark_circle(size = 80).encode(
        x = alt.X("poverty_rate:Q", title = "Poverty Rate (%)", axis = alt.Axis(format = '%')),
        y = alt.Y("recovery_2020_2022:Q", title = '% Rent Recovery from 2020 - 2022', axis = alt.Axis(format = '%')),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip("poverty_rate:Q", format=".1%", title = 'Poverty Rate'), alt.Tooltip("recovery_2020_2022:Q", format=".2%", title = '% Rent Recovery')]
        ).properties(height = 400, width = 400)
    
    line = chart1.transform_regression("poverty_rate", "recovery_2020_2022").mark_line()
    
    chart2 = alt.Chart(chart_data).mark_circle(size = 80).encode(
        x = alt.X("poverty_rate:Q", title = "Poverty Rate (%)", axis = alt.Axis(format = '%')),
        y = alt.Y("recovery_2020_2022:Q", title = '% Rent Recovery from 2020 - 2022', axis = alt.Axis(format = '%')),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip("poverty_rate:Q", format=".1%", title = 'Poverty Rate'), alt.Tooltip("recovery_2020_2022:Q", format=".2%", title = '% Rent Recovery')]
        ).properties(height = 400, width = 400)

    
    xline = alt.Chart(pd.DataFrame({"y":[recovery_median]})).mark_rule().encode(y="y:Q")
    yline = alt.Chart(pd.DataFrame({"x":[poverty_median]})).mark_rule().encode(x="x:Q")

    chart1_final = chart1 + line

    chart2_final = chart2 + xline + yline

    chart_final = (chart1_final | chart2_final).properties(title =  alt.TitleParams(text = "Districs with Higher Poverty Rates Saw Weaker Rent Recovery after COVID, which is Made Clear in the Quadrant Plot", anchor = 'middle'))
    
    return chart_final



def choropleth_mapping(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, mapping_data:pd.DataFrame) -> alt.Chart:

    chart_data = choropleth_data_transformation(rental_data,streeteasy_data,housing_data)
    choropleth_data = chart_data.copy()
    choropleth_data = choropleth_data.merge(housing_data, on = "communityDistrict")

    CD_select = alt.selection_point(fields = ['communityDistrict'])
    
    
    choropleth = alt.Chart(mapping_data).mark_geoshape(stroke="black",strokeWidth=0.5
            ).transform_lookup(lookup = 'BoroCD', from_ = alt.LookupData(housing_data, key = 'communityDistrict', fields = ['completion_rate', 'communityDistrict'])
            ).encode(
                color = alt.Color('completion_rate:Q', title = 'Housing Completion Rate', legend = alt.Legend(orient = 'left')),
                opacity = alt.condition(CD_select, alt.value(1), alt.value(0.3)),
                tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip('completion_rate:Q', format = '.2%', title = 'Completion Rate' )]
            ).project(type = 'albers').add_params(CD_select)
    
    scatter = alt.Chart(choropleth_data).mark_circle(size = 80).encode(
        x = alt.X("completion_rate:Q", title = '% Housing Completion Rate (2020 - 2022)',  axis = alt.Axis(format = '%')),
        y = alt.Y("recovery_2020_2022", title = '% Rental Recovery (2020 - 2022)',  axis = alt.Axis(format = '%')),
        color = alt.condition(CD_select, alt.value("red"), alt.value("lightgray")),
        tooltip = [alt.Tooltip('communityDistrict:N', title = 'District'), alt.Tooltip("completion_rate:Q", format=".1%", title = 'Completion Rate'), alt.Tooltip("recovery_2020_2022:Q", format=".2%", title = '% Rent Recovery')]
        ).add_params(CD_select).properties(width = 400, height = 400)
    
    chart = (choropleth | scatter).properties(title =  alt.TitleParams(text = "Neighborhoods with Less New Housing Often Saw Weaker Rent Recovery ", anchor = 'middle'))
    chart
    


def rent_burden_transformation(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, income_data:pd.DataFrame) -> pd.DataFrame:

    df = rental_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    mapping = streeteasy_data[['neighborhood', 'borough', 'communityDistrict']].drop_duplicates()

    df = df.merge(mapping, on = ['neighborhood', 'borough'], how = 'left')

    rentals_agg = df.groupby(['communityDistrict','date']).agg({
        "discountShare" : "mean",
        "medianAskingRent" : "median",
        "totalInventory" : "sum",}).reset_index()
    rentals_agg['year'] = rentals_agg['date'].dt.year
    rentals_agg = rentals_agg.merge(housing_data, on = 'communityDistrict', how = 'left')

    rent_year = rentals_agg.groupby(['communityDistrict', 'year'])['medianAskingRent'].mean().reset_index()

    rent_2019 = rent_year[(rent_year['year'] == 2019)]
    rent_2019 = rent_2019[rent_2019['medianAskingRent'] != 0.0]

    rent_2022 = rent_year[(rent_year['year'] == 2022)]
    rent_2022= rent_2022[rent_2022['medianAskingRent'] != 0.0]  

    median_rent_2019 = income_data.copy()

    income_rent_2019 = rent_2019.merge(median_rent_2019, on = 'communityDistrict', how = 'inner')
    income_rent_2022 = rent_2022.merge(median_rent_2019, on = 'communityDistrict', how = 'inner') 

    income_rent_2019['ratio_2019'] = (income_rent_2019['medianAskingRent'] * 12) / income_rent_2019['Median_Household_Income']
    income_rent_2022['ratio_2022'] = (income_rent_2022['medianAskingRent'] * 12) / income_rent_2022['Median_Household_Income']
    income_rent = income_rent_2019.merge(income_rent_2022, on = 'communityDistrict', how = 'inner')
    income_rent['change'] = income_rent['ratio_2022'] - income_rent['ratio_2019']  

    return income_rent
    

def rent_burden_visualization(rental_data: pd.DataFrame, streeteasy_data: pd.DataFrame, housing_data:pd.DataFrame, income_data:pd.DataFrame) -> alt.Chart:

    income_rent = rent_burden_transformation(rental_data, streeteasy_data, housing_data, income_data)

    top10 = income_rent.sort_values('change', ascending=False).head(10)
    filter_out = ~income_rent['communityDistrict'].isin(top10['communityDistrict'].tolist())
    outside_10 = income_rent[filter_out]

    base_scatter = alt.Chart(outside_10).mark_circle(size = 80).encode(
        x = alt.X('Median_Household_Income_x:Q', title='Median Household Income $ (Baseline: 2019)'),
        y= alt.Y('change:Q', title='Change in Rent-to-Income Ratio (2022 - 2019)', axis = alt.Axis(format = '%')),
        tooltip=[alt.Tooltip('communityDistrict:N', title='District')], 
        color = alt.value('lightgrey'))

    scatter = alt.Chart(income_rent).mark_circle(size=80).encode(
         x=alt.X('medianAskingRent_x:Q', title='Median Household Income (baseline)'),
        y=alt.Y('change:Q', title='Change in Rent-to-Income Ratio (2022 – 2019)'),
        tooltip=[alt.Tooltip('communityDistrict:N', title='District'),]).properties(width=700, height=450, title='Affordability Change vs Income by District')
    
    bar_points = alt.Chart(top10).mark_circle(size = 200).encode(
        x = alt.X('Median_Household_Income_x:Q', title='Median Household Income $ (Baseline: 2019)'),
        y= alt.Y('change:Q', title='Change in Rent-to-Income Ratio (2022 - 2019)', axis = alt.Axis(format = '%')),
        tooltip=[alt.Tooltip('communityDistrict:N', title='District')], 
        color = alt.value('red'))
    
    trend = alt.Chart(income_rent).transform_regression('Median_Household_Income_x', 'change').mark_line().encode(
        x = 'Median_Household_Income_x:Q',
        y = 'change:Q')
    
    scatter = (base_scatter + bar_points + trend).properties(width = 500, height = 500)
    
    
    bars = alt.Chart(top10).mark_bar().encode(
        x=alt.X('change:Q', title='Increase in Rent-to-Income',  axis = alt.Axis(format = '%')),
        y=alt.Y('communityDistrict:N', sort='-x', title='District'),
        tooltip=['communityDistrict', alt.Tooltip('change:Q', format='.1%')]
        ).properties(width=650, height=500, title='Top 10 Districts Where Affordability Worsened Most')

    full_chart = (scatter | bars).properties(title =  alt.TitleParams(text = "Neighborhoods with a Lower Median Income often had a Smaller Change in Rent Burden Ratio ", anchor = 'middle'))
    full_chart 

    return full_chart