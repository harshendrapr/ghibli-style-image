import streamlit as st
import requests
from PIL import Image
import io
import os

# Hugging Face token (you must set this in your environment or Render)
HF_TOKEN = os.environ.get("HF_API_TOKEN")

st.set_page_config(page_title="Ghibli Style Generator", layout="centered")
st.title("🌸 Ghibli Style Image Generator (Free Hugging Face)")

prompt = st.text_input("Describe your scene:", "a cozy forest village in Studio Ghibli style, anime, whimsical, highly detailed")
submit = st.button("Generate Image")

if submit:
    if not HF_TOKEN:
        st.error("Missing HF_API_TOKEN. Please set it as an environment variable.")
    else:
        with st.spinner("Generating image..."):
            api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
            headers = {
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": prompt}
            )

            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Ghibli Style Image")
                st.download_button("📥 Download", data=image_bytes, file_name="ghibli.png", mime="image/png")
            else:
                st.error(f"Generation failed ({response.status_code}): {response.text}")
