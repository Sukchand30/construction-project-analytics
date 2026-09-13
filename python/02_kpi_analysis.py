import pandas as pd

file_path = r"E:\Project Performance\Construction_Project_Performance_Dataset.xlsx"

# Load required sheets
projects = pd.read_excel(file_path, sheet_name="Projects")
activities = pd.read_excel(file_path, sheet_name="Activities")
progress = pd.read_excel(file_path, sheet_name="Progress")
cost_transactions = pd.read_excel(file_path, sheet_name="Cost_Transactions")
labour = pd.read_excel(file_path, sheet_name="Labour")
materials = pd.read_excel(file_path, sheet_name="Materials")
quality = pd.read_excel(file_path, sheet_name="Quality")
equipment = pd.read_excel(file_path, sheet_name="Equipment")

# Convert date columns
progress["Date"] = pd.to_datetime(progress["Date"])
cost_transactions["Date"] = pd.to_datetime(cost_transactions["Date"])
labour["Date"] = pd.to_datetime(labour["Date"])
materials["Date"] = pd.to_datetime(materials["Date"])
quality["Date"] = pd.to_datetime(quality["Date"])
equipment["Date"] = pd.to_datetime(equipment["Date"])

print("Data loaded successfully.")

print("\n========== PROJECT COST KPIs ==========")

# Project budget
project_budget = projects["Total_Budget_INR"].sum()

# Planned and actual costs
planned_cost = cost_transactions["Planned_Cost_INR"].sum()
actual_cost = cost_transactions["Actual_Cost_INR"].sum()

# Cost variance
cost_variance = planned_cost - actual_cost

# Print results
print("Project Budget:", project_budget)
print("Total Planned Cost:", planned_cost)
print("Total Actual Cost:", actual_cost)
print("Cost Variance:", cost_variance)

print("\n========== PROJECT PROGRESS ==========")

# Get the latest progress record for each activity
latest_progress = (
    progress.sort_values("Date")
    .groupby("Activity_ID")
    .tail(1)
)

# Overall planned and actual progress
overall_planned_progress = latest_progress["Planned_Percentage"].mean()
overall_actual_progress = latest_progress["Actual_Percentage"].mean()

progress_variance = (
    overall_actual_progress -
    overall_planned_progress
)

print(
    "Overall Planned Progress:",
    round(overall_planned_progress, 2), "%"
)

print(
    "Overall Actual Progress:",
    round(overall_actual_progress, 2), "%"
)

print(
    "Progress Variance:",
    round(progress_variance, 2), "%"
)


# ==================================================
# EARNED VALUE MANAGEMENT
# ==================================================

print("\n========== EARNED VALUE MANAGEMENT ==========")

# Latest reporting date
latest_date = progress["Date"].max()

print("Latest Reporting Date:", latest_date)

# Combine activity budget with latest progress
evm = activities[
    [
        "Activity_ID",
        "Budget_Cost_INR"
    ]
].merge(
    latest_progress[
        [
            "Activity_ID",
            "Planned_Percentage",
            "Actual_Percentage"
        ]
    ],
    on="Activity_ID",
    how="left"
)

# Planned Value
evm["PV"] = (
    evm["Budget_Cost_INR"] *
    evm["Planned_Percentage"] / 100
)

# Earned Value
evm["EV"] = (
    evm["Budget_Cost_INR"] *
    evm["Actual_Percentage"] / 100
)

# Total PV and EV
PV = evm["PV"].sum()
EV = evm["EV"].sum()

# Actual Cost up to latest reporting date
AC = cost_transactions[
    cost_transactions["Date"] <= latest_date
]["Actual_Cost_INR"].sum()

print("Planned Value (PV):", round(PV, 2))
print("Earned Value (EV):", round(EV, 2))
print("Actual Cost (AC):", round(AC, 2))


# ==================================================
# EVM PERFORMANCE INDICATORS
# ==================================================

print("\n========== EVM PERFORMANCE ==========")

CPI = EV / AC if AC != 0 else 0
SPI = EV / PV if PV != 0 else 0

CV = EV - AC
SV = EV - PV

print("Cost Performance Index (CPI):", round(CPI, 3))
print("Schedule Performance Index (SPI):", round(SPI, 3))
print("Cost Variance (CV):", round(CV, 2))
print("Schedule Variance (SV):", round(SV, 2))

# ==================================================
# ACTIVITY PERFORMANCE ANALYSIS
# ==================================================

print("\n========== ACTIVITY PERFORMANCE ==========")

# Add activity information to latest progress
activity_performance = latest_progress[
    [
        "Activity_ID",
        "Planned_Percentage",
        "Actual_Percentage",
        "Delay_Days"
    ]
].merge(
    activities[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Budget_Cost_INR"
        ]
    ],
    on="Activity_ID",
    how="left"
)

# Progress gap
activity_performance["Progress_Gap_%"] = (
    activity_performance["Actual_Percentage"] -
    activity_performance["Planned_Percentage"]
)

# Sort by largest delay
top_delayed = activity_performance.sort_values(
    "Delay_Days",
    ascending=False
).head(10)

print("\n--- TOP 10 DELAYED ACTIVITIES ---")

print(
    top_delayed[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Delay_Days",
            "Progress_Gap_%"
        ]
    ].to_string(index=False)
)

# Activities with largest negative progress gap
top_progress_gap = activity_performance.sort_values(
    "Progress_Gap_%"
).head(10)

print("\n--- TOP 10 ACTIVITIES BY PROGRESS GAP ---")

print(
    top_progress_gap[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Progress_Gap_%",
            "Delay_Days"
        ]
    ].to_string(index=False)
)
# ==================================================
# QUALITY PERFORMANCE ANALYSIS
# ==================================================

print("\n========== QUALITY PERFORMANCE ==========")

total_inspections = len(quality)

passed_inspections = quality["Result"].astype(str).str.lower().eq("pass").sum()
failed_inspections = quality["Result"].astype(str).str.lower().eq("fail").sum()

pass_rate = (
    passed_inspections / total_inspections
) * 100 if total_inspections > 0 else 0

fail_rate = (
    failed_inspections / total_inspections
) * 100 if total_inspections > 0 else 0

total_rework_cost = quality["Rework_Cost_INR"].sum()

print("Total Inspections:", total_inspections)
print("Passed Inspections:", passed_inspections)
print("Failed Inspections:", failed_inspections)
print("Pass Rate:", round(pass_rate, 2), "%")
print("Fail Rate:", round(fail_rate, 2), "%")
print("Total Rework Cost:", round(total_rework_cost, 2))


# Defect analysis
defect_analysis = (
    quality[
        quality["Result"].astype(str).str.lower() == "fail"
    ]
    .groupby("Defect_Type")
    .agg(
        Defect_Count=("Inspection_ID", "count"),
        Total_Rework_Cost_INR=("Rework_Cost_INR", "sum")
    )
    .reset_index()
)

print("\n--- DEFECT ANALYSIS ---")

print(
    defect_analysis
    .sort_values("Defect_Count", ascending=False)
    .to_string(index=False)
)

# ==================================================
# EQUIPMENT PERFORMANCE ANALYSIS
# ==================================================

print("\n========== EQUIPMENT PERFORMANCE ==========")

total_operating_hours = equipment["Operating_Hours"].sum()
total_downtime_hours = equipment["Downtime_Hours"].sum()
total_fuel = equipment["Fuel_Consumption_Litres"].sum()
total_rental_cost = equipment["Rental_Cost_INR"].sum()
total_maintenance_cost = equipment["Maintenance_Cost_INR"].sum()

total_available_hours = (
    total_operating_hours + total_downtime_hours
)

utilization_percentage = (
    total_operating_hours /
    total_available_hours
) * 100 if total_available_hours > 0 else 0

print("Total Operating Hours:", round(total_operating_hours, 2))
print("Total Downtime Hours:", round(total_downtime_hours, 2))
print("Equipment Utilization:", round(utilization_percentage, 2), "%")
print("Total Fuel Consumption:", round(total_fuel, 2), "Litres")
print("Total Rental Cost:", round(total_rental_cost, 2))
print("Total Maintenance Cost:", round(total_maintenance_cost, 2))


# Equipment-wise performance
equipment_performance = (
    equipment.groupby(
        ["Equipment_Name", "Equipment_Type"]
    )
    .agg(
        Operating_Hours=("Operating_Hours", "sum"),
        Downtime_Hours=("Downtime_Hours", "sum"),
        Fuel_Consumption_Litres=("Fuel_Consumption_Litres", "sum"),
        Rental_Cost_INR=("Rental_Cost_INR", "sum"),
        Maintenance_Cost_INR=("Maintenance_Cost_INR", "sum")
    )
    .reset_index()
)

equipment_performance["Utilization_%"] = (
    equipment_performance["Operating_Hours"] /
    (
        equipment_performance["Operating_Hours"] +
        equipment_performance["Downtime_Hours"]
    )
) * 100

print("\n--- EQUIPMENT-WISE PERFORMANCE ---")

print(
    equipment_performance
    .sort_values("Utilization_%", ascending=False)
    .to_string(index=False)
)

# ==================================================
# LABOUR PRODUCTIVITY ANALYSIS
# ==================================================

print("\n========== LABOUR PRODUCTIVITY ==========")

labour_productivity = (
    labour.groupby("Activity_ID")
    .agg(
        Total_Man_Hours=("Man_Hours", "sum"),
        Total_Productivity_Quantity=("Productivity_Quantity", "sum"),
        Average_Productivity_Rate=("Productivity_Rate", "mean")
    )
    .reset_index()
)

labour_productivity = labour_productivity.merge(
    activities[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Unit"
        ]
    ],
    on="Activity_ID",
    how="left"
)

print(
    labour_productivity.head(15).to_string(index=False)
)

print("\n--- PRODUCTIVITY BY ACTIVITY ---")

print(
    labour_productivity[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Unit",
            "Total_Man_Hours",
            "Total_Productivity_Quantity",
            "Average_Productivity_Rate"
        ]
    ]
    .sort_values(
        "Average_Productivity_Rate",
        ascending=False
    )
    .head(15)
    .to_string(index=False)
)

# ==================================================
# MATERIAL WASTAGE ANALYSIS
# ==================================================

print("\n========== MATERIAL WASTAGE ==========")

total_planned_material = materials["Planned_Quantity"].sum()
total_actual_material = materials["Actual_Quantity"].sum()
total_wastage = materials["Wastage_Quantity"].sum()

overall_wastage_percentage = (
    total_wastage / total_planned_material
) * 100 if total_planned_material > 0 else 0

print(
    "Total Planned Material Quantity:",
    round(total_planned_material, 2)
)

print(
    "Total Actual Material Quantity:",
    round(total_actual_material, 2)
)

print(
    "Total Wastage Quantity:",
    round(total_wastage, 2)
)

print(
    "Overall Wastage Percentage:",
    round(overall_wastage_percentage, 2),
    "%"
)


# Material-wise wastage
material_wastage = (
    materials.groupby(
        [
            "Material_Name",
            "Material_Category",
            "Unit"
        ]
    )
    .agg(
        Planned_Quantity=("Planned_Quantity", "sum"),
        Actual_Quantity=("Actual_Quantity", "sum"),
        Wastage_Quantity=("Wastage_Quantity", "sum"),
        Total_Cost_INR=("Total_Cost_INR", "sum")
    )
    .reset_index()
)

material_wastage["Wastage_Percentage"] = (
    material_wastage["Wastage_Quantity"] /
    material_wastage["Planned_Quantity"]
) * 100

print("\n--- HIGHEST MATERIAL WASTAGE ---")

print(
    material_wastage
    .sort_values(
        "Wastage_Percentage",
        ascending=False
    )
    .head(10)
    .to_string(index=False)
)

# ==================================================
# EXPORT ANALYTICAL RESULTS
# ==================================================

import os

# Create output folder if it does not exist
os.makedirs("../output", exist_ok=True)

# 1. EVM Summary
evm_summary = pd.DataFrame({
    "Metric": [
        "PV",
        "EV",
        "AC",
        "CPI",
        "SPI",
        "CV",
        "SV"
    ],
    "Value": [
        PV,
        EV,
        AC,
        CPI,
        SPI,
        CV,
        SV
    ]
})

evm_summary.to_csv(
    "../output/evm_summary.csv",
    index=False
)


# 2. Activity Performance
activity_performance.to_csv(
    "../output/activity_performance.csv",
    index=False
)


# 3. Labour Productivity
labour_productivity.to_csv(
    "../output/labour_productivity.csv",
    index=False
)


# 4. Material Wastage
material_wastage.to_csv(
    "../output/material_wastage.csv",
    index=False
)


# 5. Quality Performance
quality.to_csv(
    "../output/quality_performance.csv",
    index=False
)


# 6. Equipment Performance
equipment_performance.to_csv(
    "../output/equipment_performance.csv",
    index=False
)


print("\n========== EXPORT COMPLETED ==========")

print("Analytical files saved in the output folder.")