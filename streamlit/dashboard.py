# main.py
import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px


st.set_page_config(page_title="Ondoriya — Gold Layer Explorer", layout="wide")
st.title("Ondoriya — Gold Layer Explorer")


@st.cache_resource
def get_connection():
    path = st.secrets["duckdb"]["path"]  # set in .streamlit/secrets.toml
    conn = duckdb.connect(database=path, read_only=False)
    return conn


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    return conn.execute(sql).df()


st.header("Global Stats")
try:
    df_total = run_query("SELECT total_population FROM ondoriya_gold.total_population")
    if not df_total.empty:
        total = int(df_total.iloc[0, 0])
        st.metric("**Total population**", f"{total:,}")
except Exception as e:
    st.error(f"Could not load total population: {e}")

try:
    df_dom = run_query("SELECT faction, percent FROM ondoriya_gold.dominant_faction")
    if not df_dom.empty:
        st.write("**Dominant faction:**", f"{df_dom.iloc[0,0]} ({df_dom.iloc[0,1]})")
except Exception as e:
    st.error(f"Could not load dominant faction: {e}")


st.header("Dashboard Summary")
try:
    dashboard_dataframe = run_query("SELECT * FROM ondoriya_gold.dashboard_summary")

    if dashboard_dataframe.empty:
        st.warning("No data found in dashboard_summary")
    else:
        st.dataframe(dashboard_dataframe)

    # Population by region
    if (
        "region_full_name" in dashboard_dataframe.columns
        and "region_population_density" in dashboard_dataframe.columns
    ):
        st.subheader("Population by Region (All)")

        # Aggregate population by region_full_name
        aggregate_dataframe = (
            dashboard_dataframe.groupby("region_full_name", as_index=False)[
                "region_population_density"
            ]
            .sum()
            .sort_values("region_population_density", ascending=False)
        )

        fig_all = px.bar(
            aggregate_dataframe,
            x="region_full_name",
            y="region_population_density",
            text="region_population_density",
            title="Population by Region",
        )
        fig_all.update_layout(xaxis_title="Region", yaxis_title="Population")
        st.plotly_chart(fig_all)

    # Top 5 Most Populous Regions
    if (
        "region_full_name" in dashboard_dataframe.columns
        and "region_population_density" in dashboard_dataframe.columns
    ):
        st.subheader("Top 5 Most Populous Regions")

        top5 = (
            dashboard_dataframe[["region_full_name", "region_population_density"]]
            .sort_values("region_population_density", ascending=False)
            .head(5)
            .reset_index(drop=True)
        )

        top5 = aggregate_dataframe.head(5)

        top5_barchart = px.bar(
            top5,
            x="region_full_name",
            y="region_population_density",
            text="region_population_density",
            title="Top 5 Most Populous Regions",
        )
        top5_barchart.update_layout(xaxis_title="Region", yaxis_title="Population")
        st.plotly_chart(top5_barchart)

        # CSV download
        st.download_button(
            "Download dashboard summary CSV",
            dashboard_dataframe.to_csv(index=False),
            "dashboard_summary.csv",
        )

except Exception as e:
    st.error(f"Could not load dashboard summary: {e}")
