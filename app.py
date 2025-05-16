import streamlit as st
import requests
from PIL import Image
import io
import os

HF_TOKEN = os.environ.get("HF_API_TOKEN")

st.title("Ghibli Style Image Generator")

prompt = st.text_input(
    "Enter your prompt:",
    "a magical forest village in Studio Ghibli style, anime, whimsical, highly detailed"
)
generate = st.button("Generate")

if generate:
    if not HF_TOKEN:
        st.error("Please set HF_API_TOKEN environment variable with your Hugging Face token.")
    else:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        payload = {"inputs": prompt}

        with st.spinner("Generating image..."):
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Ghibli Style Image")
                st.download_button(
                    label="Download Image",
                    data=image_bytes,
                    file_name="ghibli_style.png",
                    mime="image/png"
                )
            else:
                st.error(f"Failed to generate image: {response.status_code} - {response.text}")
