# sahl-delivery-analytics
Food delivery operations analytics project: data preprocessing, feature engineering, and a 6-panel Seaborn insights dashboard.

🛵 Sahl Delivery: Operational Analytics & Performance Dashboard
An end-to-end data cleaning, feature engineering, and exploratory data analysis (EDA) project analyzing food delivery bottlenecks, courier performance, and their direct impact on customer retention.

📊 Project Overview
In the fast-paced food delivery industry, operational delays directly destroy customer lifetime value. This project processes a messy, real-world delivery dataset to uncover root causes for delivery delays—such as courier vehicle constraints, peak-hour kitchen bottlenecks, and zone-specific discrepancies—and visualizes how these delays affect 30-day customer reorder rates.

🛠️ Tech Stack & Libraries
Language: Python

Data Manipulation & Cleaning: Pandas, NumPy

Data Visualization: Seaborn, Matplotlib

🧹 Data Cleaning & Preprocessing Highlights
Real-world data is messy. The data pipeline in Sahl_Delivery_MohamedHesham.py implements rigorous cleaning steps to ensure data integrity:

Duplicate & Sparse Removal: Automatically drops duplicate rows and eliminates columns with over 90% missing values.

Type Casting & Sanitization: Cleans string-stored numeric columns (like order_value_egp) using Regex to strip non-numeric characters and coerce data types.

Standardizing Categorical Data: Normalizes inconsistent text entries across zones and cities (e.g., merging spelling variations like Abu-Qurqas and Aboo Qurqas into Abu Qurqas).

Mixed Date Parsing: Handles dual date-time formats within the same column seamlessly.

Anomaly Filtering: Drops physically impossible records (e.g., negative/zero distances, preparation times, or actual delivery durations).

Smart Imputation: Imputes missing numeric values using column medians while intentionally leaving customer ratings blank to prevent analytical bias.

📈 Key Insights & Dashboard Overview
The script generates a 6-panel analytical dashboard (sahl_dashboard.png) that highlights critical operational takeaways:

Retention Cliff: Customer reorder rates within 30 days drop sharply once delivery delays exceed 10 minutes.

Vehicle Limitations: Bicycles experience severe performance bottlenecks and delay spikes on distances exceeding 3 km.

Peak-Hour Strain: Average delivery delays peak dramatically during the dinner rush window (18:00 – 22:00).

Kitchen Prep Bottlenecks: Analysis of preparation times highlights specific cuisines driving kitchen-side delays.

Rating Correlation: Unrated orders exhibit distinct delay characteristics compared to rated orders.
