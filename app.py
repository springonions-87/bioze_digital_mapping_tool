import streamlit as st

padding=0
st.set_page_config(page_title="Bioze Interative Tool", layout="wide")

# st.markdown(
#     """
#     <style>
#     .small-font {
#         font-size:12px;
#         font-style: italic;
#         color: #b1a7a6;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

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
    st.markdown("### BIOZE Digital Tool")
    st.markdown("")


# Run the Streamlit app
if __name__ == "__main__":
    main()