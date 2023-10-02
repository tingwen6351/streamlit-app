import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from bokeh.plotting import figure, show
from bokeh.models import Circle, Label
from bokeh.models import HoverTool, ColumnDataSource

st.title("Demand & Supply")


tab1, tab2, tab3, tab4 = st.tabs(
    ["Static Equilibrium", "Demand Shock", "Supply Shock", "Both Demand and Supply Shock"])

with tab1:
    st.header("Set up a linear demand and Supply Model")
    st.write("")
    st.write("Suppose a linear Demand and Supply model is:")
    st.latex(r'''
             \begin{align*} 
             Q^d & =&  a + bP & \quad a>0, b<0\\
             Q^s & = & c + dP & \quad c<0, d>0\\
             \end{align*}
             ''')
    st.latex(r'''
              |\frac{a}{b}| > |\frac{c}{d}|
              ''')
    st.write("")
    
    col1, col2 = st.columns(2)
    col1.write("Demand")
    a = col1.number_input('a', value = 10)
    b = col1.number_input('b', value = -1)
    col2.write("Supply")
    c = col2.number_input('c', value = -1)
    d = col2.number_input('d', value = 0.5)
    
    st.subheader("Equlibrium")
    
    def equ_cal(a,b,c,d):
        return (a-c)/(d-b), (a*d-c*b)/(d-b)
    
    p_e, q_e = equ_cal(a,b,c,d)
    
    if st.button('Calculate Equilibrium'):
        if a*d>c*b:
            p_e = (a-c)/(d-b)
            q_e = (a*d-c*b)/(d-b)
            
            p = figure(title="Demand and Supply Model", x_axis_label='Q', y_axis_label='P')
            
            
            # 定义线性函数
            def demand(x):
                return (x-a)/b
            def supply(x):
                return (x-c)/d
            
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
            
            # 绘制指向交点的线和注释
            # p.segment(x0=q_e, y0=p_e, x1=0, y1=p_e, color="red", line_width=2)
            # label = Label(x=q_e, y=p_e+0.2, text="Equ", text_color="red")
            # p.add_layout(label)

            st.bokeh_chart(p, use_container_width=True)
            st.write('')
            st.latex(f'Q^* = {round(q_e,2)}, P^* = {round(p_e,2)}')
        else:
            st.error('Equilibrium does not exist!! Wrong parameters.', icon="🚨")
        
    
with tab2:
    st.write("Each period, there is a demand shock. ")
    st.write("")
    periods = st.number_input('Demand Shocks: Number of Periods', value = 10)
    periods = int(periods)
    # 生成随机平行移动的距离
    shifts = np.random.uniform(low= -c/d + a/b, high=-a/b, size=periods)

    # 生成随机平行移动后的曲线并绘制
    q_li =[]
    p_li=[]
    for shift in shifts:
        q_ = (d*a-c*b)/(d-b)-shift*b*d/(d-b)
        p_ = q_/d-c/d
        if (q_ > 0) and (p_ >0):
            q_li.append(q_)
            p_li.append(p_)
    p2 = figure(title="Equilibria under Demand Shocks", x_axis_label='Q', y_axis_label='P')
    # p.line(q_li, p_li, line_width=2)
    # 绘制每期的散点
    data = {
        'q': q_li,
        'p': p_li,
        'time': [str(i) for i in list(range(1,periods+1))]
    }
    p2.circle(data['q'], data['p'], size=10, color='#C73E1D')

    # 绘制连接所有点的线
    p2.multi_line([data['q']], [data['p']], line_width=2, color='#EFA00B', alpha = 0.5)
    for i in range(len(data['q'])):
        label = Label(x=data['q'][i], y= data['p'][i]+0.2, text=data['time'][i], text_font_size="10px", text_color="#BEB2C8")
        p2.add_layout(label)
        
    st.bokeh_chart(p2, use_container_width=True)
    st.write("We got Supply Curve !!")

    

with tab3:
    st.write("Each period, there is a supply shock. ")
    st.write("")
    periods = st.number_input('Supply Shocks: Number of Periods', value = 10)
    periods = int(periods)
    # 生成随机平行移动的距离
    shifts = np.random.uniform(low= c/d, high=-a/b+c/d, size=periods)

    # 生成随机平行移动后的曲线并绘制
    q_li =[]
    p_li=[]
    for shift in shifts:
        q_ = (d*a-c*b)/(d-b)+shift*b*d/(d-b)
        p_ = q_/b-a/b
        if (q_ > 0) and (p_ >0):
            q_li.append(q_)
            p_li.append(p_)
    p3 = figure(title="Equilibria under Supply Shocks", x_axis_label='Q', y_axis_label='P')
    # p.line(q_li, p_li, line_width=2)
    # 绘制每期的散点
    data = {
        'q': q_li,
        'p': p_li,
        'time': [str(i) for i in list(range(1,periods+1))]
    }
    p3.circle(data['q'], data['p'], size=10, color='#C73E1D')

    # 绘制连接所有点的线
    p3.multi_line([data['q']], [data['p']], line_width=2, color='#EFA00B', alpha = 0.5)
    for i in range(len(data['q'])):
        label = Label(x=data['q'][i], y= data['p'][i]+0.1, text=data['time'][i], text_font_size="10px", text_color="#BEB2C8")
        p3.add_layout(label)
        
    st.bokeh_chart(p3, use_container_width=True)
    st.write("We got Demand Curve !!")
    
with tab4:
    st.write("Each period, there is either a supply or a demand shock or both. ")
    st.write("")
    periods = st.number_input('Number of Periods', value = 10)
    periods = int(periods)
    # 生成随机平行移动的距离
    shifts_supply = np.random.uniform(low= c/d, high=-a/b+c/d, size=periods)
    shifts_demand = np.random.uniform(low= -c/d + a/b, high=-a/b, size=periods)
    # 生成随机平行移动后的曲线并绘制
    q_li =[]
    p_li=[]
    for d_shift, s_shift in zip(shifts_demand, shifts_supply):
        q_ = (d*a-c*b)/(d-b)+(s_shift-d_shift)*b*d/(d-b)
        p_ = q_/b-a/b + d_shift
        if (q_ > 0) and (p_ >0):
            q_li.append(q_)
            p_li.append(p_)
    p4 = figure(title="Equilibria under Both Demand and Supply Shocks", x_axis_label='Q', y_axis_label='P')
    # p.line(q_li, p_li, line_width=2)
    # 绘制每期的散点
    data = {
        'q': q_li,
        'p': p_li,
        'time': [str(i) for i in list(range(1,len(q_li)+1))]
    }
    source = ColumnDataSource(data)
    
    scatter = p4.circle('q', 'p', size=10, source = source, color='#C73E1D')

    # 绘制连接所有点的线
    lines = p4.multi_line([data['q']], [data['p']], line_width=2, color='#EFA00B', alpha = 0.5)
    for i in range(len(data['q'])):
        label = Label(x=data['q'][i], y= data['p'][i]+0.2, text=data['time'][i], text_font_size="10px", text_color="#BEB2C8")
        p4.add_layout(label)
        
    hover = HoverTool(renderers=[scatter],
                  tooltips=[('Period', '@time'), ('Q', '@q'), ('P', '@p')],
                  mode='mouse')

    p4.add_tools(hover)
        
    st.bokeh_chart(p4, use_container_width=True)           
    st.write("We got a Mess !!")