# Demand Planning Tool (DPT)

### Overview
The Demand Planning Tool (DPT) is a Minimum Viable Product (MVP) of a web application aimed at providing sales predictions and data visualization capabilities. DPT allows users to visualize sales analytics in order to make informed decisions.

### Features
1. **Sales Predictor:**
   - Input: Product ID (ASIN), Region.
   - Output: Sales predictions using a pre-trained LSTM model.
   
2. **Data Analytics:**
   - Customizable reports based on data from the company's data warehouse.
   - Accessible insights for understanding of the sales patterns' bigger picture.

### Getting Started

#### Prerequisites
- **Python 3.7+**
- **Streamlit 1.6+**
- **Snowflake Connector for Python**
- **Access to Snowflake Database:** Ensure that you have the necessary credentials and permissions to access the Snowflake database.

#### Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/your-username/demand-planning-tool.git
    cd demand-planning-tool
    ```

2. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure Snowflake Connection:**
   Add your Snowflake configuration in `db_connector.py`, ensuring your credentials and connection details are correctly set.

    ```python
    def get_snowflake_connection(user, password):
        return snowflake.connector.connect(
            user=user,
            password=password,
            account='YOUR_ACCOUNT',
            warehouse='YOUR_WAREHOUSE',
            database='YOUR_DATABASE',
            schema='YOUR_SCHEMA'
        )
    ```

4. **Run the Application:**
    ```sh
    streamlit run app.py
    ```

### Usage

1. **Log in:**
   - Enter your Snowflake username and password to log in.

2. **Navigate:**
   - Use the sidebar to navigate between the Home, Forecasting, and Analytics pages.

3. **Forecasting:**
   - Enter a valid ASIN and select a Region to generate sales forecasts.

4. **Analytics:**
   - Choose from available reports to visualize data and gain insights.