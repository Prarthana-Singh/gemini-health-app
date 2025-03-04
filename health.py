







from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit UI Setup
st.set_page_config(page_title="Gemini Health App", layout="wide")

# Sidebar Content
with st.sidebar:
    st.title("📌 App Information")
    st.markdown("""
    ### 👨‍💻 Developer: Prarthana
    ### 🌟 Features:
    - 📸 Upload a food image to analyze its calorie content
    - 🧠 AI-powered analysis using Google Gemini
    - 📊 Detailed breakdown of calories for each food item
    - ⚡ Fast and user-friendly interface

    ### 📌 How to Use:
    1. Click on **'Upload an Image'** and select a food image.
    2. Optionally, enter any dietary preferences in the text box.
    3. Click **'Analyze Calories'** and wait for the AI to process your request.
    4. Get a detailed calorie breakdown and total calorie count!
    """)

st.title("🍏 Gemini Health App - Calorie Estimator")
st.write("Upload a food image and get the estimated calorie count!")

input = st.text_input("Enter any specific dietary preferences or instructions:", key="input")

uploaded_file = st.file_uploader("📸 Upload an Image", type=["jpg", "jpeg", "png"], help="Upload an image of your meal")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Your Uploaded Image", use_column_width=True, output_format="auto")

submit = st.button("🔍 Analyze Calories")

input_prompt = """
You are an expert nutritionist. Analyze the food items in the image and provide a breakdown of total calories, along with calorie details for each item in the following format:

1. Item Name - Calories
2. Item Name - Calories
...
Total Calories: XXXX kcal
"""

if submit:
    with st.spinner("Analyzing your food items... 🍽️"):
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input)
            st.success("✅ Analysis Complete!")
            st.subheader("🍽️ Your Meal's Calorie Breakdown:")
            st.write(response)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
