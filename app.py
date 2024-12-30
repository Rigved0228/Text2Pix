import base64
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Function to add app background image


def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""<style>.stApp {{
                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                background-size: cover
            }}</style>""",
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(
            "Background image not found. The app will continue without it.")

# Function to validate Hugging Face API token with improved error handling


def is_valid_token(api_key):
    if not api_key.startswith('hf_'):
        st.sidebar.error(
            "Token should start with 'hf_'. Please check your token.")
        return False

    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        # Print the token length and first/last few characters
        st.sidebar.info(f"Token length: {len(api_key)}")
        st.sidebar.info(f"Token starts with: {api_key[:10]}...")

        response = requests.get(
            "https://huggingface.co/api/whoami",
            headers=headers,
            timeout=10
        )

        # Print the full response for debugging
        st.sidebar.info(f"Response status: {response.status_code}")
        st.sidebar.info(f"Response text: {response.text}")

        if response.status_code == 200:
            return True
        else:
            st.sidebar.error(
                f"Validation failed with status code: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        st.sidebar.error("Connection timed out. Please try again.")
        return False
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Connection error: {str(e)}")
        return False

# Function to generate images using Hugging Face API


def generate_image(prompt, api_key):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {api_key}"}

    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "negative_prompt": "blurry, bad quality, distorted, ugly, bad anatomy"
        }
    }

    try:
        # Check if model is ready
        response = requests.post(API_URL, headers=headers, json={
                                 "inputs": ""}, timeout=10)
        if response.status_code == 503:
            st.info(
                "⏳ Model is loading... This might take a minute or two. Please wait.")
            st.warning(
                "If this takes too long, try refreshing the page or generating again.")
            return None

        # Generate image
        response = requests.post(
            API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            image_bytes = response.content
            image = Image.open(BytesIO(image_bytes))
            return image
        else:
            error_message = response.json().get('error', 'Unknown error occurred')
            raise Exception(error_message)

    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")
    except Exception as e:
        raise Exception(f"Error generating image: {str(e)}")

# Main Streamlit app


def main():
    # App title
    st.markdown("""
        <svg width="600" height="100">
            <text x="50%" y="50%" font-family="monospace" font-size="42px" fill="Green" 
                text-anchor="middle" stroke="white" stroke-width="0.5" stroke-linejoin="round">
                🎨ImagiCraft🎨
            </text>
        </svg>
    """, unsafe_allow_html=True)

    # Try to add background
    add_bg_from_local('background.jpg')

    # Initialize session state
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'is_valid_token' not in st.session_state:
        st.session_state.is_valid_token = False

    # Sidebar with API token input
    st.sidebar.markdown("### API Configuration")
    api_key_input = st.sidebar.text_input(
        "Enter your Hugging Face API token:",
        type="password",
        help="Get your free token at huggingface.co/settings/tokens"
    )

    # Validate token when it changes
    if api_key_input and api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        with st.spinner("Validating token..."):
            st.session_state.is_valid_token = is_valid_token(api_key_input)

    # Main content area
    st.markdown("### Create Your Image")
    img_description = st.text_area(
        'Image Description:',
        height=100,
        help="Describe the image you want to generate. Be specific!"
    )

    # Generate button
    if st.button('🎨 Generate Image', use_container_width=True):
        if st.session_state.api_key and st.session_state.is_valid_token:
            if img_description:
                try:
                    with st.spinner('🎨 Generating your masterpiece... Please wait...'):
                        response = generate_image(
                            img_description, st.session_state.api_key)
                        if response is not None:
                            st.success("✨ Image generated successfully!")
                            st.image(response, caption=img_description,
                                     use_column_width=True)
                except Exception as e:
                    st.error(f"❌ {str(e)}")
                    if "loading" in str(e).lower():
                        st.info(
                            "⏳ The model is still loading. Please wait a minute and try again.")
                    elif "rate limit" in str(e).lower():
                        st.warning(
                            "⚠️ Rate limit reached. Please wait a minute before trying again.")
            else:
                st.warning("⚠️ Please provide an image description.")
        else:
            st.warning("⚠️ Please input a valid Hugging Face API token.")

    # Sidebar instructions
    st.sidebar.markdown("""
    ### 📝 How to Get Started:
    1. Create a free account at [Hugging Face](https://huggingface.co/join)
    2. Go to Settings → Access Tokens
    3. Create a new token (READ access is sufficient)
    4. Copy and paste your token above
    """)

    # Tips section
    st.markdown("""
    ### 💡 Tips for Better Results:
    - Be specific in your descriptions
    - Include details about style (e.g., "digital art", "oil painting", "photograph")
    - Mention lighting and composition
    - Specify colors and mood
    - Add artistic references if desired
    
    Example: "A serene landscape at sunset, showing a peaceful lake surrounded by pine trees, 
    with mountains in the background, digital art style, warm colors, dramatic lighting"
    """)


if __name__ == "__main__":
    main()
