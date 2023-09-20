import streamlit as st
import json
from api import score
from PIL import Image

# path = "/tmp/app_files/"

with open('data.json','r') as dataa:
    data_dict = json.load(dataa)


title = data_dict['title']
description = data_dict['description']
input = data_dict['input']
# icon = data_dict['icon']


st.set_page_config(page_title=title, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
with open('style.css') as f:
    st.write(f'<style>{f.read()}</style>', unsafe_allow_html=True)
col_desc,blank, col_refract_logo, col_snowflake = st.columns([8,1,1,2])

with col_desc:
    st.title(title)
    st.write(description)
with col_snowflake:
    snowflake_icon = Image.open('snowflake_logo.png')
    st.image(snowflake_icon, caption='') 
with col_refract_logo:
    refract_icon = Image.open('powered_by_refract.png')
    st.image(refract_icon, caption='') 

col1, col2 = st.columns([7,3])
input_data = {}


with col1:

    with st.form("input_details"):
        for inp in input:
            if(inp['type'] == "slider"):
                input_data[inp['label']] = [st.slider(label=inp['label'],min_value=inp['min'],max_value=inp['max'],value=inp['default'],step=inp['step'])]
                
            elif(inp['type'] == "selectbox"):
               input_data[inp['label']] = [st.selectbox(inp['label'],inp['options'],inp['index'])]
            elif(inp['type'] == 'number'):
                input_data[inp['label']] = [st.number_input(inp['label'],inp['min'],None,inp['default'],inp['step'])]
            elif(inp['type'] == 'text'):
               input_data[inp['label']] = [st.text_input(inp['label'], value=inp['default'])]
        
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Run Model", help="Clicking this button you will hit the model with above input to get the output.")
        if submitted:
            print(input_data)
            with col2:
                with st.spinner('Predicting...'):
                    # model_path=path + "model.pkl.gz"
                    import pandas as pd
                    data = pd.DataFrame(input_data)
                    print(data.head())
                    response = score(data)

                    #hit api and get response
                    if response:
                        st.success('Model inferred successfully!')
                        st.subheader("Model Prediction : " + str(response))
                        # st.write("<b>Confidence : </b>" + str(response['confidence']), unsafe_allow_html=True)
                    else:
                        st.error('Model inference failed!')