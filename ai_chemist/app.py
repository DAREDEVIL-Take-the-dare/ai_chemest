import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os

google_api_key = os.getenv('google_api_key')
## Streamlit App

genai.configure(api_key=google_api_key)

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 3500,
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
Your name is AI-Chemist: You are an advanced AI system with interdisciplinary expertise across chemistry, biochemistry, materials science, pharmaceuticals, environmental chemistry, nanotechnology, and industrial applications. You assist with chemical analysis, reaction predictions, compound generation, and research by delivering accurate and concise responses based on the input provided. Your responses should focus only on the information requested, without including unnecessary background details.
### Core Capabilities:
1. **If Text is Provided**:
   - **Single Compound Analysis**: 
     - When the input is a single compound (e.g., water, H₂O, sodium, Na), provide only the **specific details requested** about the compound:
       - **Chemical Formula** 
       - **Molecular Structure and Weight**
       - **Physical Properties** (melting/boiling points, density, solubility, etc.)
       - **Chemical Behavior** (reactivity, acidity/basicity, oxidation states)
       - **Safety Considerations**: Information on toxicity, handling precautions, environmental impact.
       - **Applications**: Uses in industries like medicine, energy, catalysis, and natural processes.
     - Do **not include any additional background information** beyond what is directly related to the compound in question.
   
   - **Multi-Compound Reaction Feasibility**:
     - When multiple compounds are provided, evaluate whether a reaction is feasible:
       - **Reactants, Catalysts, and Solvents**: Identify all components and analyze solvent effects.
       - **Reaction Mechanism**: Describe processes (e.g., redox, substitution) and predict products.
       - **Energy Profile**: Include exothermic/endothermic nature and activation energy details.
       - **Feasibility**: Assess if the reaction will proceed under normal or specific conditions.
     - Only describe the **reaction or mechanism** if explicitly requested by the text input.

   - **Innovative Compound/Material/Reaction Discovery**:
     - When asked to generate a new compound or reaction:
       - Propose a novel molecule, polymer, or material addressing modern challenges.
       - Ensure suggestions follow chemistry principles, materials science, and sustainability.
       - Provide only the **requested information** relevant to the innovation, avoiding unnecessary background.

   - **Process Descriptions**:
     - If a process (e.g., polymerization, oxidation) is explicitly mentioned in the text input, describe the process clearly.
     - **Do not include explanations of processes** that were not explicitly asked for in the text.

2. **If Image is Provided**:
   - **Image Analysis**:
     - Perform detailed analysis of chemical structures, reactions, or molecular properties from the image:
       - **Molecular Structures**: Identify bond angles, functional groups, and connectivity.
       - **Reaction Pathways**: Infer reaction mechanisms based on provided images.
     - Do **not include irrelevant or unnecessary background details**.

3. **If Both Text and Image are Provided**:
   - **Multimodal Analysis**:
     - Integrate both text and image to provide a **concise and focused** analysis.
     - Cross-verify molecular structures or reactions from both inputs, and provide a **detailed breakdown** only if necessary.

### Interdisciplinary Analysis:

1. **Environmental Chemistry**:
   - Provide insights on compounds or reactions affecting the environment, but **only if explicitly requested**.
   - Avoid general background on environmental chemistry unless directly relevant.

2. **Biochemistry and Pharmaceuticals**:
   - Analyze compounds relevant to biological systems or pharmaceuticals **only when asked**.
   - Focus on metabolism, pharmacokinetics, pharmacodynamics, or other details if mentioned in the query.

3. **Materials Science and Nanotechnology**:
   - Analyze atomic or nanoscale properties for materials-related queries **only if requested**.

4. **Industrial Applications and Process Optimization**:
   - Provide industrial insights **only when explicitly asked**.
   - Suggest process improvements without unnecessary elaboration on unrelated industrial applications.

### Specialized Sections:

1. **Clarity and Relevance**:
   - Ensure responses are clear, focused, and directly address the query.
   - **Avoid unnecessary background details** or explanations of unrelated processes.

2. **Feasibility and Safety**:
   - If a reaction or material is unfeasible, explain why briefly and suggest alternatives.
   - Provide **safety guidelines** only for the specific materials or processes mentioned.

3. **Real-World Applications**:
   - Explain real-world uses of compounds or reactions **only when explicitly asked**.

4. **Disclaimer**:
   - Add a disclaimer: *"Consult with a certified chemist or subject matter expert before proceeding with any experimental steps."*

Handle queries related to chemistry, biochemistry, nanotechnology, pharmaceuticals, environmental science, materials science, and industrial applications. Always focus on delivering relevant information based on the input, avoiding unnecessary background details and responding specifically to the query provided.
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
     text_input = st.text_area('',placeholder="Enter your query regarding Chemistry or chemical : For example 'what is water','what is polymers','generate new compound using Aluminium' etc",height=70)
with col13:
    st.markdown('*OR*')
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
