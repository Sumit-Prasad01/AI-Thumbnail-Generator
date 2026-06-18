import streamlit as st


def render_thumbnails(thumbnails):

    if not thumbnails:
        return 
    
    cols = st.columns()

    for idx, thumb in enumerate(thumbnails):

        with cols[idx % 3]:

            st.image(
                thumb["imageKit_url"],
                use_column_width = True
            )

            st.markdown(
                f"""
                <div class='style-name'>
                    {thumb["style_name"]}
                </div>
                """,
                unsafe_allow_html = True
            )

            variants = thumb.get("variants", {})

            for name, url in variants.items():

                st.link_button(
                    name,
                    url,
                    use_container_width = True
                )