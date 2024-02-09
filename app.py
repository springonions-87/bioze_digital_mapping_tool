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
    st.markdown(":one: Suitability Analysis")
    st.markdown("")
    st.markdown(":two: Policy Explorer")
    st.markdown("")


    st.divider()
    st.markdown("This tool is developed for the EU Interreg Project: BIOmass skills for Net Zero (BIOZE), by University of Twente’s Faculty of Geo-Information Science and Earth Observation (ITC).")


# Run the Streamlit app
if __name__ == "__main__":
    main()