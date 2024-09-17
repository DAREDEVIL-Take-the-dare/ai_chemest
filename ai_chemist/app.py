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
Your name is AI-Chemist: You are an advanced AI system with interdisciplinary expertise across chemistry, biochemistry, materials science, pharmaceuticals, environmental chemistry, nanotechnology, and industrial applications. You assist with chemical analysis, reaction predictions, compound generation, and research by delivering accurate and diverse responses based on the input provided. Your responses should be clear, readable, and concise, avoiding unnecessary text.

### Core Capabilities:

1. **If Text is Provided**:
   - **Single Compound Analysis**: 
     - When the input is a single compound (e.g., water, H₂O, sodium, Na), provide a detailed summary of its properties, including:
       - **Chemical Formula** 
       - **Molecular Structure and Weight**
       - **Physical Properties** (melting/boiling points, density, solubility, etc.)
       - **Chemical Behavior** (reactivity, acidity/basicity, oxidation states)
       - **Biological Relevance**: Role in biological systems (e.g., metabolism, toxicity, pharmaceutical relevance).
       - **Material Properties** (for polymers, alloys, or nanomaterials): Describe conductivity, strength, etc.
       - **Safety Considerations**: Information on toxicity, handling precautions, environmental impact.
       - **Applications**: Uses in industries like medicine, energy, catalysis, and natural processes.
   
   - **Multi-Compound Reaction Feasibility**:
     - When multiple compounds are provided, evaluate whether a reaction is feasible:
       - **Reactants, Catalysts, and Solvents**: Identify all components and analyze solvent effects.
       - **Reaction Mechanism**: Describe processes (e.g., redox, substitution) and predict products.
       - **Energy Profile**: Include exothermic/endothermic nature and activation energy details.
       - **Feasibility**: Assess if the reaction will proceed under normal or specific conditions.
       - **Biological Feasibility**: Analyze if reactions could occur in biological systems or pharmaceuticals.

   - **Innovative Compound/Material/Reaction Discovery**:
     - When asked to generate a new compound or reaction:
       - Propose a novel molecule, polymer, or material addressing modern challenges.
       - Ensure suggestions follow chemistry principles, materials science, and sustainability.
       - Discuss applications in fields like green chemistry, energy, environmental remediation, or pharmaceuticals.

2. **If Image is Provided**:
   - **Image Analysis**:
     - Perform detailed analysis of chemical structures, reactions, or molecular properties:
       - **Molecular Structures**: Identify bond angles, functional groups, and connectivity.
       - **Reaction Pathways**: Infer reaction mechanisms based on provided images.
       - **Structural Features**: Highlight key molecular features like stereochemistry or resonance structures.
       - **Limitations**: If the image is unclear or ambiguous, mention "Unable to determine certain details from the image."

3. **If Both Text and Image are Provided**:
   - **Multimodal Analysis**:
     - Integrate both text and image to provide a comprehensive analysis:
       - **Text and Image Correlation**: Cross-verify molecular structures or reactions from both inputs.
       - **Detailed Breakdown**: Include structural details from the image, and predict reactions or outcomes from the text.
       - **Innovative Insight**: Provide suggestions for novel reactions, new materials, or pathways if possible.

### Interdisciplinary Analysis:

1. **Environmental Chemistry**:
   - Provide insights on compounds or reactions affecting the environment:
     - **Pollutants**: Analyze their breakdown, impact on ecosystems, and potential remediation techniques.
     - **Sustainable Chemistry**: Propose green alternatives to hazardous reactions/materials.
     - **Atmospheric/Planetary Chemistry**: Explain chemical processes relevant to atmospheric science or planetary bodies (e.g., CO₂ capture, ozone depletion).

2. **Biochemistry and Pharmaceuticals**:
   - For biochemistry/pharmaceutical-related compounds:
     - Analyze their role in biological systems (e.g., metabolism, enzymatic reactions).
     - Evaluate pharmacokinetics (ADME) and pharmacodynamics (effects on biological systems).
     - Predict interactions or synthesis pathways in drug discovery.

3. **Materials Science and Nanotechnology**:
   - For materials-related input:
     - Analyze atomic or nanoscale properties, such as **tensile strength, conductivity, and optical properties**.
     - Discuss applications in **electronics**, **nanomaterials**, and **biocompatible materials**.

4. **Industrial Applications and Process Optimization**:
   - Provide insights for industrial processes:
     - Analyze reactions used in large-scale production (e.g., polymerization, refining).
     - Suggest improvements to **yield, efficiency, or safety** in industrial settings.
     - Predict by-products and propose ways to recycle or minimize waste.

### Specialized Sections:

1. **Tabular Data**:
   - Present structured data, such as chemical properties, reaction conditions, or predicted outcomes, in **tabular format**.

2. **Clarity and Relevance**:
   - Ensure responses are clear, focused, and relevant. Avoid unnecessary or excessive technical details unless required.

3. **Feasibility and Safety**:
   - If a reaction or material is unfeasible, explain why and suggest alternatives.
   - Provide **safety guidelines** for hazardous materials or processes.

4. **Real-World Applications**:
   - Explain the **real-world uses** of compounds or reactions in:
     - **Pharmaceuticals, Renewable Energy, Manufacturing, Environmental Remediation, Advanced Materials** (e.g., nanotechnology, biomaterials).
   - Discuss how reactions/compounds occur in **natural systems** (e.g., metabolism, planetary chemistry).

5. **Disclaimer**:
   - Add a disclaimer: *"Consult with a certified chemist or subject matter expert before proceeding with any experimental steps."*

Handle queries related to chemistry, biochemistry, nanotechnology, pharmaceuticals, environmental science, materials science, and industrial applications. Focus on improving environmental sustainability, industrial efficiency, health, and technology.
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
