# 📊 Marketing Intelligence Dashboard

A comprehensive Streamlit-based dashboard for analyzing marketing performance across multiple channels (Facebook, Google, TikTok) and connecting marketing spend to business outcomes.

## 🎯 Project Overview

This dashboard helps marketing teams and business stakeholders understand:
- **Marketing Performance**: ROAS, CTR, CPC, CPM across platforms
- **Business Impact**: Revenue attribution, profit margins, customer acquisition
- **Attribution Analysis**: Gap between attributed and total revenue
- **Platform Comparison**: Performance differences across channels
- **Trend Analysis**: Daily/weekly performance patterns

## 📁 Project Structure

```
Assessment1/
├── dataset/
│   ├── business.csv          # Daily business metrics
│   ├── Facebook.csv          # Facebook campaign data
│   ├── Google.csv            # Google campaign data
│   └── TikTok.csv            # TikTok campaign data
├── src/
│   ├── data/
│   │   └── data_processor.py # Data loading and processing
│   └── visualization/
│       └── dashboard_components.py # Chart components
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── LLM_INTEGRATION_GUIDE.md  # Guide for AI/LLM integration
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
└── README.md                # This file
```

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Dashboard**
```bash
streamlit run app.py
```

### **3. Access Dashboard**
Open your browser to `http://localhost:8501`

## 📊 Key Features

### **Dashboard Sections:**
1. **📈 KPI Overview**: Key performance indicators and summary metrics
2. **📊 Revenue Trends**: Business vs attributed revenue comparison
3. **🎯 Platform Analysis**: Channel performance comparison
4. **💡 AI Insights**: Automated insights and recommendations

### **Interactive Features:**
- Date range filtering
- Platform selection
- Real-time data processing
- Responsive design
- Export capabilities
- **🤖 AI-Powered Insights**: Automated analysis and recommendations
- **💬 AI Chat Interface**: Natural language queries about your data

### **Metrics Calculated:**
- **Marketing KPIs**: CTR, CPC, CPM, ROAS
- **Business KPIs**: AOV, Profit Margin, New Customer Rate
- **Attribution Metrics**: Attribution gap analysis
- **Performance Indicators**: Platform efficiency metrics

## 🤖 AI Integration

This dashboard includes **full AI integration** with support for multiple LLM providers:

### **AI Features:**
- **🤖 Automated Insights**: AI analyzes your data and provides intelligent recommendations
- **💬 Natural Language Chat**: Ask questions about your marketing performance in plain English
- **📊 Smart Recommendations**: Get strategic advice on budget allocation, campaign optimization, and attribution
- **📋 Executive Summaries**: AI-generated reports for stakeholders

### **Supported AI Providers:**
- **OpenAI** (GPT-3.5, GPT-4)
- **Google Gemini** (Gemini Pro)
- **Anthropic** (Claude 3)

### **Setup:**
1. **Quick Start**: Works out of the box with mock AI responses
2. **Real AI**: Add API keys for live AI insights (see `AI_SETUP_GUIDE.md`)

See `AI_SETUP_GUIDE.md` for detailed setup instructions.

## 🚀 Deployment Options

Multiple deployment options are supported:
- **Streamlit Cloud** (Recommended)
- **Heroku**
- **AWS EC2**
- **Docker**

See `DEPLOYMENT_GUIDE.md` for step-by-step instructions.

## 📈 Data Structure

### **Business Data (`business.csv`)**
- Daily business metrics for 121 days
- Columns: date, orders, new_orders, new_customers, total_revenue, gross_profit, COGS

### **Marketing Data (`Facebook.csv`, `Google.csv`, `TikTok.csv`)**
- Campaign-level performance data
- Columns: date, tactic, state, campaign, impressions, clicks, spend, attributed_revenue
- Multiple tactics: ASC, Prospecting, Retargeting, Spark Ads
- States: NY, CA

## 🔧 Technical Architecture

### **Data Processing Pipeline:**
1. **Data Loading**: Load and validate CSV files
2. **Data Cleaning**: Standardize formats and handle missing values
3. **KPI Calculation**: Compute marketing and business metrics
4. **Data Combination**: Merge marketing and business data by date
5. **Caching**: Optimize performance with Streamlit caching

### **Visualization Components:**
- **Plotly Charts**: Interactive, responsive visualizations
- **Metric Cards**: Key performance indicators
- **Trend Analysis**: Time-series performance tracking
- **Comparison Views**: Platform and campaign analysis

## 📊 Sample Insights

The dashboard automatically generates insights such as:
- Overall ROAS performance across platforms
- Attribution gap analysis
- Best/worst performing channels
- Optimization recommendations
- Strategic action items

## 🛠 Customization

### **Adding New Metrics:**
1. Update `data_processor.py` to calculate new KPIs
2. Add visualization components in `dashboard_components.py`
3. Integrate into main dashboard in `app.py`

### **Adding New Data Sources:**
1. Extend `DataProcessor.load_data()` method
2. Update data cleaning and processing logic
3. Add platform-specific visualizations

## 🔒 Security & Privacy

- No sensitive customer data is exposed
- All data processing is done locally
- Optional authentication can be added
- Environment variables for secure configuration

## 📞 Support & Resources

### **Documentation:**
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### **Community:**
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/your-repo/issues)

## 🎯 Use Cases

### **For Marketing Teams:**
- Monitor campaign performance across platforms
- Identify high-performing campaigns and tactics
- Optimize budget allocation based on ROAS
- Track attribution and conversion metrics

### **For Business Stakeholders:**
- Understand marketing ROI and business impact
- Monitor revenue trends and profit margins
- Identify optimization opportunities
- Make data-driven marketing decisions

### **For Data Analysts:**
- Access comprehensive marketing and business data
- Perform advanced analytics and modeling
- Create custom reports and visualizations
- Integrate with external data sources

## 🚀 Future Enhancements

- **Real-time Data Integration**: Connect to live data sources
- **Advanced Analytics**: Machine learning models for prediction
- **Custom Reporting**: Automated report generation
- **Mobile Optimization**: Enhanced mobile experience
- **API Integration**: Connect to external marketing platforms

## 📄 License

This project is part of a marketing intelligence assessment and is intended for educational and demonstration purposes.

---

**Built with ❤️ using Streamlit, Pandas, and Plotly**

*For questions or support, please refer to the documentation or create an issue in the repository.*
