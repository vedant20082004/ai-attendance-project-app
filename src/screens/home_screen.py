import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
def home_screen():


    header_home()
    style_background_home()
    style_base_layout()


    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<h2 style="margin:0; color: #0F172A; font-size: 1.75rem; font-weight:700; margin-bottom:0.5rem;">Student Portal</h2>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin: 1.5rem 0;"><img src="https://i.ibb.co/844D9Lrt/mascot-student.png" style="width:100px; height:auto;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#334155; margin-bottom:1.5rem; font-size:0.95rem; line-height:1.6;">Access your dashboard, view enrolled subjects, and check attendance records.</p>', unsafe_allow_html=True)
        if st.button('Enter Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', width='stretch'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.markdown('<h2 style="margin:0; color: #0F172A; font-size: 1.75rem; font-weight:700; margin-bottom:0.5rem;">Teacher Portal</h2>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin: 1.5rem 0;"><img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" style="width:120px; height:auto;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#334155; margin-bottom:1.5rem; font-size:0.95rem; line-height:1.6;">Manage subjects, take attendance using AI, and view class records.</p>', unsafe_allow_html=True)
        if st.button('Enter Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', width='stretch'):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()