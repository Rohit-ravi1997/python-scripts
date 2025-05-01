import json
import csv

# Input/output file paths
json_file_path = "Starhub_grafana_0804.json"
csv_file_path = "output.csv"

# Load JSON from file
with open(json_file_path, "r") as f:
    dashboard = json.load(f)

rows = []

# Iterate through panels
for panel in dashboard.get("panels", []):
    title = panel.get("title", "").strip()
    targets = panel.get("targets", [])
    
    for target in targets:
        expr = target.get("expr", "").strip()
        if expr:
            rows.append([title, expr])

# Write to CSV
with open(csv_file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "expr"])
    writer.writerows(rows)

print(f"CSV file '{csv_file_path}' has been created with {len(rows)} rows.")
