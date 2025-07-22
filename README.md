# Load Forecasting for Green Field Cities

## 🏙️ Energy Grid Optimization for Smart Urban Development

This project implements a machine learning-driven approach for electricity load forecasting specifically designed for green field cities like GIFT City, Gujarat. The solution helps optimize energy grid development and infrastructure planning for smart urban environments.

## 🎯 Project Overview

Green field cities face unique challenges in energy grid development due to:
- Lack of historical consumption data
- Rapid infrastructure development
- Smart city features affecting traditional consumption patterns
- Need for optimal resource allocation

Our ML-based solution addresses these challenges by leveraging regional data patterns and specialized feature engineering.

## 🚀 Key Features

- **Data Integration**: CEA API compatibility for real-time data access
- **Smart City Modeling**: Accounts for efficiency improvements and renewable integration
- **Lightweight ML Models**: Fast, accurate models suitable for real-time applications
- **Grid Planning Insights**: Actionable recommendations for infrastructure development
- **Google Colab Ready**: Optimized for cloud-based execution

## 📊 Technical Approach

### Data Sources
- Central Electricity Authority (CEA) API
- State-level electricity consumption patterns
- Weather and demographic indicators
- Smart city efficiency factors

### Machine Learning Pipeline
1. **Data Preprocessing**: Cleaning, outlier removal, feature scaling
2. **Feature Engineering**: Time-based, lag, and green field city-specific features
3. **Model Training**: Random Forest, XGBoost, and Linear Regression
4. **Evaluation**: Comprehensive metrics and validation
5. **Grid Planning**: Infrastructure sizing and capacity recommendations

### Models Implemented
- **Random Forest**: Fast, interpretable ensemble method
- **XGBoost**: High-accuracy gradient boosting
- **Linear Regression**: Baseline model for comparison

## 🛠️ Installation & Usage

### Google Colab (Recommended)
1. Open the notebook in Google Colab
2. Run all cells sequentially
3. All required packages will be automatically installed

### Local Environment
```bash
git clone https://github.com/chintanlad10/Load-forecasting.git
cd Load-forecasting
pip install -r requirements.txt
jupyter notebook gujarat_load_forecasting.ipynb
```

## 📈 Results

Our lightweight ML models achieve:
- **94.2% prediction accuracy** with MAPE of 5.78%
- **Best Model**: Linear Regression (RMSE: 45.29)
- **Real-time performance** suitable for operational forecasting
- **Scalable methodology** adaptable to any green field city
- **Comprehensive grid planning insights** for infrastructure development

### Key Performance Metrics
- **Peak Demand Forecasted**: 1321.3 MW
- **Recommended Grid Capacity**: 1651.6 MW
- **Growth Rate Identified**: 16.2% annually
- **Smart City Efficiency**: 15% energy savings

## 🏗️ Applications

### GIFT City, Gujarat Case Study
- Phase-based development modeling
- Optimal transformer and distribution sizing
- Smart grid integration strategies
- Real-time load management

### Adaptable to Other Cities
- Amaravathi, Andhra Pradesh
- Dholera Smart City, Gujarat
- Any planned urban development

## 🔮 Future Enhancements

1. **Real-time Data Integration**: Live CEA API connections
2. **IoT Sensor Integration**: Smart meter and environmental data
3. **Advanced ML Models**: Deep learning for complex patterns
4. **Multi-city Analysis**: Comparative studies across different cities
5. **Economic Impact Modeling**: Cost-benefit analysis tools

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Model improvements
- Additional data sources
- New city case studies
- Documentation enhancements

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Chintan Lad**
- GitHub: [@chintanlad10](https://github.com/chintanlad10)
- Project: Capstone Project - ML-driven Energy Grid Planning for Smart Cities

## 🙏 Acknowledgments

- Central Electricity Authority (CEA) for electricity consumption data framework
- GIFT City, Gujarat for serving as the case study location
- Open source ML libraries (scikit-learn, XGBoost, pandas) that made this project possible
