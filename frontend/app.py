import streamlit as st

from api.client import (
    upload_headshot,
    create_job
)

from api.sse_client import listen_to_job


st.set_page_config(
    page_title="AI Thumbnail Generator",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 AI Thumbnail Generator")

uploaded_file = st.file_uploader(
    "Upload Headshot",
    type=["jpg", "jpeg", "png"]
)

prompt = st.text_area(
    "Thumbnail Prompt",
    height=120
)

num_thumbnails = st.selectbox(
    "Number of Variations",
    [1, 2, 3]
)

generate = st.button(
    "Generate Thumbnails",
    use_container_width=True
)

if generate:

    if uploaded_file is None:
        st.error("Please upload a headshot")
        st.stop()

    if not prompt.strip():
        st.error("Please enter a prompt")
        st.stop()

    try:

        with st.spinner("Uploading headshot..."):

            upload_result = upload_headshot(
                uploaded_file
            )

        with st.spinner("Creating generation job..."):

            job = create_job(
                prompt=prompt,
                num_thumbnails=num_thumbnails,
                headshot_url=upload_result["url"]
            )

        job_id = job["job_id"]

        st.success(f"Job Created: {job_id}")

        status_placeholder = st.empty()

        thumbnail_container = st.container()

        with thumbnail_container:

            cols = st.columns(3)

        image_count = 0

        for message in listen_to_job(job_id):

            event = message["event"]
            data = message["data"]

            if event == "thumbnail_ready":

                image_count += 1

                status_placeholder.info(
                    f"Generated {image_count}/{num_thumbnails}"
                )

                with cols[(image_count - 1) % 3]:

                    st.image(
                        data["imageKit_url"],
                        caption=data["style_name"],
                        use_container_width=True
                    )

                    variants = data.get("variants", {})

                    for name, url in variants.items():

                        st.link_button(
                            label=name,
                            url=url,
                            use_container_width=True
                        )

            elif event == "thumbnail_failed":

                st.error(
                    f"{data['style_name']} failed: "
                    f"{data.get('error', 'Unknown Error')}"
                )

            elif event == "job_completed":

                status_placeholder.success(
                    "🎉 Generation Completed"
                )

                break

    except Exception as e:

        st.exception(e)