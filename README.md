\# E-Commerce Customer Analytics



A data analytics project focused on understanding e-commerce customer behavior, evaluating purchasing patterns, and identifying customer segments through data processing, analytics, and interactive visualization.



\## Overview



E-commerce platforms generate large volumes of transactional data that can reveal valuable insights into customer preferences, purchasing frequency, spending behavior, and customer retention.



This project explores these patterns using a data analytics pipeline that combines big data processing, customer analytics, database technologies, and an interactive dashboard. It aims to transform raw transactional data into meaningful insights that support data-driven business decisions.



\## Objectives



\- Analyze customer purchasing behavior and transaction patterns.

\- Calculate Recency, Frequency, and Monetary (RFM) metrics.

\- Segment customers based on purchasing characteristics.

\- Process and prepare e-commerce data for analysis.

\- Integrate analytical workflows with database technologies.

\- Visualize customer and purchase analytics through an interactive dashboard.



\## Key Features



\- \*\*Data preprocessing:\*\* Prepare and transform transactional datasets for analysis.

\- \*\*Customer purchase analytics:\*\* Explore customer-level purchasing behavior and order patterns.

\- \*\*RFM analysis:\*\* Evaluate customers using recency, purchase frequency, and monetary value.

\- \*\*Customer segmentation:\*\* Apply clustering techniques to identify groups of customers with similar characteristics.

\- \*\*Data quality analysis:\*\* Inspect and validate data used in analytical workflows.

\- \*\*Database integration:\*\* Use MongoDB and Apache Cassandra for supported data storage and retrieval operations.

\- \*\*Interactive dashboard:\*\* Explore analytical metrics and customer segments through a Streamlit dashboard.



\## Technology Stack



| Technology | Application |

|---|---|

| Python | Core programming and analytics |

| Apache Spark / PySpark | Data processing |

| Pandas | Data manipulation and analysis |

| Scikit-learn | Customer clustering and model evaluation |

| MongoDB | Document-oriented data storage |

| Apache Cassandra | Distributed database storage |

| Streamlit | Interactive dashboard |

| Plotly | Interactive data visualization |



\## System Workflow



```text

E-Commerce Transaction Data

&#x20;          |

&#x20;          v

&#x20;  Data Preprocessing

&#x20;          |

&#x20;          v

&#x20;Data Quality Validation

&#x20;          |

&#x20;          v

&#x20;Customer-Level Data Preparation

&#x20;          |

&#x20;          v

&#x20;  RFM Feature Engineering

&#x20;          |

&#x20;          v

&#x20;   Customer Segmentation

&#x20;          |

&#x20;          v

&#x20;Analytical Results and Metrics

&#x20;          |

&#x20;          v

&#x20;   Streamlit Dashboard

```



The project includes separate scripts for data preparation, customer analytics, segmentation, and database operations. The dashboard provides a visual interface for exploring the supported analytical results.



\## Project Structure



```text

ECommerceAnalytics/

├── dashboard/

│   └── app.py

├── scripts/

│   ├── build\_rfm.py

│   ├── cluster\_customers.py

│   ├── customer\_purchase\_analytics.py

│   ├── data\_quality\_check.py

│   ├── preprocess\_orders.py

│   ├── preprocess\_items\_payments.py

│   ├── load\_customers\_mongodb.py

│   ├── load\_orders\_cassandra.py

│   └── ...

├── src/

│   ├── analytics/

│   ├── config/

│   ├── ingestion/

│   ├── processing/

│   ├── storage/

│   └── utils/

├── tests/

├── requirements.txt

├── .gitignore

└── README.md

```



\## Dataset



The project is based on the Brazilian E-Commerce Public Dataset by Olist. The dataset contains e-commerce transaction-related information used to study customer purchases and order behavior.



Dataset source: \[Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)



Raw datasets and locally generated processing outputs are maintained separately from the source repository.



\## Dashboard



The Streamlit dashboard brings the project's analytical outputs together in an interactive interface for exploring customer behavior, purchase metrics, and segmentation results.



\## Project Goals



This project demonstrates the application of data engineering and analytics concepts to an e-commerce use case, bringing together data preparation, customer-level feature engineering, clustering, database integration, and visualization in one workflow.



