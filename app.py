import streamlit as st
import requests
from PIL import Image
import io
import os

# Hugging Face token (optional for higher limits)
HF_TOKEN = os.environ.get("HF_API_TOKEN")

st.set_page_config(page_title="Ghibli Style Generator", layout="centered")
st.title("🌸 Ghibli Style Image Generator (Hugging Face)")

prompt = st.text_input("Describe your scene:", "a cozy village in Studio Ghibli style")
submit = st.button("Generate Image")

if submit:
    with st.spinner("Generating image..."):
        api_url = "https://api-inference.huggingface.co/models/nitrosocke/Ghibli-Diffusion"
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}" if HF_TOKEN else "",
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
            st.image(image, caption="Generated Ghibli Style Image")
            st.download_button("📥 Download", data=image_bytes, file_name="ghibli.png", mime="image/png")
        else:
            st.error(f"Generation failed: {response.status_code}\n{response.text}")
