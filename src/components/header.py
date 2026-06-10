import streamlit as st


def header_home():
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
            <img src='https://i.ibb.co/S7rVHvMQ/ITM-UNIVERSITY-GWALIOR1676871946-upload-logo.png' style='height:100px;' />
        </div>   
                
                """, unsafe_allow_html=True)


def header_dashboard():
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px">
            <img src='https://i.ibb.co/S7rVHvMQ/ITM-UNIVERSITY-GWALIOR1676871946-upload-logo.png' style='height:85px;' />
        </div>   
                
                """, unsafe_allow_html=True)
