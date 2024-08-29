# Demand Plan Tool (DPT)

## Overview
The Demand Plan Tool (DPT) is a web application that aims to provide sales predictions and data visualization capabilities. DPT is developed as an internal tool that allows non-technical users of an e-commerce aggregator company to visualize sales analytics in order to make informed decisions for their company.

---

## Features
1. **Forecasting:**
   - <u>Input</u>: Product ID (ASIN), Region.
   - <u>Output</u>: Sales predictions for the upcoming 6 months using a pre-trained LSTM model.
   
2. **Data Analytics:**
   - Customizable reports based on historical data from the company's Snowflake database.
   - Accessible insights for understanding of the sales patterns' bigger picture.

---

## Getting Started

### Prerequisites
- **Python 3.7+**
- **Streamlit 1.6+**
- **Snowflake Connector for Python**
- **Access to Snowflake Database:** Ensure that you have the necessary credentials and permissions to access the Snowflake database.

### Installation

1. **Clone the Repository and navigate to the project:**
    ```sh
    git clone https://github.com/printlaura/demand-planning-tool.git
    cd demand-planning-tool
    ```
2. **Create a Virtual Environment:** 
   ```sh
   # macOS/Linux 
   python3 -m venv venv
   
   # Windows
   python -m venv venv
    ```
3. **Activate the Virtual Environment:**
   ```sh
   # macOS/Linux 
   source venv/bin/activate
   
   # Windows
   .\venv\Scripts\activate
    ```
3. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Create a new .env file in the project directory and add the following variables:**
    ```sh
    SNOWFLAKE_ACCOUNT='your_snowflake_account'
   SNOWFLAKE_WAREHOUSE='your_snowflake_warehouse'
   SNOWFLAKE_DATABASE='your_snowflake_database'
   SNOWFLAKE_SCHEMA='your_snowflake_schema'
    ```
   
4. **Configure Snowflake Connection:**
   Add your Snowflake configuration in `db_connector.py`, ensuring your connection details are correctly set.

    ```python
    def get_snowflake_connection(user, password):
        return snowflake.connector.connect(
            user=user,
            password=password,
            account='SNOWFLAKE_ACCOUNT',
            warehouse='SNOWFLAKE_WAREHOUSE',
            database='SNOWFLAKE_DATABASE',
            schema='SNOWFLAKE_SCHEMA'
        )
    ```
   Your user and password credentials are the same ones you will need to log into the application, and will be automatically passed to the snowflake connector once logged in.


4. **Run the Application:**
    ```sh
    streamlit run app.py
    ```
4. **Acces the Application locally at:** `http://localhost:8501//`


- **Log in:** Enter your Snowflake username and password to log in.

- **Navigate:** Use the sidebar to navigate between the Home, Forecasting, and Analytics pages.

- **Forecasting:** Enter an ASIN and select a Region to generate sales forecasts.

- **Analytics:** Choose from available reports to visualize data and gain insights.

---

### Running Security Audit

To ensure that your Python dependencies are secure, you can use the `pip-audit` tool. This tool checks for known vulnerabilities in your dependencies.

#### Installation

First, install the `pip-audit` tool:

```sh
pip install pip-audit
  ```

To automatically upgrade insecure packages to fixed and non-vulnerable versions, run:
```sh
pip-audit -r requirements.txt
  ```

---
### Deployment Workflow with Streamlit Cloud

1. **Prerequisite:** An account on Streamlit Community Cloud: [Streamlit Cloud](https://share.streamlit.io/)
2. **Streamlit Cloud Configuration:** Navigate to Streamlit Cloud log in and link your GitHub repository.
3. **Secret keys:** Save your Environmental Variables on your repository secrets.
4. **Automatic Deployment:** The deployment process is automatically triggered when you push changes to `master` branch.
5. **Automated Testing:** Every time a new deployment is triggered, the tests saved in `tests/` directory will be run.

