import streamlit as st


padding=0
st.set_page_config(page_title="Home", layout="wide", initial_sidebar_state="expanded")


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(4)
        {
            text-align: end;
        } 
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title(":seedling: BIOZE Interactive Tool")
    
    st.markdown("")
    st.markdown("")
    st.markdown("")

    st.subheader(":bulb: About the tool...")
    st.markdown("The tool consists of a ***two-step*** learning process to engage users to learn about the benefits and trade-offs associated with placement of large-scale biogas digesters.")

    st.markdown("")
    st.markdown("")

    st.subheader(":compass: How to use the tool...")
    st.markdown("")
    st.markdown("**Phase 1: Suitability Analysis**")
    st.markdown("Phase 1 welcomes users to conduct a multi-criteria suitability analysis. Suitability analysis can be considered a method of site selection.")
    st.markdown("We will use this method to determine the appropriateness of a give area in the region for building a large-scale digester.")
    st.markdown("At the end of this phase, you will have a list of candidate sites for large-scale digesters.")
    st.markdown("")
    st.markdown("**Phase 2: Policy Explorer**")
    st.markdown("Phase 2 invites users to explore combinations of candidate sites for large-scale digesters in order to efficiently process manure produced in the region for biogas production.")
    st.markdown("We will use your list of candidate sites from Phase 1 to generate scenarios consisting of the most strategic locations for digesters to meet certain goals.")
    st.markdown("At the end of this phase, you will learn the costs and benefits of different scenarios.")
    st.markdown("")
    st.markdown(":repeat: **Iterative Learning**") 
    col1, col2, col3 = st.columns(3)
    with col2: 
        st.image("./two_phase.png")

    
    st.markdown("")
    st.divider()
    st.markdown("This tool is developed for the EU Interreg Project: BIOmass skills for Net Zero (BIOZE), by University of Twente’s Faculty of Geo-Information Science and Earth Observation (ITC).")


# Run the Streamlit app
if __name__ == "__main__":
    main()