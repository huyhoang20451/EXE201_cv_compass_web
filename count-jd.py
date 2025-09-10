import json
from collections import Counter

# Load JSON
with open("database/job-description.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# Đếm số JD theo company_name
company_counts = Counter(job["company_name"] for job in jobs)

# In kết quả
for company, count in company_counts.items():
    print(f"{company}: {count} JD")
