import time, os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from googletrans import Translator
from gtts import gTTS

# loading the saved models
diabetes_model = pickle.load(open('C:/Users/illad/OneDrive/Desktop/multiple disease prediction system/saved models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('C:/Users/illad/OneDrive/Desktop/multiple disease prediction system/saved models/heart_disease_model.sav', 'rb'))


def translate_text(text, dest_lang):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

def translate_result1(k, language='en'):
    translator = Translator()
    translated_result = translator.translate(k,dest=language)
    return translated_result.text

def ask_question(question_text, lang_code, question_number):
    translated_text = translate_text(question_text, lang_code)
    filename = f"question_{question_number}.mp3"
    tts = gTTS(text=translated_text, lang=lang_code)
    tts.save(filename)  
    time.sleep(10)# Introduce a 1-second delay
    os.system(f"start {filename}")  # Windows
    time.sleep(10)

def text_to_speech1(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("predict.mp3")
    time.sleep(10)
    os.system("start predict.mp3")

  
# sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',

                           ['Diabetes Prediction',
                            'Heart Disease Prediction'
                            # , 'parkinsons prediction'
                        ],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)


# Diabetes Prediction Page
if selected == 'Diabetes Prediction':

    # page title
    st.title('Diabetes Prediction using ML')
    questions = [
        ("do u have a dry mouth?",'en') ,
       ("are u feeling unusual thirst?",'en'),
        ("do you have Frequent urination in large amounts?",'en'),
        ("are u feeling like Fatigue?",'en'),
        ("do u feel Hungrier and eat more than usual?",'en'),
        ("are u Being tired?",'en'),
        ("are u  Having Blurry Vision?",'en'),
        ("are u facing Slow healing power?",'en')
    ]
    
    user_responses = []
    for idx, (question, lang_code) in enumerate(questions):
        ask_question(f"Question {idx+1}: {question} if Yes click 1", 'te', idx+1)
        user_input = st.radio(f" {question} {idx+1}:", options=[0,1])
        st.write(user_input)
        user_responses.append(user_input)


            
    if st.button('Diabetes Test Result'):
        diab_prediction = diabetes_model.predict([user_responses])
        k=diab_prediction[0]
        diab_diagnosis = translate_result1("diabetic positive " if k == 1 else " diabetic negative", language='te')
        st.success(diab_diagnosis)
        text_to_speech1(diab_diagnosis, language='te')


# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':

    # page title
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction

    if st.button('Heart Disease Test Result'):

        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)
