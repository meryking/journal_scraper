import streamlit as st

def set_article_url(url_to_set):
    # This updates the state of the main text input
    st.session_state.user_url_input = url_to_set
    # Note: st.experimental_rerun() is often not needed inside the callback
    # as the button click and state change naturally trigger a rerun.

def create_sidebar_button(article):
    headline_tag = article.find('h2')
    link_tag = article.find('a', href=True)

    if link_tag and headline_tag:
        title = headline_tag.get_text(strip=True)
        href = link_tag.get('href', 'No Link Found')
               
        # Use st.link_button to create a clickable element that changes the URL query parameter.
        # This triggers a full app rerun with the new 'article_url', which is then read in Step 1.
        st.sidebar.button(
            label=title,
            help="Click to scrape",
            on_click=set_article_url,  # This function is called when the button is clicked
            args=(href,)
        )

# Function to print warning
def display_warning(current_url):
    """Display error and show current_url"""
    st.warning(
f"""**Oops! Something went wrong.**
Could it be that the article is not behind a paywall?\n
Try accessing it directly: [{current_url}]({current_url}).
""")