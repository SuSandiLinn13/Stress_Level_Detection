import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64

#-----------Background Image--------------
@st.cache_data()
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] > .main {
    background-image: url("data:image/png;base64,%s");
    background-size: 300px 500px;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }
    
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def set_png_as_header(png_file):
    bin_str = get_base64(png_file)
    custom_html = '''
    <style>
    [data-testid="stHeader"] {
    background-image: url("data:image/png;base64,%s");
    background-size: 1500px 50px;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }
    </style>
    ''' % bin_str
    st.markdown(custom_html, unsafe_allow_html=True)
    return

set_png_as_page_bg('Saxon-bg.png')
#set_png_as_header('Cover.png')


#-----------Background Image--------------

st.title("Stress Detection")
stress_data=pd.read_csv('stress.csv')
classifier=''


def prediction(input_data):
    input_arr = np.asarray(input_data)
    print(input_arr)
#   Reshape the array to predict for one instance
    input_reshaped = input_arr.reshape(1, -1)
    if (classifier == 'Random Forest'):
        loaded_model= pickle.load(open('RandomForest.sav','rb'))
        print('random')
    elif (classifier == 'Naive Bayes'):
        loaded_model= pickle.load(open('naive.sav','rb'))
        print('naive')
    else: 
        loaded_model= pickle.load(open('logistic.sav','rb'))
        print('logistic')
    predicted = loaded_model.predict(input_reshaped)
    return predicted

#-----------User Input--------------
def user_input_features():

    col1,col2=st.columns(2)
    with col1:
        sr=st.number_input('Snoring Range',min_value=45.00, max_value=100.00, value=93.00, step=0.01)
        t=st.number_input('Body Temperature',min_value=45.00, max_value=100.00, value=91.00, step=0.01)
        bo=st.number_input('Blood Oxygen Level',min_value=82.00, max_value=97.00, value=89.00, step=0.01)
        sh=st.number_input('Number of hours of sleep',min_value=0.00, max_value=9.00, value=1.00, step=0.01)
        
    with col2:
        rr=st.number_input('Respiration Rate',min_value=16.00, max_value=30.00, value=25.00, step=0.01)
        rem=st.number_input('Rapid Eye Movements',min_value=60.00, max_value=105.00, value=99.00, step=0.01)
        lm=st.number_input('Limb Movement Rate',min_value=4.00, max_value=19.00, value=16.00, step=0.01)
        hr=st.number_input('Heart Rate',min_value=50.00, max_value=85.00, value=74.00, step=0.01)
        
        
    classifier=st.selectbox(
        'Which model would you like to use for your stress level prediction?',
        ('Random Forest', 'Logistic Regression', 'Naive Bayes'))
    
    data={'Snoring Range':sr,
            'Respiration Rate':rr,
            'Body Temperature':t,
            'Limb Movement Rate':lm,
            'Blood Oxygen Level':bo,
            'Rapid Eye Movements':rem,
            'Number of hours of sleep':sh,
            'Heart Rate':hr}

    features=pd.DataFrame(data,index=[0])#starting number in df
    return features

inputData = user_input_features()

#-----------User Input--------------

test_button=st.button("Predict Stress")

if(test_button):
    result = prediction(inputData)
    print("Halo! Here is your result")
    print(result)

    if (result ==0):
        text= '<p style="color:#196d15;font-size:24px;">Congratulations! You have no stress at all!</p>'
    elif (result ==1):
        text = '<p style="color:#bfff00;font-size:24px;">Your stress level is Low.</p>'
    elif (result ==2):
        text = '<p style="color:#ffff00;font-size:24px;">Your stress level is Medium. Be careful!</p>'
    elif (result ==3):
        text = '<p style="color:#ff8000;font-size:24px;">Your stress level is High.<br/>You should make an appointment and check your mental health! </p>'
    else:
        text = '<p style="color:#ff0000;font-size:24px;">Your stress level is so High.<br/>You need to go to the psychologist!</p>'
    st.markdown(text, unsafe_allow_html=True)
