import streamlit as st
def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background:linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); padding:32px; border-radius: 16px; border: 1px solid #E2E8F0; margin-bottom:24px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
        <h3 style="margin:0; color: #0F172A; font-size: 1.35rem; line-height:1.4; font-weight:700;">{name}</h3>
        <p style="color:#475569; margin:12px 0 16px 0; font-size:0.95rem;">Code: <span style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:#FFFFFF; padding:6px 12px; border-radius:8px; font-weight:600; font-size:0.85rem;">{code}</span> <span style="color:#CBD5E1; padding:0 8px;">|</span> Section: {section}</p>

        """

    if stats:
        html+= """
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
        """
        for icon, label, value in stats:
            html+= f'<div style="background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%); color:#0F172A; border:1px solid #CBD5E1; padding:8px 16px; border-radius:20px; font-size:0.85rem; font-weight:600;">{icon} <b>{value}</b> {label}</div>'

        html+= "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
