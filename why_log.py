import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
from scipy import stats
import seaborn as sns
# from bokeh.plotting import figure, show
# from bokeh.models import Circle, Label
# from bokeh.models import HoverTool, ColumnDataSource



st.set_page_config(
    page_title = "log",
    page_icon = ":bar_chart:",
    layout = "wide"
)

st.title("Log Transformation")

@st.cache_data   # Streamlit 会自动检查函数的输入参数是否发生变化，如果没有变化，它会直接返回缓存的结果，而不会重新执行函数的计算过程。
def load_csv(file):
    return pd.read_csv(file)

df = (load_csv("China_GDP.csv")
            .rename(columns={'Unnamed: 0':'year', "Guangxi,":"Guangxi"})
            .assign(
                China = lambda df: df.iloc[:,1:].sum(axis = 1)
            )    
)

location = df.columns.tolist()[1:]
value_log = np.log(df.iloc[:,1:])
value_log.columns = [i+'_log' for i in location]
df = pd.concat([df, value_log],axis = 1)
# st.dataframe(value_log, use_container_width= True)

with open("china_province.geojson", encoding='utf-8') as f:
    provinces_map = json.load(f)
    
province_dict = {
    'Beijing': '北京',
    'Tianjin': '天津',
    'Hebei': '河北',
    'Shanxi': '山西',
    'Inner Mongolia': '内蒙古自治区',
    'Liaoning': '辽宁',
    'Jilin': '吉林',
    'Heilongjiang': '黑龙江',
    'Shanghai': '上海',
    'Jiangsu': '江苏',
    'Zhejiang': '浙江',
    'Anhui': '安徽',
    'Fujian': '福建',
    'Jiangxi': '江西',
    'Shandong': '山东',
    'Henan': '河南',
    'Hubei': '湖北',
    'Hunan': '湖南',
    'Guangdong': '广东',
    'Guangxi': '广西壮族自治区',
    'Hainan': '海南',
    'Chongqing': '重庆',
    'Sichuan': '四川',
    'Guizhou': '贵州',
    'Yunnan': '云南',
    'Tibet': '西藏自治区',
    'Shaanxi': '陕西',
    'Gansu': '甘肃',
    'Qinghai': '青海',
    'Ningxia': '宁夏回族自治区',
    'Xinjiang': '新疆维吾尔自治区'
}

#1992-2020
with st.expander('show data'):
    st.dataframe(df, use_container_width = True)

    

# 创建子图，指定两个 Y 轴
def gdp_plot(pro):   
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 添加level的曲线
    fig.add_trace(go.Scatter(
        x= df['year'],
        y= df[pro],
        name= 'Level',
        mode= 'lines+markers',
        line=dict(width=4),  # 设置线条宽度
        marker=dict(size=8)  # 设置标记的大小
    ), secondary_y=False)

    # 添加log的曲线
    fig.add_trace(go.Scatter(
        x= df['year'],
        y= df[pro+'_log'],
        name= 'Log Transformed',
        mode= 'lines+markers',
        line= dict(width=3),  # 设置线条宽度
        marker= dict(size=8)  # 设置标记的大小
    ), secondary_y=True)

    # 更新图表的布局
    fig.update_layout(
        title='GDP (unit: one hundred million)',
        xaxis_title='Year',
        yaxis_title='GDP',
        yaxis2_title='log(GDP)',
        yaxis=dict(
            tickfont=dict(size=14, family='Arial, bold'),  # 修改 y 轴标签的字体大小和粗体设置
            ),
        yaxis2=dict(
            tickfont=dict(size=14, family='Arial, bold'),  # 修改 secondary_y 的 y 轴标签的字体大小和粗体设置
            ),
        xaxis=dict(
            tickfont=dict(size=14, family='Arial, bold'),  # 修改 y 轴标签的字体大小和粗体设置
            ),
        )
    st.plotly_chart(fig, use_container_width= True)
    
def gdp_log_plot(pro):
    fig = px.scatter(df, x="year", y=pro, 
            log_y=True, 
        )
    st.plotly_chart(fig, use_container_width= True)

def gdp_map_plot(y):
    # 提取省份名称和 GDP 值
    df2 = df.query(f'year == {y}').loc[:,list(province_dict.keys())]
    provinces = list(province_dict.values())
    gdps = df2.iloc[0,].to_list()
    gdps_log = df2.iloc[0,:].map(np.log).to_list()

    # 创建 choropleth 图表对象
    fig = go.Figure(
        go.Choropleth(
            geojson = provinces_map,
            featureidkey="properties.NL_NAME_1",
            locations = provinces,  # 省份名称的拼音
            z = gdps,  # 对应的 GDP 值
            zauto = True,  
            colorscale = 'viridis',  # 设置颜色的渐变色标尺
            colorbar_title = 'GDP',  # 颜色标尺标题
            marker_opacity = 0.8,
            marker_line_width = 0.8,
            showscale = True,
    ))

    # 设置图表布局和标题
    fig.update_layout(
        title_text=f'{y}年中国各省份的 GDP',
        geo = dict(
            scope = 'asia',
            # projection=dict(type='mercator'),  # 使用墨卡托投影
            center=dict(lon=105, lat=35),  
        ),
        mapbox_style="carto-darkmatter",
        mapbox_zoom=3,
    )
    
    fig2 = go.Figure(
        go.Choropleth(
            geojson = provinces_map,
            featureidkey="properties.NL_NAME_1",
            locations = provinces,  # 省份名称的拼音
            z = gdps_log,  # 对应的 GDP 值
            zauto = True,  
            colorscale = 'viridis',  # 设置颜色的渐变色标尺
            colorbar_title = 'GDP',  # 颜色标尺标题
            marker_opacity = 0.8,
            marker_line_width = 0.8,
            showscale = True,
    ))

    # 设置图表布局和标题
    fig2.update_layout(
        title_text=f'{y}年中国各省份的 GDP',
        geo = dict(
            scope = 'asia',
            # projection=dict(type='mercator'),  # 使用墨卡托投影
            center=dict(lon=105, lat=35),  
        ),
        mapbox_style="carto-darkmatter",
        mapbox_zoom=3,
    )
    st.plotly_chart(fig, use_container_width= True)
    st.plotly_chart(fig2, use_container_width= True)
    

def density_plot():
    pass
    # # 使用指数分布生成随机股票价格数据（假设价格服从右偏的分布）
    # np.random.seed(0)
    # stock_prices = np.random.lognormal(mean=100, sigma=40, size=1000)

    # # 对股票价格进行对数转换
    # log_stock_prices = np.log(stock_prices)
    # fig, ax = plt.subplots()
    # # 绘制原始数据的密度图
    # sns.distplot(stock_prices, hist=False, kde=True, label='Original')

    # # 绘制对数转换后的密度图
    # sns.distplot(log_stock_prices, hist=False, kde=True, label='Log Transformed')

    # # 设置图表标题
    # # sns.set_title('股票价格密度图')

    # st.pyplot(use_container_width= True)

    

tab1, tab2, tab3, = st.tabs(
    ["Time Series Plot", "Choropleth Maps", "Density Plot"])


with tab1:
    with st.sidebar:
        pro = st.selectbox("Select your preferred province", location, index = len(location)-1)
        on = st.toggle('Log Plot')

        
    gdp_plot(pro)
    
    if on:
        gdp_log_plot(pro)
        
with tab2:
    with st.sidebar:
        year = st.selectbox("Year", df['year'].to_list(),
                            index = 0
        ) 
    gdp_map_plot(year)
    
# with tab3:
    # density_plot()
