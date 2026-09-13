# construction-project-analytics
Construction Project Performance Analytics &amp; Decision Support System using Python, SQL and Power BI

📌 Project Overview

The Construction Project Performance Analytics & Decision Support System is a data-driven construction project management analytics project developed to monitor and evaluate the performance of a residential building project.

The system combines Python, SQL, Power BI, and Excel/CSV to transform construction project data into meaningful KPIs, performance insights, and an interactive management dashboard.

Key Areas

Cost performance

Schedule and progress monitoring

Earned Value Management (EVM)

Labour productivity

Material wastage

Quality performance

Equipment utilization

Activity-level delay analysis

🏗️ Project Details

Parameter

Details

Project

Green Heights Residential Tower

Location

Kolkata, India

Building

G+10 Residential Building

Built-up Area

85,000 sq ft

Planned Duration

January 2026 – December 2026

Project Budget

₹85,000,000

The dataset used in this project is a simulated construction project dataset created for analytical and portfolio purposes.

🎯 Objectives

Monitor construction project cost and budget performance.

Compare planned and actual project progress.

Identify delayed and underperforming activities.

Calculate EVM indicators such as CPI and SPI.

Analyse labour productivity.

Monitor material consumption and wastage.

Evaluate quality inspections and rework costs.

Analyse equipment operating hours and utilization.

Develop an interactive Power BI dashboard for project decision support.

🛠️ Tools & Technologies

Tool

Purpose

Python

Data validation, cleaning and KPI analysis

Pandas

Data manipulation and analysis

MySQL

Relational database and SQL analysis

Power BI

Interactive dashboard and visualization

Excel / CSV

Data storage and data exchange

📂 Project Structure

Construction_Project_Analytics/
│
├── data/
│   └── Construction_Project_Performance_Dataset.xlsx
│
├── python/
│   ├── 01_data_validation_cleaning.py
│   └── 02_kpi_analysis.py
│
├── sql/
│   └── construction_project_analytics.sql
│
├── powerbi/
│   └── Construction_Project_Analytics.pbix
│
├── output/
│   ├── evm_summary.csv
│   ├── activity_performance.csv
│   ├── labour_productivity.csv
│   ├── material_wastage.csv
│   ├── quality_performance.csv
│   └── equipment_performance.csv
│
└── README.md

🔄 Data Analytics Workflow

Construction Dataset
        ↓
Data Validation & Cleaning
        ↓
Python KPI Analysis
        ↓
MySQL Database
        ↓
SQL Queries & Views
        ↓
Power BI Data Model
        ↓
Interactive Dashboard
        ↓
Project Performance Insights

🐍 Python Analysis

Python was used as the analytical layer for data validation, cleaning and KPI calculation.

Data Validation

The validation process checks:

Table sizes

Column names

Missing values

Duplicate records

Primary key uniqueness

Project and activity relationships

Date consistency

Negative values

Labour man-hour calculations

Activity duration consistency

KPI Analysis

Python calculates:

Project budget

Planned cost

Actual cost

Cost variance

Planned progress

Actual progress

Progress gap

Planned Value (PV)

Earned Value (EV)

Actual Cost (AC)

Cost Performance Index (CPI)

Schedule Performance Index (SPI)

Cost Variance (CV)

Schedule Variance (SV)

Activity delays

Labour productivity

Material wastage

Quality pass/fail rate

Rework cost

Equipment utilization

🗄️ SQL Database

The project data is stored in a MySQL relational database named:

construction_project_analytics

Main Tables

Projects

Contractors

Activities

Progress

Cost_Transactions

Labour

Materials

Quality

Equipment

Weather

Analytical Views

vw_project_kpis

vw_activity_performance

vw_labour_productivity

vw_material_wastage

vw_quality_performance

📊 Power BI Dashboard

The Power BI dashboard provides an interactive overview of construction project performance.

KPI Cards

Total Project Budget

Actual Project Cost

Cost Variance

Overall Progress

CPI

SPI

Filters

Project

Date

Category

Activity

Contractor

Status

Dashboard Visuals

Activity Status

Cost Performance Trend

Budget vs Actual Cost

Daily Project Progress

Earned Value Analysis

Top Delayed Activities

Labour Productivity

Material Wastage

Quality Performance

Equipment Utilization

📐 Key Performance Indicators

Cost Performance Index (CPI)

CPI = Earned Value / Actual Cost

CPI > 1 → Cost efficient

CPI = 1 → On budget

CPI < 1 → Cost inefficiency

Schedule Performance Index (SPI)

SPI = Earned Value / Planned Value

SPI > 1 → Ahead of schedule

SPI = 1 → On schedule

SPI < 1 → Behind schedule

Cost Variance

CV = Earned Value - Actual Cost

Schedule Variance

SV = Earned Value - Planned Value

Material Wastage

Wastage % = Wastage Quantity / Planned Quantity × 100

Equipment Utilization

Utilization % =
Operating Hours /
(Operating Hours + Downtime Hours) × 100

🔍 Analysis Areas

1. Cost Performance

Actual expenditure is compared with planned cost to identify budget inefficiencies.

2. Schedule Performance

Planned and actual progress are compared to identify activities falling behind schedule.

3. Earned Value Management

PV, EV and AC are used to assess integrated cost and schedule performance.

4. Labour Productivity

Man-hours and activity output are analysed to understand workforce productivity.

Productivity rates are interpreted within their respective units because construction activities use different measurement units.

5. Material Wastage

Material consumption and wastage are analysed by material type to identify opportunities for improved material efficiency.

6. Quality Performance

Inspection results, defects, failures and rework costs are analysed to evaluate construction quality.

7. Equipment Utilization

Operating hours, downtime, fuel consumption, rental costs and maintenance costs are analysed to evaluate equipment performance.

💡 Business Value

The system can help construction project teams:

Identify cost inefficiencies early

Detect schedule delays

Prioritize underperforming activities

Monitor labour performance

Reduce material wastage

Track quality issues and rework

Improve equipment utilization

Support data-driven project decisions

The dashboard converts raw construction records into information useful for project managers, planning engineers, quantity surveyors, construction managers and management teams.

📈 Example Questions Answered

Which activities have the highest delays?

Which activities have the largest progress gaps?

Is the project under or over budget?

Is the project ahead or behind schedule?

Is cost performance efficient?

Which materials have the highest wastage?

Which activities have lower labour productivity?

What is the quality inspection pass rate?

Which equipment has the highest downtime?

Where should corrective action be prioritized?

🚀 Future Improvements

Real-time project data integration

Automated daily progress updates

Contractor performance scoring

Project completion forecasting

Cost-at-completion forecasting

Machine learning-based delay prediction

Material demand forecasting

Automated project risk alerts

Power BI Service deployment

ERP/project management system integration

Areas of Interest

Structural Engineering

Construction Project Management

Data Analytics

Business Intelligence

Construction Technology

⭐ Project Highlights

Construction Domain + Data Analytics + SQL + Python + Power BI

This project demonstrates the application of data analytics and business intelligence techniques to a practical construction project management problem.


👨‍💻 Author
Sukchand Saren
B.Tech Civil Engineering
Jadavpur University
## 📬 Connect With Me
- 📧 Email: sukchandsaren30@gmail.com
- 💼 LinkedIn: https://www.linkedin.com/in/sukchand-saren-0418b5330?utm_source=share_via&utm_content=profile&utm_medium=member_android
- 🐙 GitHub: https://github.com/Sukchand30
