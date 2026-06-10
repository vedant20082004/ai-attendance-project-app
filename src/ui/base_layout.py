import streamlit as st



def style_background_home():

    st.markdown("""
        <style>
            .stApp {
                background:
                    linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            }

            .stApp div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.98) !important;
                border: 1px solid rgba(255, 255, 255, 0.6) !important;
                border-radius: 20px !important;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
                padding: 3rem !important;
                backdrop-filter: blur(10px) !important;
            }

            .stApp div[data-testid="stColumn"] img {
                margin: 1.5rem auto 2rem auto;
                display: block;
            }
        </style>

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>
            .stApp {
                background:
                    linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
            }

        </style>

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            :root {
                --brand-primary: #6366F1;
                --brand-primary-dark: #4F46E5;
                --brand-secondary: #64748B;
                --brand-tertiary: #F1F5F9;
                --ink: #0F172A;
                --muted: #475569;
                --surface: #FFFFFF;
                --surface-soft: #F8FAFC;
                --border: #E2E8F0;
                --shadow-soft: 0 1px 3px rgba(0, 0, 0, 0.1);
                --shadow-medium: 0 4px 6px rgba(0, 0, 0, 0.05);
            }

            /* Hide Top Bar of streamlit */
            #MainMenu, footer, header {
                visibility: hidden;
            }

            .block-container {
                max-width: 1120px;
                padding-top: 3rem !important;
                padding-bottom: 3rem !important;
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2.5rem !important;
                line-height: 1.2 !important;
                margin-bottom: 0.5rem !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.02em !important;
            }


            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 1.75rem !important;
                line-height: 1.3 !important;
                margin-bottom: 0.5rem !important;
                color: var(--ink) !important;
                letter-spacing: -0.01em !important;
            }

            h3, h4, p, label, span, div {
                font-family: 'Outfit', sans-serif;
            }

            h3, h4 {
                color: var(--ink) !important;
            }

            p {
                color: var(--muted);
            }

            div[data-testid="stDivider"] {
                margin: 2rem 0 !important;
            }

            div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
                border-color: var(--border) !important;
                border-radius: 12px !important;
                box-shadow: var(--shadow-soft) !important;
                background: rgba(255, 255, 255, 0.9) !important;
            }

            div[data-testid="stDialog"] div[role="dialog"] {
                border-radius: 16px !important;
                border: 1px solid var(--border) !important;
                box-shadow: 0 10px 40px rgba(15, 23, 42, 0.1) !important;
            }

            div[data-testid="stAlert"] {
                border-radius: 8px !important;
                border: 1px solid var(--border) !important;
            }


            button{
                border-radius: 10px !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                padding: 0.85rem 1.75rem !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
                font-weight: 600 !important;
                }

            button[kind="secondary"]{
                background: linear-gradient(135deg, #64748B 0%, #475569 100%) !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(100, 116, 139, 0.3) !important;
                }

            button[kind="tertiary"]{
                background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%) !important;
                color: var(--ink) !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                }

            button:hover{
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
            }

            button[kind="secondary"]:hover{
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(100, 116, 139, 0.4) !important;
            }

            button[kind="tertiary"]:hover{
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }

            button:disabled,
            button[disabled] {
                background-color: #CBD5E1 !important;
                color: #94A3B8 !important;
                box-shadow: none !important;
            }

            input,
            textarea,
            div[data-baseweb="select"] > div,
            div[data-testid="stFileUploaderDropzone"],
            div[data-testid="stCameraInput"] section,
            div[data-testid="stAudioInput"] section {
                border-radius: 8px !important;
                border-color: var(--border) !important;
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }

            input:focus,
            textarea:focus,
            div[data-baseweb="select"] > div:focus-within {
                border-color: var(--brand-primary) !important;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
            }

            input::placeholder,
            textarea::placeholder {
                color: #94A3B8 !important;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 8px !important;
                overflow: hidden !important;
                box-shadow: var(--shadow-soft) !important;
                border: 1px solid var(--border) !important;
            }
        </style>

                """
            ,unsafe_allow_html=True)
