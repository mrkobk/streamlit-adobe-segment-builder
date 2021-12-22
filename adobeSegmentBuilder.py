#!/usr/bin/env python
# coding: utf-8

# In[13]:


import streamlit as st
from tqdm import tqdm
import time
import os
import json
import pandas as pd
from copy import deepcopy


# In[14]:

st.set_page_config(layout="wide")	
st.title("Adobe Segment Builder")
menu = ["ag-adi-ar-prod",
		"ag-adi-au-prod",
		"ag-adi-be-prod",
		"ag-adi-br-prod",
		"ag-adi-ca-prod",
		"ag-adi-cl-prod",
		"ag-adi-co-prod",
		"ag-adi-de-prod",
		"ag-adi-es-prod",
		"ag-adi-eu-prod",
		"ag-adi-fr-prod",
		"ag-adi-it-prod",
		"ag-adi-in-prod",
		"ag-adi-nl-prod",
		"ag-adi-nz-prod",
		"ag-adi-mx-prod",
		"ag-adi-ru-prod",
		"ag-adi-pe-prod",
		"ag-adi-pl-prod",
		"ag-adi-tr-prod",
		"ag-adi-uk-prod",
		"ag-adi-us-prod",
		"ag-adi-at-prod",
		"ag-adi-cl-prod",
		"ag-rbk-ar-prod",
		"ag-rbk-au-prod",
		"ag-rbk-be-prod",
		"ag-rbk-br-prod",
		"ag-rbk-ca-prod",
		"ag-rbk-cl-prod",
		"ag-rbk-co-prod",
		"ag-rbk-de-prod",
		"ag-rbk-es-prod",
		"ag-rbk-eu-prod",
		"ag-rbk-fr-prod",
		"ag-rbk-it-prod",
		"ag-rbk-nl-prod",
		"ag-rbk-nz-prod",
		"ag-rbk-mx-prod",
		"ag-rbk-pe-prod",
		"ag-rbk-pl-prod",
		"ag-rbk-tr-prod",
		"ag-rbk-uk-prod",
		"ag-rbk-us-prod",
		"ag-rbk-at-prod",
		"ag-rbk-cl-prod"
		]
			
adobe_suite = st.sidebar.selectbox("Select Adobe Property",menu)
    
st.subheader(f"Segment to be populated in {adobe_suite} Property")
                
segment_name = st.text_input("Enter Segment Name", "")
segment_description = st.text_input("Enter Segment Description (optional)", "")
segment_owner_id = st.selectbox('Enter User Account you want the Segment to populate in:',
                          ('Mirko', 'Jur', 'Melania'), key="UserId")

st.write('This segment will be created for:', segment_owner_id)
    
dct = {
    
       "Mirko": 200132409,
       "Jur":200185531,
       "Melania":200264507
       }

segment_owner_id = dct.get(segment_owner_id)
        
upload = st.file_uploader("Upload List of URLs or ProductIDs", type=["csv"])

if upload is not None:
    
    file_details = {
        "filename":upload.name,
        "filetype":upload.type,
        "filesize":upload.size
                   }
    #st.write(loadcsvpreview(upload), width=300)
    lst = pd.read_csv(upload)
    st.dataframe(lst.head(10))
    
    raw = {'definition': {'container': {'context': 'hits',
           'func': 'container',
           'pred': {'func': 'or',
            'preds': []}},
          'func': 'segment',
          'version': [1, 0, 0]},
         'description': '',
         'id': '',
         'isPostShardId': True,
         'migratedIds': [],
         'name': '',
         'owner': {'id': ''},
         'rsid': ''}

    dct = {'description': lst.columns[0],
          'func': 'streq-in',
          'list': [],
          'val': {'func': 'attr', 'name': lst.columns[0]}}
          
    
    lst = lst.iloc[:,0].tolist()
    #lst = lst['variables/entryprop34'].tolist()
    chunks = [lst[i:i + 500] for i in range(0, len(lst), 500)]
    
    for i in range(len(chunks)):
    
    	dct_copy = deepcopy(dct)
    	raw["definition"]["container"]["pred"]["preds"].append(dct_copy)
    	raw["name"] = segment_name
    	raw["description"] = segment_description
    	raw["owner"]["id"] = segment_owner_id
    	raw["rsid"] = adobe_suite
    	
    url_counter = 0
    
    for i in range(len(raw["definition"]["container"]["pred"]["preds"])):
    	raw["definition"]["container"]["pred"]["preds"][i]["list"] = chunks[i]
    	url_counter += len(raw["definition"]["container"]["pred"]["preds"][i]["list"])
    	
    st.success(f'toBeCopied.json was generated with {url_counter} entries. Copy by clicking the blue icon next to the first curly bracket below. Then head over to https://adobedocs.github.io/analytics-2.0-apis/#/segments/segments_createSegment')
    st.write(raw)
				
#st.download_button('Download JSON payload', raw, 'application/json')  # Defaults to 'text/plain'


    


# In[ ]:




