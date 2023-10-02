import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from bokeh.plotting import figure, show
from bokeh.models import Circle, Label
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import Arrow, NormalHead

# function setup
# 定义线性函数
def demand(x):
    return (x-a)/b
def supply(x):
    return (x-c)/d

def cob_series(price):
    q = c+d*price  # calcuate next period quantity based on supply
    cob_p = [price]
    cob_q = [q]
    cob_p_draw = [price]
    cob_q_draw = [q]
    for t in range(0, 10):
        # update price level by demand function
        price = 1/b*q - a/b
        cob_q_draw.append(q) # for drawing
        cob_p_draw.append(price)            
        # seller decide next period quanitity based p_t
        # update q by supply function
        q = c + d*price
        cob_p_draw.append(price) # for drawing
        cob_q_draw.append(q) 
        # price and quantity series 
        cob_p.append(price)
        cob_q.append(q)    
        data_cob = {
            'p': cob_p,
            'q': cob_q
        }  
        
        data_cob_draw = {
            'p': cob_p_draw,
            'q': cob_q_draw
        }  
    return data_cob, data_cob_draw
    
###########################

st.title("Coweb Model")

tab1, tab2, tab3 = st.tabs(
    ["Case 1", "Case 2", "Case 3"])

with tab1:
    st.header("Case 1: Convergent Fluctuation")
    st.write("")
    st.write("Suppose a linear Demand and Supply model is:")
    st.latex(r'''
             \begin{align*} 
             Q^d & =&  a + bP & \quad a>0, b<0\\
             Q^s & = & c + dP & \quad c<0, d>0\\
             \end{align*}
             ''')
    st.latex(r'''
              |\frac{a}{b}| > |\frac{c}{d}|, \quad |b| > d
              ''')
    st.write("")
    
    col1, col2 = st.columns(2)
    col1.write("Demand")
    a = col1.number_input('a', value = 10,  key= 11)
    b = col1.number_input('b', value = -1, key= 12)
    col2.write("Supply")
    c = col2.number_input('c', value = -1, key= 13)
    d = col2.number_input('d', value = 0.5, key= 14)
    
    # st.subheader("Equlibrium")
    
    # def equ_cal(a,b,c,d):
    #     return (a-c)/(d-b), (a*d-c*b)/(d-b)
    
    # p_e, q_e = equ_cal(a,b,c,d)
    
    # if st.button('Calculate Equilibrium'):
    st.write("Equilibrium:")
    if (a*d>c*b) and (abs(b)>d):
        p_e = (a-c)/(d-b)
        q_e = (a*d-c*b)/(d-b) 
        st.latex(f'Q^* = {round(q_e,2)}, P^* = {round(p_e,2)}')   
    else:
        st.error('Equilibrium does not exist or |b|<d.', icon="🚨")
        st.stop()
    
    st.write("---")
    st.subheader("Cobweb Model Setup:")  
       
    init_price = st.number_input("Cases1: Price after initial shock (t=0): ", value = (-a/b+c/d)*1/3)  
    period = st.slider("Case 1: Periods", min_value = 1, max_value = 10)  
       

   
    # calculate price for each periods cobweb        
    
    data_cob, data_cob_draw = cob_series(init_price)   
    
    # if st.button('Cobweb Graph'):       
    p = figure(title="Cobweb Model: Convergent Fluctuation", x_axis_label='Q', y_axis_label='P')
                

    
    # 生成一组x值
    q_vals = np.linspace(0, a, 100)
    # 计算对应的y值
    if b!=0:
        p_demand_vals = [demand(x) for x in q_vals]
    else: 
        p_demand_vals = np.linspace(0, (a-c)/d + 3, 100)
    if d!=0:
        p_supply_vals = [supply(x) for x in q_vals]

    # 绘制线性函数曲线
    
    if (b!=0) and (d!=0):
        p.line(q_vals, p_demand_vals, line_width=2, legend_label="Demand")
        p.line(q_vals, p_supply_vals, line_width=2, legend_label="Supply", color = "green")
    if (b==0) and (d!=0):
        p.line([a]*100, p_demand_vals, line_width=2, legend_label="Demand")
        p.line(q_vals, p_supply_vals, line_width=2, legend_label="Supply", color = "green")
    if b!=0 and d==0:
        st.error("d cannot be 0.")
    if b==0 and d==0:
        st.error("d cannot be 0.")
    
    circle = Circle(x=q_e, y=p_e, size=10, fill_color="red")
    
    p.add_glyph(circle)
    
    # draw cobweb
    scatter = p.circle(data_cob_draw['q'][0:(2*period)], data_cob_draw['p'][0:(2*period)], size=6, color='#C73E1D')
    p.multi_line([data_cob_draw['q'][0:(2*period)]], [data_cob_draw['p'][0:(2*period)]], line_width=2, color='#EFA00B', alpha = 0.5)
    hover = HoverTool(renderers=[scatter],
                tooltips=[('Q', '@x'), ('P', '@y')],
                mode='mouse')
    p.add_tools(hover)    
    
    for i in range(1, 2*period):
        if i<= 2*5-1: 
            arrowhead = NormalHead(fill_color='black', line_color='black', size=8, line_alpha = 0.3)
            arrow = Arrow(end=arrowhead, line_color='#EFA00B', line_width=2, line_alpha = 0.5, 
                        x_start=data_cob_draw['q'][i-1], y_start=data_cob_draw['p'][i-1], x_end=data_cob_draw['q'][i], y_end=data_cob_draw['p'][i])
            # 在绘图对象上添加箭头
            p.add_layout(arrow)       
    
    p2 = figure(title="Price for each period", x_axis_label='Q', y_axis_label='P')
    p2.line(range(1,period+1), data_cob['p'][0:period],line_width=2, color = "orange")
    p2.circle(range(1,period+1), data_cob['p'][0:period], size=10, color='#C73E1D')

    # p3 = gridplot([p,p2], toolbar_location="right")
    st.bokeh_chart(p, use_container_width=True)
    st.bokeh_chart(p2, use_container_width=True)

with tab2:
    st.header("Case 2: Divergent Fluctuation")
    st.write("")
    st.write("Suppose a linear Demand and Supply model is:")
    st.latex(r'''
             \begin{align*} 
             Q^d & =&  a + bP & \quad a>0, b<0\\
             Q^s & = & c + dP & \quad c<0, d>0\\
             \end{align*}
             ''')
    st.latex(r'''
              |\frac{a}{b}| > |\frac{c}{d}|, \quad |b| < d
              ''')
    st.write("")
    
    col1, col2 = st.columns(2)
    col1.write("Demand")
    a = col1.number_input('a', value = 20, key= 21)
    b = col1.number_input('b', value = -1, key = 22)
    col2.write("Supply")
    c = col2.number_input('c', value = -1, key = 23)
    d = col2.number_input('d', value = 1.04, key = 24)
    
    # st.subheader("Equlibrium")
    
   
    # if st.button('Calculate Equilibrium'):
    st.write("Equilibrium:")
    if (a*d>c*b) and (abs(b)<d):
        p_e = (a-c)/(d-b)
        q_e = (a*d-c*b)/(d-b) 
        st.latex(f'Q^* = {round(q_e,2)}, P^* = {round(p_e,2)}')   
    else:
        st.error('Equilibrium does not exist or |b|>d.', icon="🚨")
        st.stop()
    
    st.write("---")
    st.subheader("Cobweb Model Setup:")  
       
    init_price = st.number_input("Case 2: Price after initial shock (t=0): ", value = 8/1.04)  
    period = st.slider("Case 2: Periods", min_value = 1, max_value = 10)  
   
    # calculate price for each periods cobweb        
    
    data_cob, data_cob_draw = cob_series(init_price)   
    
    # if st.button('Cobweb Graph'):       
    p3 = figure(title="Cobweb Model: Divergent Fluctuation", x_axis_label='Q', y_axis_label='P')
                

    
    # 生成一组x值
    q_vals = np.linspace(0, a, 100)
    # 计算对应的y值
    if b!=0:
        p_demand_vals = [demand(x) for x in q_vals]
    else: 
        p_demand_vals = np.linspace(0, (a-c)/d + 3, 100)
    if d!=0:
        p_supply_vals = [supply(x) for x in q_vals]

    # 绘制线性函数曲线
    
    if (b!=0) and (d!=0):
        p3.line(q_vals, p_demand_vals, line_width=2, legend_label="Demand")
        p3.line(q_vals, p_supply_vals, line_width=2, legend_label="Supply", color = "green")
    if (b==0) and (d!=0):
        p3.line([a]*100, p_demand_vals, line_width=2, legend_label="Demand")
        p3.line(q_vals, p_supply_vals, line_width=2, legend_label="Supply", color = "green")
    if b!=0 and d==0:
        st.error("d cannot be 0.")
    if b==0 and d==0:
        st.error("d cannot be 0.")
    
    circle = Circle(x=q_e, y=p_e, size=10, fill_color="red")
    
    p3.add_glyph(circle)
    
    # draw cobweb
    scatter = p3.circle(data_cob_draw['q'][0:(2*period)], data_cob_draw['p'][0:(2*period)], size=6, color='#C73E1D')
    p3.multi_line([data_cob_draw['q'][0:(2*period)]], [data_cob_draw['p'][0:(2*period)]], line_width=2, color='#EFA00B', alpha = 0.5)
    hover = HoverTool(renderers=[scatter],
                tooltips=[('Q', '@x'), ('P', '@y')],
                mode='mouse')
    p3.add_tools(hover)
    
    for i in range(1, 2*period):
        arrowhead = NormalHead(fill_color='black', line_color='black', size=8, line_alpha = 0.3)
        arrow = Arrow(end=arrowhead, line_color='#EFA00B', line_width=2, line_alpha = 0.5, 
                    x_start=data_cob_draw['q'][i-1], y_start=data_cob_draw['p'][i-1], x_end=data_cob_draw['q'][i], y_end=data_cob_draw['p'][i])
        # 在绘图对象上添加箭头
        p3.add_layout(arrow)
              
    p4 = figure(title="Price for each period", x_axis_label='Q', y_axis_label='P')
    p4.line(range(1,period+1), data_cob['p'][0:period],line_width=2, color = "orange")
    p4.circle(range(1,period+1), data_cob['p'][0:period], size=10, color='#C73E1D')

    # p3 = gridplot([p,p2], toolbar_location="right")
    st.bokeh_chart(p3, use_container_width=True)
    st.bokeh_chart(p4, use_container_width=True)
    
with tab3:
    st.header("Case 3: Continuous Fluctuation")
    st.write("")
    st.write("Suppose a linear Demand and Supply model is:")
    st.latex(r'''
             \begin{align*} 
             Q^d & =&  a + bP & \quad a>0, b<0\\
             Q^s & = & c + dP & \quad c<0, d>0\\
             \end{align*}
             ''')
    st.latex(r'''
              |\frac{a}{b}| > |\frac{c}{d}|, \quad |b| = d
              ''')
    st.write("")
    
    col1, col2 = st.columns(2)
    col1.write("Demand")
    a = col1.number_input('a', value = 10, key= 31)
    b = col1.number_input('b', value = -1, key = 32)
    col2.write("Supply")
    c = col2.number_input('c', value = -1, key = 33)
    d = col2.number_input('d', value = 1, key = 34)
    
    # st.subheader("Equlibrium")
    
   
    # if st.button('Calculate Equilibrium'):
    st.write("Equilibrium:")
    if (a*d>c*b) and (abs(b)==d):
        p_e = (a-c)/(d-b)
        q_e = (a*d-c*b)/(d-b) 
        st.latex(f'Q^* = {round(q_e,2)}, P^* = {round(p_e,2)}')   
    else:
        st.error('Equilibrium does not exist or |b|!= d.', icon="🚨")
        st.stop()
    
    st.write("---")
    st.subheader("Cobweb Model Setup:")  
       
    init_price = st.number_input("Case 3: Price after initial shock (t=0): ", value = (-a/b + c/d)*1/3)  
    period = st.slider("Case 3: Periods", min_value = 1, max_value = 10)  
    
        # calculate price for each periods cobweb        
    
    data_cob, data_cob_draw = cob_series(init_price)   
    
    # if st.button('Cobweb Graph'):       
    p5 = figure(title="Cobweb Model: Continuous Fluctuation", x_axis_label='Q', y_axis_label='P')         
    
    # 生成一组x值
    q_vals = np.linspace(0, a, 100)
    # 计算对应的y值
    if b!=0:
        p_demand_vals = [demand(x) for x in q_vals]
    else: 
        p_demand_vals = np.linspace(0, (a-c)/d + 3, 100)
        
    if d!=0:
        p_supply_vals = [supply(x) for x in q_vals]

    # 绘制线性函数曲线
    
    if (b!=0) and (d!=0):
        p5.line(q_vals, p_demand_vals, line_width=2, legend_label="Demand")
        p5.line(q_vals, p_supply_vals, line_width=2, legend_label="Supply", color = "green")
    if (b==0) and (d!=0):
        p5.line([a]*100, p_demand_vals, line_width=2, legend_label="Demand")
        p5.line(q_vals, p_supply_vals, line_width=2, legend_label="Supply", color = "green")
    if b!=0 and d==0:
        st.error("d cannot be 0.")
    if b==0 and d==0:
        st.error("d cannot be 0.")
    
    circle = Circle(x=q_e, y=p_e, size=10, fill_color="red")
    
    p5.add_glyph(circle)
    
    # draw cobweb
    scatter = p5.circle(data_cob_draw['q'][0:(2*period)], data_cob_draw['p'][0:(2*period)], size=6, color='#C73E1D')
    p5.multi_line([data_cob_draw['q'][0:(2*period)]], [data_cob_draw['p'][0:(2*period)]], line_width=2, color='#EFA00B', alpha = 0.5)
    hover = HoverTool(renderers=[scatter],
                tooltips=[('Q', '@x'), ('P', '@y')],
                mode='mouse')
    p5.add_tools(hover)
    
    for i in range(1, 2*period):
        arrowhead = NormalHead(fill_color='black', line_color='black', size=8, line_alpha = 0.3)
        arrow = Arrow(end=arrowhead, line_color='#EFA00B', line_width=2, line_alpha = 0.5, 
                  x_start=data_cob_draw['q'][i-1], y_start=data_cob_draw['p'][i-1], x_end=data_cob_draw['q'][i], y_end=data_cob_draw['p'][i])
        # 在绘图对象上添加箭头
        p5.add_layout(arrow)
              
    p6 = figure(title="Price for each period", x_axis_label='Q', y_axis_label='P')
    p6.line(range(1,period+1), data_cob['p'][0:period],line_width=2, color = "orange")
    p6.circle(range(1,period+1), data_cob['p'][0:period], size=10, color='#C73E1D')

    # p3 = gridplot([p,p2], toolbar_location="right")
    st.bokeh_chart(p5, use_container_width=True)
    st.bokeh_chart(p6, use_container_width=True)