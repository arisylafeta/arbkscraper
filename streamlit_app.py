import streamlit as st
import pandas as pd
from scraper import Scraper

st.set_page_config(page_title="ARBK Business Scraper", layout="wide")

st.title("ARBK Business Scraper")

# Input fields
col1, col2 = st.columns(2)

with col1:
    url = st.text_input("Enter URL:", "https://arbk.rks-gov.net")
    trade_number = st.text_input("Enter Trade Number:", placeholder="Enter the trade activity code")
    max_workers = st.slider("Number of concurrent workers", min_value=1, max_value=5, value=3)

with col2:
    debug_mode = st.checkbox("Debug Mode (limit number of records)", value=True)
    if debug_mode:
        num_records = st.number_input("Number of records to scrape:", min_value=1, value=5)
    else:
        num_records = None

# Add a submit button
if st.button("Start Scraping"):
    if url and trade_number:
        try:
            scraper = Scraper(url, max_workers=max_workers)
            
            # Get business numbers using trade number
            with st.spinner('Fetching business numbers...'):
                business_numbers = scraper.getNUI(trade_number)
                
                if business_numbers:
                    total_found = len(business_numbers)
                    
                    # Apply debug limit if needed
                    if debug_mode and num_records:
                        nui_list = business_numbers[:num_records]
                        st.info(f"Debug Mode: Found {total_found} businesses, processing first {num_records}")
                    else:
                        nui_list = business_numbers
                        st.info(f"Found {total_found} businesses to process")
                    
                    # Scrape business details concurrently
                    with st.spinner('Scraping business details...'):
                        results = scraper.scrape_batch(nui_list)
                        
                        if results:
                            # Convert results to DataFrame
                            df = pd.DataFrame(results, columns=['Name', 'Business Number', 'Status', 'Address', 'Phone', 'Email'])
                            st.success(f"Scraping completed! Found details for {len(results)} businesses")
                            st.dataframe(df)
                            
                            # Add download button
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                "Download Results as CSV",
                                csv,
                                f"trade_{trade_number}_results.csv",
                                "text/csv",
                                key='download-csv'
                            )
                        else:
                            st.warning("No business details could be scraped")
                else:
                    st.warning(f"No businesses found for trade number {trade_number}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter both URL and Trade Number")

# Help section
with st.expander("Help"):
    st.markdown("""
    ### How to use:
    1. Enter the URL (default is https://arbk.rks-gov.net)
    2. Enter the Trade Number (activity code)
    3. Adjust number of concurrent workers (1-5)
    4. Optional: Enable debug mode to limit the number of records processed
    5. Click 'Start Scraping'
    
    ### Concurrent Processing:
    - More workers = faster scraping but more resource intensive
    - Default is 3 workers, adjust based on your system's capabilities
    
    ### Debug Mode:
    - When enabled, you can specify how many records to process
    - Useful for testing without processing all records
    
    ### Note:
    The trade number is used to search for business activities in the system.
    """)
