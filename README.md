# 🛒 E-Commerce Customer Analytics

An end-to-end data analytics project focused on understanding customer purchasing behavior, analyzing transaction patterns, and identifying customer segments using data processing, analytics, database technologies, and interactive visualization.

---

## 📌 Overview

E-commerce platforms generate large volumes of transactional data that can reveal valuable insights into customer preferences, purchasing frequency, spending behavior, and customer retention.

This project explores customer and order data through a data analytics workflow that combines data preprocessing, customer analytics, RFM analysis, customer segmentation, database integration, and an interactive dashboard.

The goal is to transform raw transactional data into meaningful insights that can support data-driven business decisions.

## 🎯 Objectives

- Analyze customer purchasing behavior and order patterns.
- Calculate Recency, Frequency, and Monetary (RFM) metrics.
- Identify customer segments based on purchasing characteristics.
- Prepare and validate transactional data for analysis.
- Explore database technologies for storing and retrieving analytical data.
- Present analytical metrics and customer insights through an interactive dashboard.

## ✨ Key Features

- **Data Preprocessing:** Clean, transform, and prepare transactional datasets.
- **Customer Purchase Analytics:** Analyze customer-level purchases and order patterns.
- **RFM Analysis:** Evaluate customers using recency, frequency, and monetary value.
- **Customer Segmentation:** Apply clustering techniques to group customers with similar characteristics.
- **Data Quality Analysis:** Inspect datasets and validate analytical inputs.
- **Database Integration:** Implement data storage and retrieval workflows using MongoDB and Apache Cassandra.
- **Interactive Dashboard:** Explore customer analytics and visualizations through Streamlit.
- **Data Visualization:** Present analytical results using interactive charts.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming and analytics |
| Apache Spark / PySpark | Data processing |
| Pandas | Data manipulation and analysis |
| Scikit-learn | Customer clustering and model evaluation |
| MongoDB | Document-oriented data storage |
| Apache Cassandra | Distributed database storage |
| Streamlit | Interactive dashboard |
| Plotly | Interactive data visualization |
| Git and GitHub | Version control and project hosting |

## 🔄 System Workflow

```text
        E-Commerce Transaction Data
                    |
                    v
           Data Preprocessing
                    |
                    v
          Data Quality Validation
                    |
                    v
       Customer-Level Data Preparation
                    |
                    v
          RFM Feature Engineering
                    |
                    v
          Customer Segmentation
                    |
                    v
       Analytical Results and Metrics
                    |
                    v
           Streamlit Dashboard
```

The repository contains separate scripts for preprocessing, customer analytics, segmentation, data validation, and database operations.

## 📂 Project Structure

```text
ECommerceAnalytics/
│
├── dashboard/
│   └── app.py
│
├── scripts/
│   ├── build_rfm.py
│   ├── cluster_customers.py
│   ├── customer_purchase_analytics.py
│   ├── data_quality_check.py
│   ├── preprocess_orders.py
│   ├── preprocess_items_payments.py
│   ├── load_customers_mongodb.py
│   ├── load_orders_cassandra.py
│   ├── setup_cassandra.py
│   ├── check_mongodb.py
│   ├── check_cassandra.py
│   └── ...
│
├── src/
│   ├── analytics/
│   ├── config/
│   ├── ingestion/
│   ├── processing/
│   ├── storage/
│   └── utils/
│
├── tests/
│
├── data/                 # Local datasets; not tracked by Git
├── requirements.txt
├── .gitignore
└── README.md
```

## 📊 Dataset

This project is based on the **Brazilian E-Commerce Public Dataset by Olist**, which contains information related to e-commerce orders and transactions.

Dataset source: [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Raw datasets and locally generated processing outputs are excluded from the source repository to keep it focused on code and documentation.

## 📈 Dashboard

The project includes a Streamlit dashboard designed to bring supported analytical outputs into an interactive interface.

It provides a visual way to explore customer behavior, purchasing metrics, and customer segmentation results.

**Dashboard technology:** Streamlit and Plotly.

## 💡 Project Goals

This project demonstrates the application of data engineering and analytics concepts to an e-commerce use case. It brings together data preparation, customer-level feature engineering, clustering, database operations, and visualization in a single project.

The project also provides practical experience in organizing Python analytics workflows and presenting results through an interactive dashboard.

