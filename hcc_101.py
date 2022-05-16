import streamlit as st
import pandas as pd
import numpy as np
import json
from hccpy.hcc import HCCEngine
he = HCCEngine()

st.title('HCC 101')
age_text = st.number_input(label="Age", value=70)
gender_text = st.selectbox('Gender:',('M', 'F'))
icd10_text = st.text_input(label="Enter ICD-10 Codes:", value="E1169, I5030, I509, I211, I209, R05")

rp = he.profile(icd10_text.split(","), age=age_text, sex = gender_text)

hcc_map = pd.DataFrame(rp['hcc_map']).transpose()
details = pd.DataFrame(rp['details'],  index=[0]).transpose()

st.subheader("Risk Score")
st.header(round(rp['risk_score'], 3))

st.subheader("ICD-10 / HCC")
st.dataframe(hcc_map)

st.subheader("Category / Weight")
st.dataframe(details)



