import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.sidebar.image("GMD.png")

# Function to plot charts based on the selected chart type
def plot_chart(data, y_column, title, chart_type):
    fig = go.Figure()

    for year in data['Year'].unique():
        year_df = data[data['Year'] == year]

        if chart_type in ["Bar", "Both"]:
            fig.add_trace(go.Bar(x=year_df['Month'], y=year_df[y_column], name=f'Bar - {y_column} ({year})'))

        if chart_type in ["Line", "Both"]:
            fig.add_trace(go.Scatter(x=year_df['Month'], y=year_df[y_column], mode='lines+markers', name=f'Line - {y_column} ({year})'))

    fig.update_layout(title=title, xaxis_title='Month', yaxis_title=y_column)
    return fig

def product_page(df):
    st.header("產品 Page")

    # Select 客戶需求日期
    date_range = st.sidebar.date_input("Select 客戶需求日期", [])

    # Select 項目名稱
    item_name = st.sidebar.selectbox("Select 項目名稱 (first 3 chars as catalog)", df["項目名稱"].str[:3].unique())

    # Select Chart Type
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Line", "Bar", "Both"])

    # Filter based on the selected date range and item name
    filtered_df = df.copy()
    if date_range:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[(filtered_df["客戶需求日期"] >= start_date) & (filtered_df["客戶需求日期"] <= end_date)]
    filtered_df = filtered_df[filtered_df["項目名稱"].str.startswith(item_name)]

    # Group by Year and Month for each metric
    filtered_df['Year'] = filtered_df['客戶需求日期'].dt.year
    filtered_df['Month'] = filtered_df['客戶需求日期'].dt.month

    # Sum the data by Year and Month
    grouped_df = filtered_df.groupby(['Year', 'Month']).agg({
        '原始訂單數': 'sum',
        '已交數': 'sum'
    }).reset_index()

    # Calculate 最終交貨率
    grouped_df['最終交貨率 %'] = (grouped_df['已交數'] / grouped_df['原始訂單數'])*100

    # Display the combined data in a table with the selected 項目名稱 in the title
    st.subheader(f"[{item_name}] 原始資料")
    st.dataframe(grouped_df)

    # Create tabs for charts with the selected 項目名稱 in the titles
    tab1, tab2, tab3 = st.tabs([
        f"[{item_name}] 原始訂單數趨勢圖",
        f"[{item_name}] 已交數趨勢圖",
        f"[{item_name}] 最終交貨率趨勢圖 %"
    ])

    # Plot the charts in the respective tabs
    with tab1:
        st.plotly_chart(plot_chart(grouped_df, '原始訂單數', f"[{item_name}] 原始訂單數趨勢圖", chart_type))

    with tab2:
        st.plotly_chart(plot_chart(grouped_df, '已交數', f"[{item_name}] 已交數趨勢圖", chart_type))

    with tab3:
        st.plotly_chart(plot_chart(grouped_df, '最終交貨率 %', f"[{item_name}] 最終交貨率趨勢圖 %", chart_type))

def dealer_page(df):
    st.header("經銷商 Page")

    # Select 客戶需求日期
    date_range = st.sidebar.date_input("Select 客戶需求日期", [])

    # Get all unique dealers from the dataframe
    all_dealers = df['客戶名稱'].unique().tolist()

    # Define the top 10 dealers
    dealers = [
        "一中商業有限公司", "世淯企業有限公司", "升鑫交通器材有限公司", "嘉晨企業社", "嘉航車業",
        "安都實業股份有限公司", "明杰輪業", "明陽實業股份有限公司", "聯有企業行", "雷士國際企業社"
    ]

    # Create options for the first selectbox, including "Other"
    dealer_options = dealers + ["Other"]

    # First selectbox for top 10 dealers or "Other"
    selected_dealer_option = st.sidebar.selectbox("Select 客戶名稱", dealer_options)

    # If "Other" is selected, show a second selectbox for other dealers
    if selected_dealer_option == "Other":
        # Get dealers not in the top 10, sorted for better usability
        other_dealers = sorted([dealer for dealer in all_dealers if dealer not in dealers])
        final_customer_name = st.sidebar.selectbox("Select 其他客戶名稱", other_dealers)
    else:
        # If a top 10 dealer is selected, use it directly
        final_customer_name = selected_dealer_option

    # Select Chart Type
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Line", "Bar", "Both"])

    # Filter based on the selected date range and final customer name
    filtered_df = df.copy()
    if date_range and len(date_range) == 2:  # Ensure two dates are selected
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[(filtered_df["客戶需求日期"] >= start_date) &
                                 (filtered_df["客戶需求日期"] <= end_date)]
    filtered_df = filtered_df[filtered_df["客戶名稱"] == final_customer_name]

    # Group by Year and Month for each metric
    filtered_df['Year'] = filtered_df['客戶需求日期'].dt.year
    filtered_df['Month'] = filtered_df['客戶需求日期'].dt.month

    # Sum the data by Year and Month
    grouped_df = filtered_df.groupby(['Year', 'Month']).agg({
        '原始訂單數': 'sum',
        '已交數': 'sum'
    }).reset_index()

    # Calculate 最終交貨率
    grouped_df['最終交貨率 %'] = (grouped_df['已交數'] / grouped_df['原始訂單數'])*100

    # Display the combined data in a table with the selected 客戶名稱 in the title
    st.subheader(f"[{final_customer_name}] 原始資料")
    st.dataframe(grouped_df)

    # Create tabs for charts with the selected 客戶名稱 in the titles
    tab1, tab2, tab3 = st.tabs([
        f"[{final_customer_name}] 原始訂單數趨勢圖",
        f"[{final_customer_name}] 已交數趨勢圖",
        f"[{final_customer_name}] 最終交貨率趨勢圖 %"
    ])

    # Plot the charts in the respective tabs
    with tab1:
        st.plotly_chart(plot_chart(grouped_df, '原始訂單數',
                                  f"[{final_customer_name}] 原始訂單數趨勢圖", chart_type))

    with tab2:
        st.plotly_chart(plot_chart(grouped_df, '已交數',
                                  f"[{final_customer_name}] 已交數趨勢圖", chart_type))

    with tab3:
        st.plotly_chart(plot_chart(grouped_df, '最終交貨率 %',
                                  f"[{final_customer_name}] 最終交貨率趨勢圖 %", chart_type))


def full_product_page(df):
    st.header("庫存&淡旺季")

    # Sidebar section selection
    section_selection = st.sidebar.radio("選擇區塊", ["庫存", "生產淡旺季", "Top 10 生產淡旺季", "Top10 庫存"])

    # Get initial date range from data
    if not df.empty:
        min_date, max_date = df["交貨日"].min(), df["交貨日"].max()
    else:
        min_date, max_date = None, None

    # Sidebar filters
    date_range = st.sidebar.date_input("選擇日期範圍", [min_date, max_date] if min_date and max_date else [])

    if date_range and len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        start_date, end_date = min_date, max_date

    if section_selection == "庫存":
        # Section 1: 庫存
        st.subheader("庫存")
        selected_customer = st.sidebar.selectbox("選擇客戶", df["客戶"].unique())
        filtered_df = df[df["客戶"] == selected_customer]

        if start_date and end_date:
            filtered_df = filtered_df[(filtered_df["交貨日"] >= start_date) & (filtered_df["交貨日"] <= end_date)]

        inventory_df = filtered_df.groupby("項目名稱", as_index=False)["A1庫存"].sum()
        inventory_df = inventory_df.sort_values(by="A1庫存", ascending=False)
        inventory_df = inventory_df[inventory_df["A1庫存"] > 0]
        # Calculate Percentage
        inventory_df["percentage"] = (inventory_df["A1庫存"] / inventory_df["A1庫存"].sum()) * 100

        # Filter out percentages lower than 1%
        inventory_df = inventory_df[inventory_df["percentage"] >= 1]
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader(f"A1庫存明細 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})")
            st.dataframe(inventory_df.drop(columns=["percentage"]))
        with col2:
            if not inventory_df.empty:
                fig = px.pie(inventory_df, names="項目名稱", values="A1庫存", title="A1庫存分佈")
                st.plotly_chart(fig)

            else:
                st.warning("沒有符合條件的資料")

    elif section_selection == "生產淡旺季":
        # Section 2: 生產淡旺季
        st.subheader("生產淡旺季")
        selected_customer = st.sidebar.selectbox("選擇客戶", df["客戶"].unique())
        filtered_df = df[df["客戶"] == selected_customer]

        if start_date and end_date:
            filtered_df = filtered_df[(filtered_df["交貨日"] >= start_date) & (filtered_df["交貨日"] <= end_date)]
        else:
            filtered_df = df.copy()

        filtered_df["Year"] = filtered_df["交貨日"].dt.year
        filtered_df["Month"] = filtered_df["交貨日"].dt.month.astype(int)  # Extract month and convert to integer

        # Aggregate by Year and Month
        seasonality_df = filtered_df.groupby(["Month", "Year"], as_index=False)["原始訂單數"].sum()

        # Ensure the dataset contains all months (fill missing months with 0)
        all_years = seasonality_df["Year"].unique()
        full_months = pd.DataFrame({"Month": list(range(1, 13))})  # Ensure 1-12 always appear

        full_data = []
        for year in all_years:
            df_year = seasonality_df[seasonality_df["Year"] == year]
            df_full = full_months.merge(df_year, on="Month", how="left").fillna({"原始訂單數": 0})
            df_full["Year"] = year  # Add Year column
            full_data.append(df_full)

        seasonality_df = pd.concat(full_data)
        seasonality_df = seasonality_df.sort_values(by=["Year", "Month"])

        st.subheader(f"生產淡旺季明細 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})")
        st.dataframe(seasonality_df, hide_index=True)

        if not seasonality_df.empty:
            fig = px.line(seasonality_df, x="Month", y="原始訂單數", color="Year",
                          title="生產淡旺季趨勢圖", markers=True, line_shape='linear')

            # Ensure the x-axis always starts from 1月 and ends at 12月
            fig.update_xaxes(type='category', tickmode='array', tickvals=list(range(1, 13)),
                             ticktext=[f"{i}月" for i in range(1, 13)])
            st.plotly_chart(fig)
        else:
            st.warning("沒有符合條件的資料")

    if section_selection == "Top 10 生產淡旺季":
        # Section 3: 生產淡旺季Top 10
        st.subheader("生產淡旺季Top 10")

        if start_date and end_date:
            filtered_df = df[(df["交貨日"] >= start_date) & (df["交貨日"] <= end_date)]
        else:
            filtered_df = df.copy()

        filtered_df["Year"] = filtered_df["交貨日"].dt.year
        filtered_df["Month"] = filtered_df["交貨日"].dt.strftime("%m")  # Extract month as string
        filtered_df["Month"] = filtered_df["Month"].astype(int)  # Convert to integer for sorting

        seasonality_top10_df = filtered_df.groupby(["Month", "Year"], as_index=False)["原始訂單數"].sum()
        seasonality_top10_df = seasonality_top10_df.sort_values(by=["Month"])

        st.subheader(f"生產淡旺季Top 10 明細 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})")
        st.dataframe(seasonality_top10_df, hide_index=True)

        if not seasonality_top10_df.empty:
            fig = px.line(seasonality_top10_df, x="Month", y="原始訂單數", color="Year",
                          title="生產淡旺季Top 10 趨勢圖", markers=True, line_shape='linear')
            fig.update_xaxes(type='category', tickmode='array', tickvals=list(range(1, 13)),
                             ticktext=[f"{i}月" for i in range(1, 13)])
            st.plotly_chart(fig)
        else:
            st.warning("沒有符合條件的資料")

    elif section_selection == "Top10 庫存":
        # Section 3: Top10 庫存
        st.subheader("Top10 庫存")

        if start_date and end_date:
            filtered_df = df[(df["交貨日"] >= start_date) & (df["交貨日"] <= end_date)]
        else:
            filtered_df = df.copy()

        inventory_df = filtered_df.groupby("項目名稱", as_index=False)["A1庫存"].sum()
        inventory_df = inventory_df.sort_values(by="A1庫存", ascending=False).head(10)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader(f" ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})")
            st.dataframe(inventory_df, hide_index=True)
        with col2:
            if not inventory_df.empty:
                fig = px.pie(inventory_df, names="項目名稱", values="A1庫存")
                st.plotly_chart(fig)
            else:
                st.warning("沒有符合條件的資料")


# Upload the data
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Load the Excel file
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        df['客戶需求日期'] = pd.to_datetime(df['客戶需求日期'])

        # Sidebar selection
        st.sidebar.header("Select Page")
        page_selection = st.sidebar.selectbox("Choose a page", ["產品", "經銷商", "庫存&淡旺季"])

        # Page routing
        if page_selection == "產品":
            product_page(df)
        elif page_selection == "經銷商":
            dealer_page(df)
        else:
            full_product_page(df)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.write("Please upload an Excel file to begin.")
