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
  ("E1151", "Not Recorded", "E1169", "E1122", "R05"))



care_gap_dx_level = prev_year_dx != curr_year_dx


rp = he.profile([prev_year_dx])
prev_hcc = get_hcc_from_icd10(prev_year_dx)
curr_hcc = get_hcc_from_icd10(curr_year_dx)
care_gap_hcc_level = len(set(prev_hcc).intersection(curr_hcc)) == 0

rec_date = st.date_input("Enter dx capture date:")
max_date = st.date_input("Enter most recent (any) dx date for patient and hcc:",
value = datetime.date(2022, 3, 14))

max_date_gap = max_date >=rec_date and (care_gap_hcc_level or care_gap_dx_level)

dat = dict(prev_year_dx=[prev_year_dx],
           curr_year_dx =[curr_year_dx],
           hcc = [prev_hcc],
           care_gap_dx_level =[care_gap_dx_level],
           care_gap_hcc_level = [care_gap_hcc_level],
           care_gap_dx_recent_level = max_date_gap)
st.table(pd.DataFrame(dat))


