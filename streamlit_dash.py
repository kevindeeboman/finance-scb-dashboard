import streamlit as st
import pandas as pd
from pyscbwrapper import SCB
import datetime as dt
import plotly.express as px

### sidebar ###
st.sidebar.title('Finansmarknadsstatistiken')
options = st.sidebar.selectbox("Välj data", ("Penningmängd", "Pågående.."))

### Main page ###
st.title(options)
if options == "Penningmängd":
    # st.sidebar.date_input('Start datum', value=dt.datetime(2004, 1, 1), min_value=dt.datetime(2004, 1, 1), max_value=dt.datetime(2020, 3, 1))
    # st.sidebar.date_input('Slut datum', value=dt.datetime(2020, 4, 1), min_value=dt.datetime(2004, 2, 1), max_value=dt.datetime(2020, 4, 1))
    scb = SCB('sv', 'FM', 'FM5001')
    scb.go_down('FM5001A', 'FM5001SDDSPM')
    scb.set_query(penningmängdsmått=["M1", "M3"], 
                tabellinnehåll=['Penningmängd, mkr'])

    data = scb.get_data()['data']

    dta_m1 = []; dta_m3 = []
    for i in data:
        if i['key'][0] == '5LLM1.1E.NEP.V.A':
            dt_object = dt.datetime.strptime(i['key'][1], '%YM%m').date()
            obs = dt_object, int(i['values'][0])
            dta_m1.append(obs)
        elif i['key'][0] == "5LLM3a.1E.NEP.V.A":
            dta_m3.append(int(i['values'][0]))
    dataframe = pd.DataFrame(dta_m1, columns=['date','M1'])
    dataframe['M3'] = dta_m3
    selection = st.sidebar.selectbox("Penningmängsmått", ("M1", "M3", ["M1", 'M3']))
    fig = px.line(dataframe, x='date', y=selection)
    st.plotly_chart(fig)
    
    show_dta = st.sidebar.checkbox("Visa data")
    if show_dta:
        st.dataframe(dataframe)

    #analysis = st.sidebar.selectbox("Analysval", ('ARIMA'))


### ### ### ### ### ### ###


