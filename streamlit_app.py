import streamlit as st
from main import Scraper
import pandas as pd

st.set_page_config(page_title="Web Scraper Interface", layout="wide")

st.title("Web Scraper Interface")

# Input fields
url = st.text_input("Enter URL to scrape:", "https://arbk.rks-gov.net")
nui_file = st.text_input("Enter NUI file path (optional):", "")
max_workers = st.slider("Number of concurrent workers", min_value=1, max_value=5, value=3)

# Add a submit button
if st.button("Start Scraping"):
    if url:
        try:
            scraper = Scraper(url, max_workers=max_workers)
            with st.spinner('Scraping in progress...'):
                # If NUI file is provided, use it
                if nui_file:
                    from helper import getNUI
                    nui_list = getNUI(nui_file)
                    results = scraper.scrape_batch(nui_list)
                    
                    # Convert results to DataFrame for better display
                    if results:
                        df = pd.DataFrame(results, columns=['Name', 'Business Number', 'Status', 'Address', 'Phone', 'Email'])
                        st.success(f"Scraping completed successfully! Found {len(results)} results.")
                        st.dataframe(df)
                        
                        # Add download button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Download Results as CSV",
                            csv,
                            "scraping_results.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    else:
                        st.warning("No results found")
                else:
                    st.error("Please provide a NUI file path")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a URL to scrape")

# Add some helpful information
with st.expander("Help"):
    st.markdown("""
    ### How to use this scraper:
    1. Enter the URL you want to scrape (default is https://arbk.rks-gov.net)
    2. Provide the NUI file path containing the business numbers to scrape
    3. Adjust the number of concurrent workers (1-5)
    4. Click 'Start Scraping' to begin
    
    ### Notes:
    - More workers = faster scraping, but might be more resource-intensive
    - The scraper uses Chrome in headless mode
    - Results can be downloaded as a CSV file
    - Each worker uses its own browser instance
    """)
