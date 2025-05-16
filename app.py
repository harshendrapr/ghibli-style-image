import streamlit as st
import requests
import base64
import time
import os

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
REPLICATE_MODEL_VERSION = "c1a5db2c2b6c4d5eb46cb8e7542fdf8c8e6200cded6dfc05bb2de8133ccf43cb"

st.set_page_config(page_title="Ghibli Style Image", layout="centered")
st.title("🌸 Ghibli Style Image Generator")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Ghibli Style"):
        with st.spinner("Generating..."):
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": REPLICATE_MODEL_VERSION,
                    "input": {
                        "image": f"data:image/jpeg;base64,{image_base64}",
                        "prompt": "Studio Ghibli style, magical, whimsical anime scene"
                    }
                }
            )

            prediction = response.json()
            status_url = prediction.get("urls", {}).get("get")

            image_url = None
            if status_url:
                while True:
                    result = requests.get(status_url, headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"})
                    result_json = result.json()
                    status = result_json.get("status")

                    if status == "succeeded":
                        image_url = result_json.get("output", [None])[0]
                        break
                    elif status == "failed":
                        st.error("Image generation failed.")
                        break
                    time.sleep(1)

            if image_url:
                st.success("Image generated!")
                st.image(image_url, caption="Ghibli Style Image")

                download_button = requests.get(image_url)
                st.download_button(
                    label="📥 Download Image",
                    data=download_button.content,
                    file_name="ghibli-style.png",
                    mime="image/png"
                )
            else:
                st.error("Failed to retrieve image.")
