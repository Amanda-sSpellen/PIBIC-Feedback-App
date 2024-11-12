import streamlit as st

def inject_custom_css():
    # Lê o arquivo CSS e injeta no Streamlit
    with open("assets/styles/custom.css") as css_file:
        css = css_file.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
