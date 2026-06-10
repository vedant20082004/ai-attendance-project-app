import streamlit as st


def header_home():
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin:32px 0 40px 0;">
            <img src='https://i.ibb.co/S7rVHvMQ/ITM-UNIVERSITY-GWALIOR1676871946-upload-logo.png' style='height:80px; width:auto; object-fit:contain; filter: drop-shadow(0 2px 8px rgba(15, 23, 42, 0.1));' />
        </div>

                """, unsafe_allow_html=True)


def header_dashboard():
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px; padding:8px 0;">
            <img src='https://i.ibb.co/S7rVHvMQ/ITM-UNIVERSITY-GWALIOR1676871946-upload-logo.png' style='height:64px; width:auto; object-fit:contain;' />
        </div>

                """, unsafe_allow_html=True)
