import streamlit as st
import pandas as pd
import helper
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
sns.set()

data = pd.read_csv('merge.csv')
# data.drop(columns='Unnamed:0')
medal_tally = pd.read_csv('medal_tally.csv',header=None)
medal_tally.drop(medal_tally.columns[0], axis=1, inplace=True)
# medal_tally.drop(columns='Unnamed')
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country Wise Analysis','Athlete Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years , countries = helper.country_year_list(data)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Year', countries)

    medal_tally = helper.fetch_medal_tally(data,selected_year,selected_country)

    if selected_year =='Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selected_year !='Overall' and selected_country =='Overall':
        st.title('Medal Tally in '+str(selected_year)+ ' Olympics')
    if selected_year =='Overall' and selected_country !='Overall':
        st.title('Medal Tally in '+selected_country)
    if selected_year !='Overall' and selected_country !='Overall':
        st.title('Medal Tally in '+selected_country+ ' in selected '+str(selected_year))

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
        st.title("Top Statistics")
        editions = data['Year'].unique().shape[0]-1
        cities = data['City'].unique().shape[0]-1
        sports = data['Sport'].unique().shape[0]
        events = data['Event'].unique().shape[0]
        athletes = data['Name'].unique().shape[0]
        nations = data['region'].unique().shape[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Cities")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Athletes")
            st.title(athletes)
        with col3:
            st.header("Nations")
            st.title(nations)
############################## NATIONS OVER TIME FRAME #########################

        nations_over_time = helper.data_over_time(data,'region')
        # Create the line graph
        st.title('Participating Nations over the Graph')
        fig=px.line(nations_over_time, x='Year', y='count')

        st.plotly_chart(fig)
############################## EVENTS OVER TIME FRAME #########################

        nations_over_time = helper.data_over_time(data, 'Event')
        # Create the line graph
        st.title('Events over the Graph')
        fig = px.line(nations_over_time, x='Year', y='count')
        st.plotly_chart(fig)

############################## ATHLETES OVER TIME FRAME #########################

        nations_over_time = helper.data_over_time(data, 'Name')
        # Create the line graph
        st.title('Athletes over the Graph')
        fig = px.line(nations_over_time, x='Year', y='count')
        st.plotly_chart(fig)


        # st.title('No.Of Events over Time')
        plt.figure(figsize=(20, 20))
        x= data.drop_duplicates(['Year','Sport','Event'])
        sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event', aggfunc='count').fillna(0).astype('int'), annot=True, linewidths=0.5, square=True)
        st.pyplot(plt)


        st.title("Most Successful Athletes")
        #making the filter box
        sport_list = data['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall') # by default
        selected_sport = st.selectbox('Select a Sport',sport_list)
        x= helper.most_successful(data,selected_sport)
        st.table(x)

if user_menu == 'Country Wise Analysis':
    st.sidebar.title('Country Wise Analysis')
    # making the filter box
    region_list = data['region'].dropna().unique().tolist()
    region_list.sort()
    selected_region = st.sidebar.selectbox('Select a Sport', region_list)
    ########################### LINE GRAP ###############################
    country_medal_tally = helper.country_wise_medal_tally(data,selected_region)
    st.title(f'{selected_region} Medal Tally')
    st.table(country_medal_tally)
    st.title(f'{selected_region} Medal Tally')
    fig = px.line(country_medal_tally, x='Year', y='Counts')
    st.plotly_chart(fig)

    ####################### HEAT MAP #################################
    st.title(f'{selected_region} Medal Tally Heat Map')
    country_medal_heatmap = helper.country_wise_medal_heatmap(data,selected_region)
    plt.figure(figsize=(20, 20))
    sns.heatmap(country_medal_heatmap.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True, linewidths=0.5, square=True)
    st.pyplot(plt)

    st.title(f'Top 10 Athletes of {selected_region}')
    top_ten_df = helper.most_successful_athlete_country_wise(data,selected_region)
    st.table(top_ten_df)


if user_menu == 'Athlete Wise Analysis':
    st.title('Athlete Wise Analysis')
    athletes_df = data.drop_duplicates(subset=['Name', 'region'])
    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()
    figure = ff.create_distplot([x1, x2, x3, x4],
                                ['Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                show_hist=False, show_rug=False)
    st.plotly_chart(figure)













