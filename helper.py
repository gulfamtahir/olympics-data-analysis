import numpy as np

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years,countries


def fetch_medal_tally(df, year, country):

    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:

        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    # nations_over_time.rename(columns={'index': 'Edition', 'Year': 'no_of_countries'}, inplace=True)
    # remove duplicates region and years and put the value counts to get the number
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])[['Name', 'Sport', 'region']]

    if sport != 'Overall':
        temp_df = temp_df.groupby('Name').value_counts().sort_values(ascending=False).reset_index()
        temp_df.rename(columns={
            'count': "Medal",
            'region': 'Region'

        }, inplace=True)
        temp_df = temp_df[['Name', 'Medal', 'Sport', 'Region']]
        return temp_df[temp_df['Sport'] == sport].head(15)
    if sport == 'Overall':
        temp_df = temp_df.groupby('Name').value_counts().sort_values(ascending=False).reset_index()

        temp_df.rename(columns={
            'count': 'Medal',
            'region': 'Region'

        }, inplace=True)


        temp_df = temp_df[['Name', 'Medal', 'Sport', 'Region']]

        return temp_df[temp_df['Medal'] > 5]

def country_wise_each_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'Year', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    region_data = temp_df.groupby('region')[['Year', 'Medal']].value_counts().reset_index()
    region_wise = region_data[region_data['region'] == country].sort_values('Year')
    return region_wise
    # region_wise.rename(columns={
    #     'count': 'Counts'
    # }, inplace=True)
    # country_final_df = region_wise.groupby('Year').sum()['Counts'].reset_index()
    # return country_final_df

def country_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'Year', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    region_data = temp_df.groupby('region')[['Year', 'Medal']].value_counts().reset_index()
    region_wise = region_data[region_data['region'] == country].sort_values('Year')
    region_wise.rename(columns={
        'count': 'Counts'
    }, inplace=True)
    country_final_df = region_wise.groupby('Year').sum()['Counts'].reset_index()
    return country_final_df

def country_wise_medal_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'Year', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    country_heatmap = temp_df[temp_df['region'] == country]
    return country_heatmap

def most_successful_athlete_country_wise(df,country):
    temp_df = df.dropna(subset=['Medal'])[['Name', 'Sport', 'region', 'Year', 'Medal']].reset_index()
    temp_df = temp_df[temp_df['region'] == country]
    athlete_country_wise = temp_df.groupby(['Name', 'Sport'])['Medal'].count().sort_values(ascending=False).head(10).reset_index()
    return athlete_country_wise




