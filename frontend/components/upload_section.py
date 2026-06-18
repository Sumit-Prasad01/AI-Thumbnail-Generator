import streamlit as st


def render_upload_section():

    upload_file = st.file_uploader(
        "Upload Headshot",
        type = ["png"]
    )

    prompt = st.text_area(
        "Thumbnail Prompt",
        height = 120
    )

    num_thumbnails = st.selectbox(
        "Number of Variations",
        [1, 2, 3]
    )

    generate = st.button(
        "Generate Thumbnails",
        use_container_width = True
    )

    return (
        upload_file,
        prompt,
        num_thumbnails,
        generate
    )