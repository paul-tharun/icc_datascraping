import streamlit as st
import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import altair as alt

DATABASE = {
    "drivername": "postgresql",
    "host": "localhost",
    "port": 5432,
    "username": "",
    "password": "",
    "database": "",
}

st.title("Data Visualization Dashboard based on ICC ODI Ratings")
st.sidebar.title("Data Visualization Dashboard by ICC ODI Ratings")

st.sidebar.subheader("Explore the dashboard by")
explore_type = st.sidebar.radio("", ("By Nationality", "By Player"))
player_type = st.sidebar.radio(
    "Select Player Type", ("Batsmen", "Bowlers", "All-Rounders")
)

st.markdown(" ")
st.sidebar.markdown("")


@st.cache(persist=True)
def load_data(type):
    alchemyEngine = create_engine(URL(**DATABASE))
    dbConnection = alchemyEngine.connect()
    data = pd.read_sql(
        'select * from "playersData"', dbConnection, parse_dates=["date"]
    )
    dbConnection.close()
    data = data.drop(columns="id")
    types = {"Batsmen": "batting", "Bowlers": "bowling", "All-Rounders": "all-rounder"}
    data = data[data.type == types[type]]
    return data


def plot_indi_players(data, day, num=10):
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d")
    df = data[data.date == day].sort_values(by=["rating"], ascending=False).head(num)
    bars = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="rating:Q",
            y=alt.Y(
                "name:N",
                sort=alt.EncodingSortField("rating", op="min", order="descending"),
            ),
            tooltip=["name", "rating", "country"],
            color="country",
        )
    )
    text = (
        alt.Chart(df)
        .mark_text(align="left", baseline="middle", dx=2)
        .encode(
            x="rating:Q",
            y=alt.Y(
                "name:N",
                sort=alt.EncodingSortField("rating", op="min", order="descending"),
            ),
            text="rating:Q",
        )
    )
    plot = (bars + text).properties(
        height=500, width=650, title="Top {} {} on {}".format(num, player_type, day)
    )
    return plot


def plot_nations(data, day):
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d")
    df = data[data.date == day].sort_values(by=["rating"], ascending=False).head(20)
    df = df.groupby(by="country").size()
    return df


data = load_data(player_type)

if explore_type == "By Player":
    st.markdown("## Top 10 players on a day")
    day = st.date_input(
        "Select the Date", min_value=min(data["date"]), max_value=max(data["date"])
    )
    st.altair_chart(plot_indi_players(data, day))
    st.markdown("## Change in top 10 players over time")
    start_day = st.date_input(
        "Select the Date",
        min_value=min(data["date"]),
        max_value=max(data["date"]),
        key="start_date",
    )
    end_day = st.date_input(
        "Select the Date",
        min_value=min(data["date"]),
        max_value=max(data["date"]),
        key="end_date",
    )
    delta = datetime.timedelta(days=1)

    chart = st.empty()
    if st.button("Run time graph"):
        while start_day <= end_day:
            bar_data = plot_indi_players(data, start_day)
            time.sleep(0.5)
            chart.altair_chart(bar_data)
            start_day += delta

if explore_type == "By Nationality":
    st.markdown("## Number of Players in Top 20 for each nation over time")
    start_date = st.date_input(
        "Select the Date",
        min_value=min(data["date"]),
        max_value=max(data["date"]),
        key="start_nation",
    )
    end_date = st.date_input(
        "Select the Date",
        min_value=min(data["date"]),
        max_value=max(data["date"]),
        key="end_nation",
    )
    delta = datetime.timedelta(days=1)
    chart = st.empty()
    if st.button("Run time graph"):
        while start_date <= end_date:
            bar_data = plot_nations(data, start_date)
            time.sleep(0.5)
            chart.bar_chart(bar_data)
            start_date += delta
