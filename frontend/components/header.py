import streamlit as st


def render_header():

    st.markdown(
        """
        <div class='title'>
                    AI Thumbnail Generator
                </div>

                <div class='subtitle'>
                    Generate YouTube Thumbnails using AI
                </div>
        """,
        unsafe_allow_html = True
    )