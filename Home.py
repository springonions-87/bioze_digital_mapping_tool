import streamlit as st


padding=0
st.set_page_config(page_title="Begin", layout="wide", initial_sidebar_state="expanded")


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
    st.title(":seedling: Provincie Zuid-Holland Interactieve Tool")
    
    st.markdown("")
    st.markdown("")
    st.markdown("")

    st.subheader(":bulb: Over de tool...")
    st.markdown("De tool bestaat uit een ***tweestaps*** leerproces om gebruikers te betrekken bij het leren over de voordelen en afwegingen die gepaard gaan met de plaatsing van grootschalige biogasvergisters.")

    st.markdown("")
    st.markdown("")

    st.subheader(":compass: Hoe de tool te gebruiken...")
    st.markdown("")
    st.markdown("**Fase 1: Geschiktheidsanalyse**")
    st.markdown("Fase 1 verwelkomt gebruikers om een ​​geschiktheidsanalyse op meerdere criteria uit te voeren. Geschiktheidsanalyse kan worden beschouwd als een methode voor locatieselectie.")
    st.markdown("We zullen deze methode gebruiken om te bepalen of een bepaald gebied in de regio geschikt is voor het bouwen van een grootschalige vergister.")
    st.markdown("Aan het einde van deze fase beschikt u over een lijst met kandidaatlocaties voor grootschalige vergisters.")
    st.markdown("")
    st.markdown("**Fase 2: Beleidsverkenner**")
    st.markdown("Fase 2 nodigt gebruikers uit om combinaties van kandidaat-locaties voor grootschalige vergisters te verkennen om de in de regio geproduceerde mest efficiënt te verwerken voor de productie van biogas.")
    st.markdown("We zullen uw lijst met kandidaatlocaties uit Fase 1 gebruiken om scenario's te genereren die bestaan ​​uit de meest strategische locaties voor vergisters om bepaalde doelen te bereiken.")
    st.markdown("Aan het einde van deze fase leer je de kosten en baten van verschillende scenario’s.")
    st.markdown("")
    st.markdown(":repeat: **Iterative Learning**") 
    col1, col2, col3 = st.columns(3)
    with col2: 
        st.image("./two_phase.png")

    
    st.markdown("")
    st.divider()
    st.markdown("Deze tool is ontwikkeld voor Data Gedreven werken binnen het Provincie Zuid Holland Programma Landelijk Gebied. Het bouwt verder op het al bestaande BIOZE project. BIOZE is ontwikkeld voor het EU Interreg Project: BIOmass skills for Net Zero (BIOZE), door de Faculteit Geo-Informatie Wetenschap en Aardobservatie (ITC) van de Universiteit Twente.")


# Run the Streamlit app
if __name__ == "__main__":
    main()