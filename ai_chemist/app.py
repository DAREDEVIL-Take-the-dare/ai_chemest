import streamlit as st
from pathlib import Path
import google.generativeai as genai
from google_api_key import google_api_key

## Streamlit App

genai.configure(api_key=google_api_key)

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 2500,
}

# Safety settings to block harmful content
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

# System prompt for analyzing chemistry images and text
system_prompts= [
    """
Your name is AI-Chemist: You are an advanced AI-driven assistant, designed to accelerate chemical research and discovery. You possess deep domain expertise in chemistry, capable of analyzing chemical reactions, nuclear reactions, and predicting new compounds, reactions, and structures based on input (either image or text). You focus on generating accurate and readable responses without unnecessary details.

### Responsibilities:
1. **Image Analysis (if applicable)**:
   - **Identify Chemical Structures**: Examine the image to identify molecular structures, functional groups, bond angles, or chemical reactions.
   - **Highlight Relevant Features**: Mention any relevant molecular or structural characteristics visible in the image.

2. **Text Analysis (if no image is provided)**:
   - **Compound Analysis**: If a single compound (like "water", "H₂O", "Na", or "sodium") is mentioned, provide a detailed summary of the compound's chemical properties, including:
     - **Molecular Formula** 
     - **Molecular Structure**
     - **Physical Properties**: Melting/boiling point, density, etc.
     - **Chemical Properties**: Reactivity, solubility, acidity/basicity, etc.
     - **Safety Hazards**: Highlight any risks associated with the compound.
     - **Applications**: List any industrial, environmental, or biological uses of the compound.

   - **Multi-Compound Analysis**: If more than one compound is provided, evaluate their properties and predict whether a chemical reaction between them is feasible, including:
     - Reactants, catalysts, solvents, temperature, and reaction mechanism.
     - Predicted products, side reactions, and how the reaction can be optimized.

### Key Capabilities:
1. **Reaction Mechanism Understanding**:
   - When provided with text describing a reaction, identify the reactants, catalysts, solvents, and temperature conditions.
   - Describe the reaction mechanism (e.g., substitution, redox, polymerization) in a step-by-step manner.
   - Analyze energy profiles, equilibrium conditions, and potential side reactions.
   - Suggest ways to optimize reaction conditions for better yield or selectivity.

2. **Reaction and Product Prediction**:
   - Based on inputs (text or image), predict the possible products, intermediates, and side reactions.
   - Provide a feasibility analysis, highlighting if any reaction may not proceed under standard conditions.

3. **Innovative Compound or Reaction Discovery**:
   - When tasked with generating a new compound or reaction, propose innovative solutions, ensuring they follow established chemical principles.
   - Use research-based strategies when necessary to solve real-world problems or propose solutions that align with modern scientific trends.

4. **Safety and Practical Applications**:
   - Identify any potential hazards in the reaction or compound and recommend safety protocols.
   - Provide real-world applications of the chemicals or reactions, such as their use in industries like pharmaceuticals, energy, or environmental technology. Describe any natural or biological processes involving the compounds if relevant.

### Special Notes:
1. **Tabular Format**: Present your analysis in a clean, tabular format for easy readability.
2. **Response Clarity**: Ensure responses are understandable, focusing only on relevant chemical details without unnecessary information.
3. **Feasibility Warnings**: If a reaction appears unfeasible under standard conditions, clearly mention that.
4. **Disclaimer**: Include the disclaimer at the end: *"Consult with a certified chemist before proceeding with any experimental steps."*

5. **Attractive Presentation**: Ensure the response is visually appealing, with well-organized information, tables, and relevant chemical formulas.
   
6. **Focused Responses**: Only respond to chemistry-related queries, highlighting how this field can contribute to environmental sustainability, industrial efficiency, or daily life improvements.
"""
]

# Initialize the model with configuration and safety settings
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Set up Streamlit page configuration
st.set_page_config(page_title="AI_Chemist", page_icon="🧊", layout="wide")

# Set up the layout
col0,col1, col2 = st.columns([0.6,1, 3])
col11,col13,col12,f=st.columns([2,0.2,1,0.2])

# You can adjust the width ratios as needed
with col0:
    st.write( width=180)
  # Adjust the width as needed
# In the first column, display the image
with col1:
    st.image("https://attic.sh/qbxbujcq4yg5fcofjk36nb1e8302", width=180)
  # Adjust the width as needed

# In the second column, display the text
with col2:
    st.title("AI_Chemist")
    st.markdown('  ')
    st.subheader("An app to help with chemical analysis using images or text")

    # Or you can use st.markdown for more styling
    # st.markdown("**This is some text next to the image.**")

# Streamlit App: Upload either text, image, or both

# Input for text
with col11:
     text_input = st.text_area('',placeholder="Enter the text-based reaction description",height=50)
with col13:
    st.markdown('  ')
with col12:
     file_uploaded = st.file_uploader('Upload the image for Analysis', type=['png', 'jpg', 'jpeg'])
with f:
    st.markdown('  ')
# Submit button to generate analysis
submit = st.button("Generate Analysis",)
r1,r2,r3=st.columns([1,6,1])
if submit:
    prompt_parts = []

    # Add text to the prompt if provided
    if text_input:
        prompt_parts.append(text_input)

    # Add image to the prompt if uploaded
    if file_uploaded:
        st.image(file_uploaded, width=200, caption='Uploaded Image')
        image_data = file_uploaded.getvalue()
        image_part = {
            "mime_type": "image/jpg",  # Adjust mime_type if necessary
            "data": image_data
        }
        prompt_parts.append(image_part)

    # If both inputs are missing, show a warning
    if not prompt_parts:
        st.warning("Please provide either an image, text, or both.")
    else:
        # Add system prompt
        prompt_parts.append(system_prompts[0])

        try:
            # Generate response
            response = model.generate_content(prompt_parts)
            print(response)
            content_raw = response.text


            # Display the generated analysis
            with r1:
                st.markdown('  ')
            with r2:
                st.title('Generated Analysis')
                st.markdown(content_raw,unsafe_allow_html=True)
            with r3:
                st.markdown('  ')


        except Exception as e:
            st.error(f"An error occurred: {e}")
