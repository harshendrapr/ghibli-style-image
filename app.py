import streamlit as st
import requests
import base64
import time
import os

# --- Setup ---
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
REPLICATE_MODEL_VERSION = "c1a5db2c2b6c4d5eb46cb8e7542fdf8c8e6200cded6dfc05bb2de8133ccf43cb"

st.set_page_config(page_title="Ghibli Style Image", layout="centered")
st.title("🌸 Ghibli Style Image Generator")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Ghibli Style"):
        with st.spinner("Sending image to model..."):
            try:
                image_bytes = uploaded_file.read()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                # Create prediction
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

                if response.status_code != 201:
                    st.error(f"Error creating prediction: {response.text}")
                    st.stop()

                prediction = response.json()
                status_url = prediction["urls"]["get"]

                # Poll for result
                image_url = None
                while True:
                    poll = requests.get(status_url, headers={
                        "Authorization": f"Token {REPLICATE_API_TOKEN}"
                    })
                    result = poll.json()

                    if result["status"] == "succeeded":
                        output = result.get("output")
                        if isinstance(output, list) and len(output) > 0:
                            image_url = output[0]
                        elif isinstance(output, str):
                            image_url = output
                        break
                    elif result["status"] == "failed":
                        st.error("Model failed to generate image.")
                        break
                    time.sleep(1)

                # Display output
                if image_url:
                    st.success("Here's your Ghibli-style image!")
                    st.image(image_url, caption="Ghibli Style Output", use_column_width=True)
                    st.download_button("📥 Download Image", data=requests.get(image_url).content,
                                       file_name="ghibli-style.png", mime="image/png")
                else:
                    st.error("Failed to retrieve image from model output.")

            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
