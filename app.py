import streamlit as st
from PIL import Image
import pandas as pd
st.title("Auto Finder Printer")

# Load the Excel file
@st.cache_data
def load_data():
    df = pd.read_csv("printer_sheet_15_04_25.csv") 
    return df

df = load_data()

# Session state to control disabling
if 'use_image' not in st.session_state:
    st.session_state.use_image = False
if 'use_text' not in st.session_state:
    st.session_state.use_text = False

# Toggle logic
def toggle_input(use_image: bool):
    st.session_state.use_image = use_image
    st.session_state.use_text = not use_image

# Radio buttons to choose input type
choice = st.radio("Select input type:", ["Text", "Image"], index=0)
toggle_input(choice == "Image")

# Inputs
result = None
if st.session_state.use_text:
    text_input = st.text_input("Enter some text:")
    text_input = text_input.strip()
    if text_input:
        filtered_df = df[df["Description"].str.contains(text_input, case=False, na=False)]
        filtered_df1 = df[df["Part Name"].str.contains(text_input, case=False, na=False)]
        # st.write(f"### Search for res1: {text_input}  {len(filtered_df)}")
        # st.dataframe(filtered_df)
        # st.write(f"### Search for  res2 : {text_input}  {len(filtered_df1)}")
        # st.dataframe(filtered_df1)
        filtered_df =filtered_df.loc[:,["Part Name","Description","LOCATION"]]
        filtered_df1 =filtered_df1.loc[:,["Part Name","Description","LOCATION"]]
        if len(filtered_df) >0 or len(filtered_df1) > 0:
            print("pass")
            st.write(f"### Results :")
            if(len(filtered_df)>0):
                print(f"pass1 ..{len(filtered_df)} {len(filtered_df1)}")
                # filtered_df = filtered_df[filtered_df['LOCATION'].notna() & (filtered_df['LOCATION'] != '')]
                st.dataframe(filtered_df)
                st.write(f"### Result 1:")
                
            else:
                # filtered_df1 = filtered_df1[filtered_df1['LOCATION'].notna() & (filtered_df1['LOCATION'] != '')]
                st.dataframe(filtered_df1)
                st.write(f"### Results 2:")
        else:
            st.write(f"### Not found")            
elif st.session_state.use_image:
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image")
        result = image

# Output
st.markdown("---")
if result is not None:
    st.subheader("Result:")
    if isinstance(result, Image.Image):
        st.write("As of now image feature is updating ...  ! try with text. ")
    else:
        st.write(f"You entered: `{result}`")
