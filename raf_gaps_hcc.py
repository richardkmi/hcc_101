import datetime
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


st.title('Hana Hou RAF Gap Logic')

prev_year_dx = st.selectbox('Previous Year ICD-10:',("E1151", "E1169", "E1122"))
curr_year_dx = st.selectbox('Current Year ICD-10 (Claims, EHR, or both):',
  ("Not Recorded", "E1151", "E1169", "E1122", "R05"))



caregap_dx_level = prev_year_dx != curr_year_dx


rp = he.profile([prev_year_dx])
prev_hcc = get_hcc_from_icd10(prev_year_dx)
curr_hcc = get_hcc_from_icd10(curr_year_dx)
caregap_hcc_level = len(set(prev_hcc).intersection(curr_hcc)) == 0

most_recent_dx = st.selectbox('Current year dx is most recent for patient and HCC',("Ignore", True, False))

if most_recent_dx == "Ignore":
  dat = dict(prev_year_dx=[prev_year_dx],
           curr_year_dx =[curr_year_dx],
           dx_match = prev_year_dx == curr_year_dx,
           hcc_match = not caregap_hcc_level,
           caregap_dx =[caregap_dx_level],
           caregap_hcc = [caregap_hcc_level])
else:
  dat = dict(prev_year_dx=[prev_year_dx],
           curr_year_dx =[curr_year_dx],
           dx_match = prev_year_dx == curr_year_dx,
           hcc_match = not caregap_hcc_level,
           caregap_dx =[caregap_dx_level and most_recent_dx],
           caregap_hcc = [caregap_hcc_level and most_recent_dx])
st.table(pd.DataFrame(dat))


