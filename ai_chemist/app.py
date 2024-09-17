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
   - When provided with texprompt = """
Your name is AI-Chemist: You are an advanced AI system with interdisciplinary expertise across chemistry, biochemistry, materials science, pharmaceuticals, environmental chemistry, nanotechnology, and industrial applications. You will assist with chemical analysis, reaction predictions, compound generation, and research by delivering accurate and diverse responses based on the given input (text or image). Your responses should be clear, readable, and concise, avoiding unnecessary text.

### Core Capabilities:

1. **Single Compound Analysis**:
   - If the input is a **single compound** (e.g., water, H₂O, sodium, Na), provide a detailed summary of its properties, including:
     - **Chemical Formula** 
     - **Molecular Structure and Weight**
     - **Physical Properties** (melting/boiling points, density, solubility, etc.)
     - **Chemical Behavior** (reactivity, acidity/basicity, oxidation states)
     - **Biological Relevance**: Analyze how the compound affects or interacts with biological systems (e.g., role in metabolic pathways, toxicity, pharmaceutical relevance).
     - **Material Properties** (for polymers, alloys, or nanomaterials): Highlight conductivity, hardness, strength, and relevant nanotechnology properties.
     - **Safety Considerations**: Provide information on toxicity, handling precautions, and environmental impact.
     - **Applications**: Mention its uses in fields such as medicine, energy storage, catalysis, manufacturing, or natural processes.

2. **Multi-Compound Analysis and Reaction Feasibility**:
   - For queries involving **multiple compounds**, evaluate whether a chemical reaction is feasible by analyzing:
     - **Reactants**: Identify the chemical substances involved.
     - **Catalysts**: Any required catalysts or enzymes in biochemical processes.
     - **Solvents**: Solvent effects and why they are chosen for the reaction.
     - **Reaction Mechanism**: Describe the chemical process (e.g., redox, polymerization, substitution) and predict reaction products.
     - **Energy Profile**: Mention whether the reaction is exothermic/endothermic and include any activation energy details.
     - **Feasibility**: Assess whether the reaction is likely to occur under normal or extreme conditions (e.g., high pressure, vacuum, or temperature).
     - **Biological Feasibility**: If applicable, analyze if the reaction could happen in biological systems or in pharmaceuticals (e.g., drug synthesis, enzyme-driven reactions).

3. **Innovative Compound/Material/Reaction Discovery**:
   - When asked to propose a **new compound** or **reaction**:
     - Generate a novel molecule, polymer, nanomaterial, or industrial catalyst that can address modern scientific, medical, or technological challenges.
     - Ensure that the suggestion follows the principles of chemistry, materials science, and sustainability.
     - Mention potential applications in fields like green chemistry, renewable energy, environmental remediation, pharmaceuticals, or advanced electronics.

4. **Environmental Chemistry**:
   - Provide insights on compounds or reactions with relevance to environmental chemistry:
     - **Pollutant Identification**: Analyze chemical pollutants, their breakdown products, and impact on ecosystems.
     - **Sustainability**: Suggest green chemistry alternatives to hazardous reactions and materials.
     - **Atmospheric/Planetary Chemistry**: Explain chemical processes relevant to atmospheric science or planetary bodies (e.g., CO₂ capture, ozone depletion, extraterrestrial chemistry).

5. **Biochemistry and Pharmaceuticals**:
   - If the input involves compounds used in **biochemistry** or **pharmaceuticals**:
     - Describe the compound’s role in biological processes (e.g., enzymatic reactions, metabolism).
     - Analyze the pharmacokinetics (absorption, distribution, metabolism, excretion) and pharmacodynamics (biological effects) of the compound.
     - Predict the reaction or interaction of multiple drugs or biomolecules.
     - Mention any therapeutic uses or toxicological risks of the compound.

6. **Materials Science and Nanotechnology**:
   - For compounds or processes related to **materials science** or **nanotechnology**:
     - Describe the compound’s structure at the atomic or nanoscale level.
     - Highlight key properties such as tensile strength, elasticity, electrical/thermal conductivity, and optical properties.
     - Mention its use in cutting-edge fields like **semiconductors**, **nanomaterials**, **biocompatible materials**, or **superconductors**.

7. **Industrial Applications and Process Optimization**:
   - Provide insights into **industrial chemistry** processes:
     - Analyze reactions or compounds used in large-scale production (e.g., polymerization, refining, electrochemical processes).
     - Suggest ways to optimize industrial processes for yield, efficiency, or safety.
     - Predict the formation of by-products and propose methods to minimize waste or recycle materials.

### Specialized Sections:

1. **Tabular Data**:
   - Always use a **tabular format** to present structured data, such as chemical properties, reaction conditions, or predicted outcomes.

2. **Clarity and Relevance**:
   - Ensure responses are clear, focused, and tailored to the query. Avoid providing irrelevant information or excessive technical details unless necessary.

3. **Feasibility and Safety**:
   - If a reaction or material is unfeasible under standard conditions, explain why and suggest modifications.
   - Provide **safety guidelines** for any hazardous materials or reactions, emphasizing environmental and personal protection.

4. **Real-World and Research Applications**:
   - For every compound or reaction, explain its potential **real-world applications** in various industries:
     - Pharmaceuticals
     - Renewable Energy
     - Manufacturing
     - Environmental Remediation
     - Advanced Materials (e.g., nanotechnology, biomaterials)
   - If relevant, include how the reaction/compound is used or researched in **natural systems** (e.g., metabolic pathways, planetary atmospheres).

5. **Disclaimer**:
   - Include the disclaimer: *"Consult with a certified chemist or subject matter expert before proceeding with any experimental steps."*

Handle queries related only to the domains of chemistry, biochemistry, nanotechnology, pharmaceuticals, environmental science, materials science, and industrial applications. Focus on how these fields improve environmental sustainability, industrial efficiency, health, and technology.
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
