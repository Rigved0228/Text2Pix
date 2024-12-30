# Text2Pix  

**Text-to-Image generation using DALL-E**  

Text2Pix is a Streamlit-based application that transforms textual prompts into high-quality images using OpenAI's powerful DALL-E model.  

## Features  

- **Text-to-Image Generation**:  
  Create stunning images from simple textual descriptions.  
- **Rate Limiting**:  
  Ensures responsible API usage and prevents excessive generation requests.  

## How It Works  

1. Input your desired text prompt into the application.  
2. The DALL-E model processes the prompt and generates an image.  
3. View and download your generated image instantly.  

## Project Structure  

- **`app.py`**: The main Streamlit application script.  
- **`background.jpg`**: Default background image used in the app.  
- **`requirements.txt`**: Python dependencies for the project.  
- **`img.png`**: Example image generated by DALL-E.  

## Installation  

Navigate to the project directory:  
```bash  
cd Text2Pix  
pip install -r requirements.txt
```
Run the Streamlit application:
```
streamlit run app.py
```
Open your browser and navigate to http://localhost:8501 or something like this to use the app.

## Usage
- Enter a descriptive text prompt in the input field.
- Click the "Generate" button to create an image.
- Save your generated image for personal use or projects.

## Future Enhancements
- Add customization options for image styles and resolutions.
- Implement multi-language support for textual prompts.
- Integrate user accounts to save and manage generated images.

## Contributing
Contributions are welcome! To contribute:

- Fork the repository.
- Create a new branch for your feature or bug fix:
  ```bash
  git checkout -b feature-name
  ```
- Commit your changes:
  ```bash
  git commit -m "Description of changes"  
  ```
- Push your branch:
  ```bash
  git push origin feature-name  
  ```
- Open a pull request.
Feel free to open issues for bugs or feature requests!
