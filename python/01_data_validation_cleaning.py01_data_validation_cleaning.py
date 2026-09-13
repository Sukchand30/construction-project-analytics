import pandas as pd
file_path = r"E:\Project Performance\Construction_Project_Performance_Dataset.xlsx"
excel_file = pd. ExcelFile(file_path)
# Import all sheets

projects = pd.read_excel(file_path, sheet_name="Projects")
contractors = pd.read_excel(file_path, sheet_name="Contractors")
activities = pd.read_excel(file_path, sheet_name="Activities")
progress = pd.read_excel(file_path, sheet_name="Progress")
cost_transactions = pd.read_excel(file_path, sheet_name="Cost_Transactions")
labour = pd.read_excel(file_path, sheet_name="Labour")
materials = pd.read_excel(file_path, sheet_name="Materials")
quality = pd.read_excel(file_path, sheet_name="Quality")
equipment = pd.read_excel(file_path, sheet_name="Equipment")
weather = pd.read_excel(file_path, sheet_name="Weather")
calendar = pd.read_excel(file_path, sheet_name="Calendar")

print("All sheets imported successfully!")
# Check number of rows and columns in each table

print("\n--- TABLE SIZES ---")

print("Projects:", projects.shape)
print("Contractors:", contractors.shape)
print("Activities:", activities.shape)
print("Progress:", progress.shape)
print("Cost Transactions:", cost_transactions.shape)
print("Labour:", labour.shape)
print("Materials:", materials.shape)
print("Quality:", quality.shape)
print("Equipment:", equipment.shape)
print("Weather:", weather.shape)
print("Calendar:", calendar.shape)

print("\n--- ROWS AND COLUMNS ---")

tables = {
    "Projects": projects,
    "Contractors": contractors,
    "Activities": activities,
    "Progress": progress,
    "Cost Transactions": cost_transactions,
    "Labour": labour,
    "Materials": materials,
    "Quality": quality,
    "Equipment": equipment,
    "Weather": weather,
    "Calendar": calendar
}

for name, df in tables.items():
    rows, columns = df.shape
    print(f"{name}: Rows = {rows}, Columns = {columns}")

    print("\n--- MISSING VALUES ---")

for name, df in tables.items():
    print(f"\n{name}")
    print(df.isnull().sum())

    print("\n--- DUPLICATE RECORDS ---")

for name, df in tables.items():
    duplicates = df.duplicated().sum()
    print(f"{name}: {duplicates} duplicate rows")

    print("\n--- ID CHECK ---")

id_columns = {
    "Projects": ["Project_ID"],
    "Contractors": ["Contractor_ID"],
    "Activities": ["Activity_ID"],
}

for table_name, columns in id_columns.items():
    df = tables[table_name]

    for column in columns:
        duplicate_ids = df[column].duplicated().sum()
        missing_ids = df[column].isnull().sum()

        print(f"\n{table_name} - {column}")
        print(f"Duplicate IDs: {duplicate_ids}")
        print(f"Missing IDs: {missing_ids}")

        print("\n--- ACTIVITY ID RELATIONSHIP CHECK ---")

activity_ids = set(activities["Activity_ID"])

progress_ids = set(progress["Activity_ID"])

cost_ids = set(cost_transactions["Activity_ID"])

labour_ids = set(labour["Activity_ID"])

materials_ids = set(materials["Activity_ID"])

quality_ids = set(quality["Activity_ID"])

equipment_ids = set(equipment["Activity_ID"])


print("Progress IDs not found in Activities:",
      progress_ids - activity_ids)

print("Cost IDs not found in Activities:",
      cost_ids - activity_ids)

print("Labour IDs not found in Activities:",
      labour_ids - activity_ids)

print("Materials IDs not found in Activities:",
      materials_ids - activity_ids)

print("Quality IDs not found in Activities:",
      quality_ids - activity_ids)

print("Equipment IDs not found in Activities:",
      equipment_ids - activity_ids)

print("\n--- PROJECT ID RELATIONSHIP CHECK ---")

project_ids = set(projects["Project_ID"])

for name, df in tables.items():

    if "Project_ID" in df.columns:

        used_ids = set(df["Project_ID"])

        invalid_ids = used_ids - project_ids

        print(f"{name}: {invalid_ids}")

        print("\n--- PROGRESS VALIDATION ---")
        print("\n--- PROGRESS COLUMNS ---")
print("\n--- PROGRESS VALIDATION ---")

print("Minimum Actual Progress:",
      progress["Actual_Percentage"].min())

print("Maximum Actual Progress:",
      progress["Actual_Percentage"].max())

print("Minimum Planned Progress:",
      progress["Planned_Percentage"].min())

print("Maximum Planned Progress:",
      progress["Planned_Percentage"].max())

print("\n--- NEGATIVE VALUE CHECK ---")

print("Negative Budget Costs:",
      (activities["Budget_Cost_INR"] < 0).sum())

print("Negative Actual Costs:",
      (cost_transactions["Actual_Cost_INR"] < 0).sum())

print("Negative Labour Hours:",
      (labour["Man_Hours"] < 0).sum())

print("Negative Material Quantity:",
      (materials["Actual_Quantity"] < 0).sum())

print("\n--- BUDGET CONSISTENCY CHECK ---")

project_budget = projects["Total_Budget_INR"].sum()

activity_budget = activities["Budget_Cost_INR"].sum()

difference = project_budget - activity_budget

print("Total Project Budget:", project_budget)
print("Total Activity Budget:", activity_budget)
print("Difference:", difference)

print("\n--- DATE VALIDATION ---")

# Convert date columns to datetime
projects["Start_Date"] = pd.to_datetime(projects["Start_Date"])
projects["Planned_End_Date"] = pd.to_datetime(projects["Planned_End_Date"])

activities["Planned_Start_Date"] = pd.to_datetime(activities["Planned_Start_Date"])
activities["Planned_End_Date"] = pd.to_datetime(activities["Planned_End_Date"])

progress["Date"] = pd.to_datetime(progress["Date"])
cost_transactions["Date"] = pd.to_datetime(cost_transactions["Date"])
labour["Date"] = pd.to_datetime(labour["Date"])
materials["Date"] = pd.to_datetime(materials["Date"])
quality["Date"] = pd.to_datetime(quality["Date"])
equipment["Date"] = pd.to_datetime(equipment["Date"])
weather["Date"] = pd.to_datetime(weather["Date"])

# Check whether activity end date is before start date
invalid_activity_dates = (
    activities["Planned_End_Date"] < activities["Planned_Start_Date"]
).sum()

print("Activities with invalid dates:", invalid_activity_dates)

# Check whether project end date is before start date
invalid_project_dates = (
    projects["Planned_End_Date"] < projects["Start_Date"]
).sum()

print("Projects with invalid dates:", invalid_project_dates)

activities["Calculated_Duration_Days"] = (
    activities["Planned_End_Date"]
    - activities["Planned_Start_Date"]
).dt.days + 1

duration_mismatch = (
    activities["Duration_Days"] != activities["Calculated_Duration_Days"]
).sum()

print("Activities with duration mismatch:", duration_mismatch)



print("\n--- LABOUR MAN-HOURS VALIDATION ---")

labour["Calculated_Man_Hours"] = (
    labour["Number_of_Workers"] * labour["Working_Hours"]
)

labour["Man_Hours_Difference"] = (
    labour["Man_Hours"] - labour["Calculated_Man_Hours"]
)

mismatch = (
    labour["Man_Hours_Difference"].abs() > 0.01
).sum()

print("Man-Hours mismatches:", mismatch)



print("\n--- SAMPLE LABOUR DATA ---")

print(
    labour[
        [
            "Number_of_Workers",
            "Working_Hours",
            "Man_Hours",
            "Productivity_Quantity",
            "Productivity_Unit",
            "Productivity_Rate"
        ]
    ].head(10)
)

print("\n--- DURATION MISMATCH DETAILS ---")

mismatches = activities[
    activities["Duration_Days"] != activities["Calculated_Duration_Days"]
]

print(
    mismatches[
        [
            "Activity_ID",
            "Activity_Name",
            "Planned_Start_Date",
            "Planned_End_Date",
            "Duration_Days",
            "Calculated_Duration_Days"
        ]
    ].to_string(index=False)
)

print("\n--- FIXING DURATION MISMATCHES ---")

activities.loc[
    activities["Activity_ID"] == "A001",
    "Duration_Days"
] = 10

activities.loc[
    activities["Activity_ID"] == "A047",
    "Duration_Days"
] = 21

activities.loc[
    activities["Activity_ID"] == "A064",
    "Duration_Days"
] = 101

print("Duration mismatches corrected.")
duration_mismatch = (
    activities["Duration_Days"] != activities["Calculated_Duration_Days"]
).sum()

print("Activities with duration mismatch:", duration_mismatch)

duration_mismatch = (
    activities["Duration_Days"] != activities["Calculated_Duration_Days"]
).sum()

print("Activities with duration mismatch:", duration_mismatch)

print("\n--- MATERIAL VALIDATION ---")

# 1. Check negative quantities
negative_actual_qty = (
    materials["Actual_Quantity"] < 0
).sum()

negative_planned_qty = (
    materials["Planned_Quantity"] < 0
).sum()

negative_wastage = (
    materials["Wastage_Quantity"] < 0
).sum()

print("Negative planned quantities:", negative_planned_qty)
print("Negative actual quantities:", negative_actual_qty)
print("Negative wastage quantities:", negative_wastage)

# 2. Check material total cost

materials["Calculated_Total_Cost"] = (
    materials["Actual_Quantity"] *
    materials["Unit_Cost_INR"]
)

materials["Cost_Difference"] = (
    materials["Total_Cost_INR"] -
    materials["Calculated_Total_Cost"]
)

cost_mismatch = (
    materials["Cost_Difference"].abs() > 0.01
).sum()

print("Material cost mismatches:", cost_mismatch)

print("\n--- MATERIAL WASTAGE VALIDATION ---")

# Calculate wastage quantity
materials["Calculated_Wastage_Quantity"] = (
    materials["Actual_Quantity"] -
    materials["Planned_Quantity"]
)

# Calculate wastage percentage
materials["Calculated_Wastage_Percentage"] = (
    materials["Calculated_Wastage_Quantity"] /
    materials["Planned_Quantity"]
) * 100

# Check wastage quantity mismatch
wastage_qty_mismatch = (
    materials["Wastage_Quantity"] -
    materials["Calculated_Wastage_Quantity"]
).abs() > 0.01

print(
    "Wastage quantity mismatches:",
    wastage_qty_mismatch.sum()
)

# Check wastage percentage mismatch
wastage_pct_mismatch = (
    materials["Wastage_Percentage"] -
    materials["Calculated_Wastage_Percentage"]
).abs() > 0.01

print(
    "Wastage percentage mismatches:",
    wastage_pct_mismatch.sum()
)
print("\n--- COST VALIDATION ---")

negative_planned_cost = (
    cost_transactions["Planned_Cost_INR"] < 0
).sum()

negative_actual_cost = (
    cost_transactions["Actual_Cost_INR"] < 0
).sum()

print("Negative planned costs:", negative_planned_cost)
print("Negative actual costs:", negative_actual_cost)

duplicate_cost_ids = (
    cost_transactions["Cost_ID"].duplicated()
).sum()

print("Duplicate Cost IDs:", duplicate_cost_ids)

print("\n--- COST TYPES ---")
print(
    cost_transactions["Cost_Type"]
    .value_counts()
)

print("\n--- COST PERFORMANCE CHECK ---")

total_planned_cost = cost_transactions["Planned_Cost_INR"].sum()
total_actual_cost = cost_transactions["Actual_Cost_INR"].sum()

cost_variance = total_planned_cost - total_actual_cost

print("Total Planned Cost:", total_planned_cost)
print("Total Actual Cost:", total_actual_cost)
print("Cost Variance:", cost_variance)

over_budget_transactions = (
    cost_transactions["Actual_Cost_INR"] >
    cost_transactions["Planned_Cost_INR"]
).sum()

print(
    "Transactions where actual cost > planned cost:",
    over_budget_transactions
)
print("\n--- QUALITY VALIDATION ---")

duplicate_inspection_ids = (
    quality["Inspection_ID"].duplicated()
).sum()

print("Duplicate Inspection IDs:", duplicate_inspection_ids)
print("\n--- INSPECTION RESULTS ---")
print(
    quality["Result"]
    .value_counts()
)
print("\n--- REWORK VALIDATION ---")

print("Rework Required values:")
print(
    quality["Rework_Required"]
    .value_counts()
)

print("\nTotal Rework Cost:",
      quality["Rework_Cost_INR"].sum())

print(
    "Negative Rework Costs:",
    (quality["Rework_Cost_INR"] < 0).sum()
)

print("\n--- FAILED INSPECTION vs REWORK ---")

failed_inspections = quality[
    quality["Result"].astype(str).str.lower() == "fail"
]

print("Total Failed Inspections:", len(failed_inspections))

print(
    "Failed inspections requiring rework:",
    failed_inspections["Rework_Required"]
    .astype(str)
    .str.lower()
    .eq("yes")
    .sum()
)

print(
    "Total Rework Cost from failed inspections:",
    failed_inspections["Rework_Cost_INR"].sum()
)

rework_logic_error = (
    (quality["Rework_Required"].astype(str).str.lower() == "no") &
    (quality["Rework_Cost_INR"] > 0)
).sum()

print(
    "Records with Rework = No but positive Rework Cost:",
    rework_logic_error
)

print("\n--- EQUIPMENT VALIDATION ---")

duplicate_equipment_ids = (
    equipment["Equipment_ID"].duplicated()
).sum()

print("Duplicate Equipment IDs:", duplicate_equipment_ids)
negative_operating_hours = (
    equipment["Operating_Hours"] < 0
).sum()

negative_downtime_hours = (
    equipment["Downtime_Hours"] < 0
).sum()

negative_fuel = (
    equipment["Fuel_Consumption_Litres"] < 0
).sum()

print("Negative Operating Hours:", negative_operating_hours)
print("Negative Downtime Hours:", negative_downtime_hours)
print("Negative Fuel Consumption:", negative_fuel)

print("\n--- EQUIPMENT STATUS ---")
print(
    equipment["Equipment_Status"]
    .value_counts()
)
print("\n========== FINAL DATA QUALITY CHECK ==========")

# 1. Missing values
print("\n--- Missing Values ---")

for name, df in tables.items():
    missing = df.isnull().sum().sum()
    print(f"{name}: {missing}")

# 2. Duplicate rows
print("\n--- Duplicate Rows ---")

for name, df in tables.items():
    duplicates = df.duplicated().sum()
    print(f"{name}: {duplicates}")

# 3. Negative values in important numeric columns
print("\n--- Negative Values ---")

print(
    "Negative Project Budgets:",
    (projects["Total_Budget_INR"] < 0).sum()
)

print(
    "Negative Activity Budgets:",
    (activities["Budget_Cost_INR"] < 0).sum()
)

print(
    "Negative Actual Costs:",
    (cost_transactions["Actual_Cost_INR"] < 0).sum()
)

print(
    "Negative Labour Hours:",
    (labour["Man_Hours"] < 0).sum()
)

print(
    "Negative Material Quantities:",
    (materials["Actual_Quantity"] < 0).sum()
)

print(
    "Negative Equipment Operating Hours:",
    (equipment["Operating_Hours"] < 0).sum()
)

print("\n========== VALIDATION COMPLETE ==========")

print("\n========== PROJECT COST KPIs ==========")

project_budget = projects["Total_Budget_INR"].sum()

planned_cost = cost_transactions["Planned_Cost_INR"].sum()

actual_cost = cost_transactions["Actual_Cost_INR"].sum()

cost_variance = planned_cost - actual_cost

print("Project Budget:", project_budget)
print("Total Planned Cost:", planned_cost)
print("Total Actual Cost:", actual_cost)
print("Cost Variance:", cost_variance)

print("\n========== PROJECT PROGRESS ==========")

latest_progress = progress.sort_values("Date").groupby(
    "Activity_ID"
).tail(1)

overall_planned_progress = latest_progress["Planned_Percentage"].mean()
overall_actual_progress = latest_progress["Actual_Percentage"].mean()

print(
    "Overall Planned Progress:",
    round(overall_planned_progress, 2), "%"
)

print(
    "Overall Actual Progress:",
    round(overall_actual_progress, 2), "%"
)

progress_variance = (
    overall_actual_progress -
    overall_planned_progress
)

print(
    "Progress Variance:",
    round(progress_variance, 2), "%"
)
print("\n========== EARNED VALUE MANAGEMENT ==========")

# Latest reporting date
latest_date = progress["Date"].max()

print("Latest Reporting Date:", latest_date)

# Latest progress record for each activity
latest_progress = (
    progress.sort_values("Date")
    .groupby("Activity_ID")
    .tail(1)
)

# Merge activity budget with latest progress
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

# Planned Value (PV)
evm["PV"] = (
    evm["Budget_Cost_INR"] *
    evm["Planned_Percentage"] / 100
)

# Earned Value (EV)
evm["EV"] = (
    evm["Budget_Cost_INR"] *
    evm["Actual_Percentage"] / 100
)

PV = evm["PV"].sum()
EV = evm["EV"].sum()

# Actual Cost up to latest reporting date
AC = cost_transactions[
    cost_transactions["Date"] <= latest_date
]["Actual_Cost_INR"].sum()

print("Planned Value (PV):", round(PV, 2))
print("Earned Value (EV):", round(EV, 2))
print("Actual Cost (AC):", round(AC, 2))

print("\n========== EVM PERFORMANCE ==========")

CPI = EV / AC
SPI = EV / PV

print("Cost Performance Index (CPI):", round(CPI, 3))
print("Schedule Performance Index (SPI):", round(SPI, 3))
CV = EV - AC
SV = EV - PV

print("Cost Variance (CV):", round(CV, 2))
print("Schedule Variance (SV):", round(SV, 2))
print("\n========== TOP DELAYED ACTIVITIES ==========")

activity_delay = (
    latest_progress[
        [
            "Activity_ID",
            "Planned_Percentage",
            "Actual_Percentage",
            "Delay_Days"
        ]
    ]
    .merge(
        activities[
            [
                "Activity_ID",
                "Activity_Name",
                "Category"
            ]
        ],
        on="Activity_ID",
        how="left"
    )
)

top_delayed = activity_delay.sort_values(
    "Delay_Days",
    ascending=False
).head(10)

print(
    top_delayed.to_string(index=False)
)

print("\n========== PROGRESS GAP ==========")

activity_delay["Progress_Gap"] = (
    activity_delay["Actual_Percentage"] -
    activity_delay["Planned_Percentage"]
)

top_progress_gaps = activity_delay.sort_values(
    "Progress_Gap"
).head(10)

print(
    top_progress_gaps.to_string(index=False)
)
print("\n========== HIGHEST BUDGET ACTIVITIES ==========")

activity_budget = activities[
    [
        "Activity_ID",
        "Activity_Name",
        "Category",
        "Budget_Cost_INR"
    ]
].sort_values(
    "Budget_Cost_INR",
    ascending=False
).head(10)

print(
    activity_budget.to_string(index=False)
)
print("\n========== ACTIVITY RISK ANALYSIS ==========")

risk_analysis = activity_delay.merge(
    activities[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Budget_Cost_INR"
        ]
    ],
    on=["Activity_ID", "Activity_Name", "Category"],
    how="left"
)

total_activity_budget = activities["Budget_Cost_INR"].sum()

risk_analysis["Budget_Share_%"] = (
    risk_analysis["Budget_Cost_INR"] /
    total_activity_budget
) * 100

print(
    risk_analysis[
        [
            "Activity_ID",
            "Activity_Name",
            "Category",
            "Progress_Gap",
            "Delay_Days",
            "Budget_Cost_INR",
            "Budget_Share_%"
        ]
    ]
    .sort_values(
        ["Delay_Days", "Budget_Cost_INR"],
        ascending=[False, False]
    )
    .head(15)
    .to_string(index=False)
)
print("\n========== RISK CLASSIFICATION ==========")

risk_analysis["Risk_Score"] = (
    (-risk_analysis["Progress_Gap"]) * 0.5
    + risk_analysis["Delay_Days"] * 2
    + risk_analysis["Budget_Share_%"] * 1.5
)

def classify_risk(score):
    if score >= 15:
        return "High"
    elif score >= 8:
        return "Medium"
    else:
        return "Low"

risk_analysis["Risk_Level"] = (
    risk_analysis["Risk_Score"]
    .apply(classify_risk)
)

risk_summary = risk_analysis[
    [
        "Activity_ID",
        "Activity_Name",
        "Category",
        "Progress_Gap",
        "Delay_Days",
        "Budget_Cost_INR",
        "Budget_Share_%",
        "Risk_Score",
        "Risk_Level"
    ]
].sort_values(
    "Risk_Score",
    ascending=False
)

print(
    risk_summary.head(15).to_string(index=False)
)
print("\n========== LABOUR PRODUCTIVITY ==========")

labour_productivity = (
    labour.groupby("Activity_ID")
    .agg(
        Total_Man_Hours=("Man_Hours", "sum"),
        Total_Productivity_Quantity=("Productivity_Quantity", "sum"),
        Average_Productivity_Rate=("Productivity_Rate", "mean"),
        Total_Workers=("Number_of_Workers", "sum")
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

print("\n========== PRODUCTIVITY BY UNIT ==========")

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

print("\n========== MATERIAL WASTAGE ANALYSIS ==========")

total_planned_material = materials["Planned_Quantity"].sum()
total_actual_material = materials["Actual_Quantity"].sum()
total_wastage = materials["Wastage_Quantity"].sum()

overall_wastage_percentage = (
    total_wastage / total_planned_material
) * 100

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

print("\n========== HIGHEST MATERIAL WASTAGE ==========")

material_wastage = (
    materials.groupby(
        ["Material_Name", "Material_Category", "Unit"]
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

print(
    material_wastage
    .sort_values("Wastage_Percentage", ascending=False)
    .head(10)
    .to_string(index=False)
)
print("\n========== QUALITY PERFORMANCE ==========")

total_inspections = len(quality)

passed_inspections = (
    quality["Result"]
    .astype(str)
    .str.lower()
    .eq("pass")
    .sum()
)

failed_inspections = (
    quality["Result"]
    .astype(str)
    .str.lower()
    .eq("fail")
    .sum()
)

pass_rate = (
    passed_inspections / total_inspections
) * 100

fail_rate = (
    failed_inspections / total_inspections
) * 100

total_rework_cost = quality["Rework_Cost_INR"].sum()

print("Total Inspections:", total_inspections)
print("Passed Inspections:", passed_inspections)
print("Failed Inspections:", failed_inspections)
print("Pass Rate:", round(pass_rate, 2), "%")
print("Fail Rate:", round(fail_rate, 2), "%")
print("Total Rework Cost:", round(total_rework_cost, 2))

print("\n========== DEFECT ANALYSIS ==========")

defect_analysis = (
    quality[
        quality["Defect_Type"].notna()
    ]
    .groupby("Defect_Type")
    .agg(
        Defect_Count=("Inspection_ID", "count"),
        Rework_Cost_INR=("Rework_Cost_INR", "sum")
    )
    .reset_index()
    .sort_values(
        "Defect_Count",
        ascending=False
    )
)

print(
    defect_analysis.to_string(index=False)
)

print("\n========== EQUIPMENT PERFORMANCE ==========")

total_operating_hours = equipment["Operating_Hours"].sum()
total_downtime_hours = equipment["Downtime_Hours"].sum()
total_fuel = equipment["Fuel_Consumption_Litres"].sum()
total_rental_cost = equipment["Rental_Cost_INR"].sum()
total_maintenance_cost = equipment["Maintenance_Cost_INR"].sum()

utilization = (
    total_operating_hours /
    (total_operating_hours + total_downtime_hours)
) * 100

print("Total Operating Hours:", round(total_operating_hours, 2))
print("Total Downtime Hours:", round(total_downtime_hours, 2))
print("Equipment Utilization:", round(utilization, 2), "%")
print("Total Fuel Consumption:", round(total_fuel, 2), "Litres")
print("Total Rental Cost:", round(total_rental_cost, 2))
print("Total Maintenance Cost:", round(total_maintenance_cost, 2))

print("\n========== EQUIPMENT-WISE PERFORMANCE ==========")

equipment_analysis = (
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

equipment_analysis["Utilization_%"] = (
    equipment_analysis["Operating_Hours"] /
    (
        equipment_analysis["Operating_Hours"] +
        equipment_analysis["Downtime_Hours"]
    )
) * 100

print(
    equipment_analysis
    .sort_values("Utilization_%")
    .head(10)
    .to_string(index=False)
)
print("\n========================================")
print("PYTHON DATA VALIDATION AND KPI ANALYSIS")
print("COMPLETED SUCCESSFULLY")
print("========================================")