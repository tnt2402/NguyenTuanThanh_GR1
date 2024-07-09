import streamlit as st
import pandas as pd
import numpy as np
import base64
import pickle

import pathlib
code_dir = pathlib.Path(__file__).parent.resolve()

categorical_columns = ['engine_type', 'series', 'model'
    , 'brand', 'assemble_place', 'transmission']



@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: linear-gradient(90deg, #ffc3a0 0%, #ffafbd 100%);
 background-position: center;
}}
[data-testid="stSidebar"] > div:first-child {{
background-color: #f9f7f4;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
models=['XGBoost', 'Random Forest',"LGBM" ]
st.write("#### Select model predict")
model_select=st.selectbox("Select the model predict:", models)


data = pd.read_csv("./data/output.csv")


st.write("#### Select the car features")


normalized_color_interiors = np.sort(np.array(data['normalized_color_interior'].unique().tolist())).tolist()
make_names= data['make_name'].unique().tolist()
model_names=data['model_name'].unique().tolist()
transmissions=data['transmission'].unique().tolist()
trims=data['trim'].unique().tolist()
drivetrains=data['drivetrain'].unique().tolist()
normalized_color_exteriors=data['normalized_color_exterior'].unique().tolist()
fuel_types=data['fuel_type'].unique().tolist()
body_styles=data['body_style'].unique().tolist()
cols= st.columns(2)
with cols[0]:
    make_name = st.selectbox("Select make_name:", make_names ,index=make_names.index(data['make_name'][10]))
    model_name = st.selectbox("Select model_name:", model_names ,index=model_names.index(data['model_name'][10]))
    transmission = st.selectbox("Select car transmission:", transmissions ,index=transmissions.index(data['transmission'][10]))
    trim = st.selectbox("Select car trim:",trims ,index=trims.index(data['trim'][10]))
    drivetrain = st.selectbox("Select drive train:",drivetrains ,index=drivetrains.index(data['drivetrain'][10]))
    normalized_color_exterior = st.selectbox("Select type of normalized_color_exterior",normalized_color_exteriors ,index=normalized_color_exteriors.index(data['normalized_color_exterior'][10]) )
    normalized_color_interior = st.selectbox("Select type of normalized_color_interior", normalized_color_interiors ,index=normalized_color_interiors.index("adrenaline red"))
# year = 2023 - year
with cols[1]:

    year = st.number_input("Select year:", min_value=1990, max_value=2024,value=int(data['year'][10]))
    mileage = st.number_input("Select driven kms:", min_value=0, max_value=1000000,value=int(data['mileage'][10]))
    door_count = st.number_input("Select number of doors:", min_value=2, max_value=100,value=int(data['door_count'][10]))
    fuel_type = st.selectbox("Select type of fuel_type", fuel_types ,index=fuel_types.index(data['fuel_type'][10]))
    body_style = st.selectbox("Select type of body_style",body_styles ,index=body_styles.index(data['body_style'][10]))

import time


with open(code_dir/"./model/mapping.txt", "r") as f:
        encoder = eval(f.read())

def predict(name,make_name,model_name,fuel_type,transmission,drivetrain,door_count,normalized_color_interior,normalized_color_exterior,body_style,mileage,trim,year):
    predict_df=pd.DataFrame({"name":[encoder["name"][name]],
                            "make_name":[encoder["make_name"][make_name]],
                            "model_name":[encoder["model_name"][model_name]],
                            "fuel_type":[encoder["fuel_type"][fuel_type]],
                            "transmission":[encoder["transmission"][transmission]],
                            "drivetrain":[encoder["drivetrain"][drivetrain]],
                            "normalized_color_exterior":[encoder["normalized_color_exterior"][normalized_color_exterior]],
                            "normalized_color_interior":[encoder["normalized_color_interior"][normalized_color_interior]],
                            "door_count":[door_count],
                            "body_style":[encoder["body_style"][body_style]],
                            "mileage":[mileage],
                            "trim":[encoder["trim"][trim]],
                            "year":[year],})
    if(model_select=="XGBoost"):
        with open(code_dir/"./model/xgb.pkl", "rb") as file:
            xgb = pickle.load(file)

            st.write("Predict price:",xgb.predict(predict_df)[0],"$")
    if(model_select=="Random Forest"):
        with open(code_dir/"./model/rf.pkl", "rb") as file:
            rf = pickle.load(file)
            st.write("Predict price:",rf.predict(predict_df)[0],"$")
    if(model_select=="LGBM"):
        with open(code_dir/"./model/lgbm.pkl", "rb") as file:
            lgbm = pickle.load(file)
            st.write("Predict price:",lgbm.predict(predict_df)[0],"$")
        
        
    
if st.button("Predict"):
    name=make_name+ " "+model_name
    predict(name,make_name,model_name,fuel_type,transmission,drivetrain,door_count,normalized_color_interior,normalized_color_exterior,body_style,mileage,trim,year)
    