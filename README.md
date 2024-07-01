[![DOI](https://zenodo.org/badge/682611837.svg)](https://zenodo.org/doi/10.5281/zenodo.10782927)

# BIOZE Interactive Decision Support Tool
Authors: Wen-Yu Chen [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/in/wenyuchen-tw-nl/), Johannes Flacke [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/in/johannes-flacke-38463340/), Pirouz Nourian [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/in/pirouz-nourian-71b10427/)  

The tool is developed for the EU Interreg Project: BIOmass skills for Net Zero ([BIOZE](https://www.interregnorthsea.eu/bioze)), on behalf of the Faculty of Geo-Information Science and Earth Observation ([ITC](https://www.itc.nl/)) at the University of Twente.  

Access the tool [here](https://bioze-interreg.streamlit.app/).  

User manual is available in [English](https://docs.google.com/document/d/1ycvVgknZ5-1XHSdp9uUJvC5qiD_btm0e/edit?usp=sharing&ouid=106170972880662385112&rtpof=true&sd=true "User Manual (Eng)") and [Dutch](https://docs.google.com/document/d/1kIgRok_GxITcHYWf_X_9CXxNyqwHAqdc/edit?usp=sharing&ouid=106170972880662385112&rtpof=true&sd=true "User Manual (Dutch)").  


<!-- GETTING STARTED -->
## Getting Started
It is highly recommended to create a virtual environment before running the project to manage dependencies effectively. If you encounter issues installing PyScipopt, please create a new environment with Python version 3.8.
  ```sh
  conda install --channel conda-forge pyscipopt
  ```

<!-- ### Installation-->

<!-- ### https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md-->


<!-- ERRORS -->
## Exceed Resource Limits 
If the Streamlit app has gone over the resource limits of Streamlit Community Cloud, access to the website will be temporarily restrcited. A few possible solutions:
* Reboot the app to clear the memory.
* Upgrade the Streamlit version of the app to the latest release.
* Optimize memory usage of the app, refers to these [tips](https://docs.streamlit.io/streamlit-community-cloud/manage-your-app#app-resources-and-limits "Manage your app resources and limits").

## Script errors
  ```ruby
  AttributeError: 'DeckGLWidget' object has no attribute 'm'
  ```
If you encounter this error while running the repository locally, the quick and dirty fix is to comment out **@st.cache_data** right above the function **generate_pydeck** in 1_Phase_1_Suitability Analysis.py. The long-term fix is not yet found. 

<!-- 
## File Descriptions
<details>
<summary>Data processing notebooks</summary>
<br>
This is how you dropdown.
</details>

<details>
<summary>Web app notebooks</summary>
<br>
Home.py
</details>
-->
