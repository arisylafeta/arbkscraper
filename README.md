# ARBK Business Scraper 🔍

A modern web scraper for the Kosovo Business Registration Agency (ARBK) with a Streamlit interface. This tool allows you to efficiently fetch and analyze business data using trade activity codes.

## 🌟 Features

- **Interactive Streamlit Interface**: User-friendly web interface for easy data collection
- **Concurrent Scraping**: Multi-threaded scraping for improved performance
- **Debug Mode**: Test functionality with limited records
- **Export Capability**: Download results as CSV files
- **Customizable Workers**: Adjust concurrent workers based on your system's capabilities

## 🚀 Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

3. Enter the required information:
   - ARBK URL (default: https://arbk.rks-gov.net)
   - Trade activity code
   - Number of concurrent workers (1-5)
   - Optional: Enable debug mode to limit records

## 📊 Data Extracted

For each business, the scraper collects:
- Business Name
- Business Number (NUI)
- Status
- Address
- Phone Number
- Email

## ⚙️ Configuration

- **Concurrent Workers**: Default is 3, adjustable through the UI (1-5)
- **Debug Mode**: Limit the number of records for testing
- **Headless Mode**: Chrome runs in headless mode for better performance

## 🛠️ Technical Details

Built with:
- Python 3.x
- Streamlit
- Selenium WebDriver
- BeautifulSoup4
- ChromeDriver (automatically managed)
- Concurrent Futures for parallel processing

## 📝 Notes

- The scraper implements reasonable delays and concurrent request limiting
- No explicit robots.txt rules are in place, but the tool maintains respectful scraping practices
- Consider rate limiting for large-scale scraping

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements!
