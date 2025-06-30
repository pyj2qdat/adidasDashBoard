# 1. 라이브러리 임포트 및 기본 설정
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
st.set_page_config(page_title="Adidas US Sales Dashboard", layout="wide")
st.title("📊 Adidas US Sales Data Dashboard")


# 2. 데이터 불러오기 및 전처리

data = pd.read_csv("https://raw.githubusercontent.com/myoh0623/dataset/refs/heads/main/adidas_us_sales_datasets.csv")

data.columns = data.columns.str.strip()
for col in ["Price per Unit", "Total Sales", "Operating Profit"]:
    data[col] = data[col].replace('[\$,]', '', regex=True).astype(float)
data["Units Sold"] = data["Units Sold"].replace('[,]', '', regex=True).astype(int)
data["Operating Margin"] = data["Operating Margin"].replace('[\%,]', '', regex=True).astype(float)
data["Invoice Date"] = pd.to_datetime(data["Invoice Date"], errors="coerce")
data = data.dropna(subset=["Invoice Date"])

# 파생 변수 생성
data["Profit Rate"] = data["Operating Margin"] * 0.01
data["Year"] = data["Invoice Date"].dt.year
data["Month"] = data["Invoice Date"].dt.month

# 사이드바 필터 구현
st.sidebar.header("Filter Options")
region = st.sidebar.multiselect("Region", options=sorted(data["Region"].dropna().unique()), default=list(data["Region"].dropna().unique()))
retailer = st.sidebar.multiselect("Retailer", options=sorted(data["Retailer"].dropna().unique()), default=list(data["Retailer"].dropna().unique()))
product = st.sidebar.multiselect("Product", options=sorted(data["Product"].dropna().unique()), default=list(data["Product"].dropna().unique()))
sales_method = st.sidebar.multiselect("Sales Method", options=sorted(data["Sales Method"].dropna().unique()), default=list(data["Sales Method"].dropna().unique()))

filtered = data[
    data["Region"].isin(region) &
    data["Retailer"].isin(retailer) &
    data["Product"].isin(product) &
    data["Sales Method"].isin(sales_method)
]

# 주요 지표 요약 표시
st.markdown("## 📈 주요 지표")
k1, k2, k3, k4 = st.columns(4)
k1.metric("총 매출액 ($)", f"{filtered['Total Sales'].sum():,.0f}")
k2.metric("총 판매수량", f"{filtered['Units Sold'].sum():,}")
k3.metric("평균 단가 ($)", f"{filtered['Price per Unit'].mean():.2f}")
k4.metric("평균 마진율 (%)", f"{filtered['Operating Margin'].mean():.2f}")

# 탭 레이아웃 구성
tat1, tab2, tab3 = st.tabs(["트렌드 및 분포","소매점/제품","심화 분석"])

# 트렌드 및 분포 시각화