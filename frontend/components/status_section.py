import streamlit as st

def render_status(message):

    st.markdown(
        f"""
        <div class='status-card'>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

    