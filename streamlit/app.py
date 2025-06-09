import streamlit as st
import pandas as pd
import altair as alt
from utils.db import get_engine
from calendar import month_name

st.set_page_config(layout="wide", page_title="Spotify Dashboard")

# --- Apply custom CSS for dark theme and Spotify styling ---
st.markdown("""
    <style>
        body {
            background-color: #191414;
            color: white;
        }
        .stApp {
            background-color: #191414;
        }
        h1, h2, h3, h4, h5 {
            color: #1DB954;
        }
        .css-18e3th9 {
            background-color: #191414;
        }
        .stSelectbox > div, .stMultiSelect > div {
            background-color: #121212;
            color: white;
        }
        .kpi-box {
            background-color: #121212;
            border: 1px solid #1DB954;
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            color: white;
            font-family: sans-serif;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Spotify header ---
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" width="40"/>
        <h1 style="color: #1DB954;">Spotify Listening History Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

engine = get_engine()

# --- Load filters ---
@st.cache_data
def load_filters():
    df = pd.read_sql("SELECT DISTINCT year, month FROM kpi_summary", engine)
    df["month_name"] = df["month"].apply(lambda x: month_name[x])
    return df["year"].sort_values().unique(), df["month"].unique(), df["month_name"].unique(), df

years, months, month_names, filter_df = load_filters()

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox("Year", years)
selected_month_names = st.sidebar.multiselect("Month", month_names, default=list(month_names))
selected_months = filter_df[filter_df["month_name"].isin(selected_month_names)]["month"].unique()

if selected_months.size > 0:
    month_clause = ", ".join(str(m) for m in selected_months)
    filter_clause = f"WHERE year = {selected_year} AND month IN ({month_clause})"
else:
    filter_clause = f"WHERE year = {selected_year}"

# --- KPIs ---
kpi_query = f"SELECT * FROM kpi_summary {filter_clause}"
kpi = pd.read_sql(kpi_query, engine)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-box">
        <div>Songs Played</div>
        <div style="font-size: 28px; font-weight: bold;">{kpi['total_songs_played'].sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-box">
        <div>Play Time (hrs)</div>
        <div style="font-size: 28px; font-weight: bold;">{kpi['total_play_time_hours'].sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-box">
        <div>Albums</div>
        <div style="font-size: 28px; font-weight: bold;">{kpi['total_albums'].sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-box">
        <div>Artists</div>
        <div style="font-size: 28px; font-weight: bold;">{kpi['total_artists'].sum()}</div>
    </div>
    """, unsafe_allow_html=True)

# --- Top 5 Artists Table ---
st.subheader("Top 5 Artists")
query = f"SELECT * FROM artist_top_plays {filter_clause} ORDER BY song_play_count DESC LIMIT 5"
df_artists = pd.read_sql(query, engine)

# Display only valid columns
display_columns = {
    "artist_name": "Artist Name",
    "song_play_count": "Play Count",
    "total_play_time_minutes": "Play Time (minutes)"
}
available_cols = [col for col in display_columns.keys() if col in df_artists.columns]
st.dataframe(df_artists[available_cols].rename(columns=display_columns), use_container_width=True, hide_index=True)

# --- Play Time by Part of Day ---
col5, col6 = st.columns(2)

with col5:
    st.subheader("Play Time by Part of Day")
    tod_query = f"SELECT time_of_day, SUM(total_play_time_minutes) as play_time FROM time_of_day_summary {filter_clause} GROUP BY time_of_day"
    df_tod = pd.read_sql(tod_query, engine)

    bar_chart = alt.Chart(df_tod).mark_bar(color="#1DB954").encode(
        x=alt.X("time_of_day:N", title="Time of Day", sort=['morning', 'afternoon', 'evening', 'night']),
        y=alt.Y("play_time:Q", title="Play Time (minutes)")
    ).properties(
        width=500,
        height=350
    ).configure_axis(
        labelColor='white',
        titleColor='white'
    )
    st.altair_chart(bar_chart, use_container_width=True)

# --- Top 5 Songs Table with Album Art ---
with col6:
    st.subheader("Top 5 Songs")
    songs_query = f"SELECT track_name, artist_name, play_count, album_artwork_url FROM top_songs {filter_clause} ORDER BY play_count DESC LIMIT 5"
    df_songs = pd.read_sql(songs_query, engine)

    for _, row in df_songs.iterrows():
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <img src="{row['album_artwork_url']}" width="60" style="border-radius: 4px; margin-right: 10px;"/>
            <div>
                <strong>{row['track_name']}</strong><br>
                <span style="color: #AAAAAA;">{row['artist_name']} — {row['play_count']} plays</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Monthly Listening Trends (Altair Line Chart) ---
st.subheader("Monthly Listening Trends")
trend_query = f"SELECT play_month, SUM(play_count) as play_count FROM monthly_listening_trends WHERE year = {selected_year} GROUP BY play_month"
df_trend = pd.read_sql(trend_query, engine)
df_trend["play_month"] = pd.to_datetime(df_trend["play_month"])

line_chart = alt.Chart(df_trend).mark_line(color="#1DB954", point=alt.OverlayMarkDef(color="white")).encode(
    x=alt.X("play_month:T", title="Month"),
    y=alt.Y("play_count:Q", title="Songs Played")
).properties(
    width=1000,
    height=400
).configure_axis(
    labelColor='white',
    titleColor='white'
)
st.altair_chart(line_chart, use_container_width=True)
