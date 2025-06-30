import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
st.set_page_config(page_title="Adidas US Sales Dashboard", layout="wide")
st.title("📊 Adidas US Sales Data Dashboard")

# 데이터 불러오기
data = pd.read_csv("https://raw.githubusercontent.com/myoh0623/dataset/refs/heads/main/adidas_us_sales_datasets.csv")

# 컬럼 정리 및 타입 변환
data.columns = data.columns.str.strip()
for col in ["Price per Unit", "Total Sales", "Operating Profit"]:
    data[col] = data[col].replace('[\$,]', '', regex=True).astype(float)
data["Units Sold"] = data["Units Sold"].replace('[,]', '', regex=True).astype(int)
data["Operating Margin"] = data["Operating Margin"].replace('[\%,]', '', regex=True).astype(float)
data["Invoice Date"] = pd.to_datetime(data["Invoice Date"], errors="coerce")
data = data.dropna(subset=["Invoice Date"])

#  파생 변수 생성
data["Profit Rate"] = data["Operating Margin"] * 0.01
data["Year"] = data["Invoice Date"].dt.year
data["Month"] = data["Invoice Date"].dt.month

