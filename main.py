import re
import csv

def extract_budget_goals(file_path, output_csv):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regex pattern to capture title, needed goal, and due time (monthly or eventually)
    pattern = re.compile(
        r'<div class="budget-table-cell-goal-nowrap">.*?'  # Match the start of the div
        r'<button title="(.*?)">.*?</button>.*?'  # Extract the title inside button
        r'<div class="budget-table-cell-goal-status">.*?<span.*?>(\$[\d,]+\.\d{2})</span>.*?needed</div>.*?'  # Extract goal amount
        r'<div class="budget-table-cell-goal-status-details">(.*?)</div>',  # Extract due time
        re.DOTALL  # Enable multi-line matching
    )
    
    matches = pattern.findall(content)
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["CATEGORY", "GOAL", "TYPE"])
        
        for title, goal_needed, due in matches:
            category = re.sub(r'\s*\(.*?\)', '', title.split('\n')[0].strip())  # Clean category title
            goal_number = goal_needed.replace('$', '').replace(',', '')  # Convert to a pure number
            
            goal_type = "Monthly" if "this month" in due.lower() else "Eventually"
            
            csv_writer.writerow([category, goal_number, goal_type])

# Example usage
file_path = "budget_data.html"  # Change this to the actual file path
output_csv = "budget_goals.csv"
extract_budget_goals(file_path, output_csv)

print(f"CSV file '{output_csv}' has been created successfully.")