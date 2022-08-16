import streamlit as st
import pandas as pd
from hccpy.hcc import HCCEngine
he = HCCEngine()

def get_hcc_from_icd10(dx):
  rp = he.profile([dx])
  hcc =  rp['hcc_map'].get(dx)
  if hcc is None:
    hcc = ""
  return hcc

prev_year_dx = st.selectbox('Previous Year ICD-10:',("E1169", "E1122", "E1151"))
curr_year_dx = st.selectbox('Current Year ICD-10 (Claims, EHR, or both):',("Not Recorded", "E1169", "E1122", "E1151", "R05"))


st.title('Hana Hou RAF Gap Logic')
care_gap_dx_level = prev_year_dx != curr_year_dx

rp = he.profile([prev_year_dx])
prev_hcc = get_hcc_from_icd10(prev_year_dx)
curr_hcc = get_hcc_from_icd10(curr_year_dx)
care_gap_hcc_level = len(set(prev_hcc).intersection(curr_hcc)) == 0

dat = dict(prev_year_dx=[prev_year_dx],
           curr_year_dx =[curr_year_dx],
           hcc = [prev_hcc],
           care_gap_dx_level =[care_gap_dx_level],
           care_gap_hcc_level = [care_gap_hcc_level])
st.table(pd.DataFrame(dat))

