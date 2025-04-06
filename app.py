import streamlit as st
import pandas as pd
import plotly.express as px

# 设置页面基础信息
st.set_page_config(page_title="Nutrition Goal Classifier", layout="wide")

# 侧边栏导航
page = st.sidebar.selectbox("Choose a page", ["Landing Page", "Interactive Visualization"])


# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("food.csv")
    return df


df = load_data()

# 定义分类阈值
low_cal = df["Data.Kilocalories"].quantile(0.33)
high_cal = df["Data.Kilocalories"].quantile(0.67)
low_fat = df["Data.Fat.Total Lipid"].quantile(0.33)
high_protein = df["Data.Protein"].quantile(0.67)
mid_fat = df["Data.Fat.Total Lipid"].quantile(0.67)


# 健康目标分类函数
def classify_health_goal(row):
    if row["Data.Kilocalories"] <= low_cal and row["Data.Protein"] >= high_protein and row[
        "Data.Fat.Total Lipid"] <= mid_fat:
        return "Fat Loss (Preserve Muscle)"
    elif row["Data.Kilocalories"] >= high_cal and row["Data.Protein"] >= high_protein:
        return "Weight Gain (Muscle Focus)"
    elif row["Data.Kilocalories"] <= low_cal and row["Data.Fat.Total Lipid"] <= low_fat:
        return "Dieting"
    else:
        return "General Health"


# 应用分类函数
df["HealthGoal"] = df.apply(classify_health_goal, axis=1)

# Landing Page
if page == "Landing Page":
    st.title("Personalized Nutrition Recommender")

    st.subheader("DS4420 Final Project")
    st.markdown("""
    **Team Members**: Eric Wu, Gregory Zeng, Yinzheng Xiong  
    **Date**: April 3, 2025  

    ---

    **Project Overview**

    In this project, we aim to build a smart food recommendation system based on nutritional content.  
    The goal is to help users quickly identify which foods align with their personal **health goals**, such as:

    - Weight Gain (Muscle Focus)  
    - Fat Loss (Preserve Muscle)  
    - Dieting (Low Calories & Low Fat)  
    - General Health

    We implemented and compared two models:

    - **Method 1**: Multi-Layer Perceptron (Python)
    - **Method 2**: Naive Bayes Classifier (R)

    ---

    **Why does this matter?**  
    Manually analyzing nutrition labels is confusing and time-consuming.  
    Our models automate the process, making it faster and more personalized.

    Use the tab on the left to explore an **interactive visualization** of our results!
    """)

# Interactive Plot Page
elif page == "Interactive Visualization":
    st.title("Calories vs Protein: Interactive Visualization")

    # 清洗数据
    plot_df = df[['Data.Kilocalories', 'Data.Protein', 'HealthGoal', 'Description']].dropna()

    # 创建 Plotly 图
    fig = px.scatter(
        plot_df,
        x='Data.Kilocalories',
        y='Data.Protein',
        color='HealthGoal',
        hover_data=['Description'],
        title='Calories vs Protein by Health Goal',
        labels={'Data.Kilocalories': 'Calories', 'Data.Protein': 'Protein (g)'},
        opacity=0.7
    )

    fig.update_layout(
        width=1000,
        height=700,
        font=dict(size=14),
        legend_title_text='Health Goal'
    )

    st.plotly_chart(fig, use_container_width=True)
