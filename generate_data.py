import pandas as pd
import random
from datetime import datetime, timedelta
import os

# ---- UNITS ----
units = [
    {"UnitID": 1, "UnitName": "Whitefield PS", "DistrictID": 1},
    {"UnitID": 2, "UnitName": "MG Road PS", "DistrictID": 1},
    {"UnitID": 3, "UnitName": "Koramangala PS", "DistrictID": 1},
    {"UnitID": 4, "UnitName": "Jayanagar PS", "DistrictID": 1},
    {"UnitID": 5, "UnitName": "Indiranagar PS", "DistrictID": 1},
    {"UnitID": 6, "UnitName": "Hebbal PS", "DistrictID": 1},
]

# ---- IPC SECTIONS ----
ipc_sections = [
    {"IPCSectionID": 302, "SectionName": "Murder"},
    {"IPCSectionID": 307, "SectionName": "Attempt to Murder"},
    {"IPCSectionID": 376, "SectionName": "Rape"},
    {"IPCSectionID": 379, "SectionName": "Theft"},
    {"IPCSectionID": 380, "SectionName": "Theft in Dwelling"},
    {"IPCSectionID": 392, "SectionName": "Robbery"},
    {"IPCSectionID": 395, "SectionName": "Dacoity"},
    {"IPCSectionID": 420, "SectionName": "Cheating"},
    {"IPCSectionID": 363, "SectionName": "Kidnapping"},
    {"IPCSectionID": 366, "SectionName": "Abduction"},
]

# ---- CRIME HEADS ----
crime_heads = [
    {"CrimeHeadID": 1, "CrimeGroupName": "Crimes Against Body"},
    {"CrimeHeadID": 2, "CrimeGroupName": "Crimes Against Property"},
    {"CrimeHeadID": 3, "CrimeGroupName": "Crimes Against Women"},
    {"CrimeHeadID": 4, "CrimeGroupName": "Cyber Crime"},
    {"CrimeHeadID": 5, "CrimeGroupName": "Drug Trafficking"},
    {"CrimeHeadID": 6, "CrimeGroupName": "Kidnapping"},
]

# ---- CRIME SUB HEADS ----
crime_sub_heads = [
    {"CrimeSubHeadID": 1,  "CrimeHeadID": 1, "CrimeHeadName": "Murder",          "IPCSectionID": 302},
    {"CrimeSubHeadID": 2,  "CrimeHeadID": 1, "CrimeHeadName": "Assault",          "IPCSectionID": 307},
    {"CrimeSubHeadID": 3,  "CrimeHeadID": 2, "CrimeHeadName": "Robbery",          "IPCSectionID": 392},
    {"CrimeSubHeadID": 4,  "CrimeHeadID": 2, "CrimeHeadName": "Theft",            "IPCSectionID": 379},
    {"CrimeSubHeadID": 5,  "CrimeHeadID": 2, "CrimeHeadName": "Chain Snatching",  "IPCSectionID": 379},
    {"CrimeSubHeadID": 6,  "CrimeHeadID": 2, "CrimeHeadName": "Burglary",         "IPCSectionID": 380},
    {"CrimeSubHeadID": 7,  "CrimeHeadID": 2, "CrimeHeadName": "Vehicle Theft",    "IPCSectionID": 379},
    {"CrimeSubHeadID": 8,  "CrimeHeadID": 3, "CrimeHeadName": "Harassment",       "IPCSectionID": 376},
    {"CrimeSubHeadID": 9,  "CrimeHeadID": 4, "CrimeHeadName": "Cyber Fraud",      "IPCSectionID": 420},
    {"CrimeSubHeadID": 10, "CrimeHeadID": 4, "CrimeHeadName": "Online Scam",      "IPCSectionID": 420},
    {"CrimeSubHeadID": 11, "CrimeHeadID": 5, "CrimeHeadName": "Drug Peddling",    "IPCSectionID": 420},
    {"CrimeSubHeadID": 12, "CrimeHeadID": 5, "CrimeHeadName": "Drug Trafficking", "IPCSectionID": 420},
    {"CrimeSubHeadID": 13, "CrimeHeadID": 6, "CrimeHeadName": "Kidnapping",       "IPCSectionID": 363},
    {"CrimeSubHeadID": 14, "CrimeHeadID": 6, "CrimeHeadName": "Abduction",        "IPCSectionID": 366},
]

# ---- CRIME SEVERITY ----
crime_severity = {
    "Murder": "CRITICAL",
    "Attempt to Murder": "CRITICAL",
    "Kidnapping": "CRITICAL",
    "Abduction": "CRITICAL",
    "Rape": "CRITICAL",
    "Dacoity": "HIGH",
    "Robbery": "HIGH",
    "Drug Trafficking": "HIGH",
    "Drug Peddling": "HIGH",
    "Assault": "HIGH",
    "Burglary": "MEDIUM",
    "Chain Snatching": "MEDIUM",
    "Vehicle Theft": "MEDIUM",
    "Harassment": "MEDIUM",
    "Theft": "LOW",
    "Cyber Fraud": "LOW",
    "Online Scam": "LOW",
}

# ---- CASE STATUS ----
case_statuses = [
    {"CaseStatusID": 1, "CaseStatusName": "Under Investigation"},
    {"CaseStatusID": 2, "CaseStatusName": "Charge Sheeted"},
    {"CaseStatusID": 3, "CaseStatusName": "Closed"},
    {"CaseStatusID": 4, "CaseStatusName": "Undetected"},
]

# ---- LOCATIONS ----
locations = [
    {"area": "Whitefield",  "lat": 12.9698, "lon": 77.7499, "UnitID": 1},
    {"area": "MG Road",     "lat": 12.9756, "lon": 77.6097, "UnitID": 2},
    {"area": "Koramangala", "lat": 12.9279, "lon": 77.6271, "UnitID": 3},
    {"area": "Jayanagar",   "lat": 12.9308, "lon": 77.5833, "UnitID": 4},
    {"area": "Indiranagar", "lat": 12.9784, "lon": 77.6408, "UnitID": 5},
    {"area": "Hebbal",      "lat": 13.0358, "lon": 77.5970, "UnitID": 6},
]

# ---- REPEAT OFFENDERS ----
repeat_offenders = [
    "Raju Sharma",
    "Mohammed Siddiqui",
    "Vikram Nair",
    "Suresh Kumar",
    "Ramesh Gowda"
]

# ---- OTHER ACCUSED ----
other_accused = [
    "Ajay Singh", "Prakash Reddy", "Santhosh Kumar",
    "Imran Khan", "Deepak Verma", "Naveen Raj",
    "Arjun Shetty", "Kiran Patil", "Manoj Yadav",
    "Sunil Naik", "Rohit Das", "Ganesh Rao",
    "Salim Sheikh", "Vinod Kumar", "Ravi Shankar"
]

# ---- ACCUSED STATUS ----
accused_statuses = [
    "Released",
    "Absconding",
    "Arrested",
    "Under Surveillance"
]

# ---- OFFICERS ----
officers = [
    {"OfficerID": 1, "OfficerName": "Rajesh Kumar",  "Rank": "Inspector", "UnitID": 1},
    {"OfficerID": 2, "OfficerName": "Suresh Patil",  "Rank": "Constable", "UnitID": 2},
    {"OfficerID": 3, "OfficerName": "Anand Gowda",   "Rank": "Inspector", "UnitID": 3},
    {"OfficerID": 4, "OfficerName": "Priya Sharma",  "Rank": "DCP",       "UnitID": 4},
    {"OfficerID": 5, "OfficerName": "Mohammed Rafi", "Rank": "Constable", "UnitID": 5},
    {"OfficerID": 6, "OfficerName": "Kavitha Reddy", "Rank": "Inspector", "UnitID": 6},
]

# ---- HELPERS ----
def random_date(start_year=2022):
    start = datetime(start_year, 1, 1)
    end = datetime(2026, 6, 1)
    delta = end - start
    return start + timedelta(
        days=random.randint(0, delta.days)
    )

def random_time():
    hour = random.randint(0, 23)
    minute = random.choice([0, 15, 30, 45])
    return f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"

# ---- GENERATE CASES ----
cases = []
for i in range(1, 41):
    loc = random.choice(locations)
    sub = random.choice(crime_sub_heads)
    severity = crime_severity.get(
        sub["CrimeHeadName"], "LOW"
    )
    cases.append({
        "CaseMasterID": 1000 + i,
        "CrimeNo": f"1044300062026{str(i).zfill(5)}",
        "CaseNo": f"2026{str(i).zfill(5)}",
        "CrimeRegisteredDate": random_date().strftime(
            "%Y-%m-%d"
        ),
        "CrimeTime": random_time(),
        "PoliceStationID": loc["UnitID"],
        "CrimeMajorHeadID": sub["CrimeHeadID"],
        "CrimeMinorHeadID": sub["CrimeSubHeadID"],
        "CrimeType": sub["CrimeHeadName"],
        "IPCSectionID": sub["IPCSectionID"],
        "CaseStatusID": random.randint(1, 4),
        "GravityOffenceID": random.randint(1, 2),
        "CrimeSeverity": severity,
        "latitude": loc["lat"] + random.uniform(
            -0.01, 0.01
        ),
        "longitude": loc["lon"] + random.uniform(
            -0.01, 0.01
        ),
        "Area": loc["area"],
        "BriefFacts": (
            f"{sub['CrimeHeadName']} reported "
            f"at {loc['area']}"
        )
    })

# ---- GENERATE ACCUSED ----
accused_list = []
accused_id = 1

# Force repeat offenders into multiple cases
repeat_case_ids = random.sample(
    [c["CaseMasterID"] for c in cases], 15
)

for idx, offender in enumerate(repeat_offenders):
    assigned_cases = repeat_case_ids[idx*3:(idx+1)*3]
    for case_id in assigned_cases:
        case = next(
            c for c in cases
            if c["CaseMasterID"] == case_id
        )
        accused_list.append({
            "AccusedMasterID": accused_id,
            "CaseMasterID": case_id,
            "AccusedName": offender,
            "AgeYear": random.randint(22, 45),
            "GenderID": "M",
            "PersonID": "A1",
            "CrimeType": case["CrimeType"],
            "IPCSectionID": case["IPCSectionID"],
            "CrimeSeverity": case["CrimeSeverity"],
            "Status": random.choice([
                "Released",
                "Absconding",
                "Under Surveillance"
            ])
        })
        accused_id += 1

# Fill remaining with random accused
for case in cases:
    num = random.randint(1, 2)
    for j in range(num):
        accused_list.append({
            "AccusedMasterID": accused_id,
            "CaseMasterID": case["CaseMasterID"],
            "AccusedName": random.choice(other_accused),
            "AgeYear": random.randint(18, 55),
            "GenderID": random.choice(["M", "F"]),
            "PersonID": f"A{j+2}",
            "CrimeType": case["CrimeType"],
            "IPCSectionID": case["IPCSectionID"],
            "CrimeSeverity": case["CrimeSeverity"],
            "Status": random.choice(accused_statuses)
        })
        accused_id += 1

# ---- GENERATE VICTIMS ----
victims = []
victim_id = 1
for case in cases:
    victims.append({
        "VictimMasterID": victim_id,
        "CaseMasterID": case["CaseMasterID"],
        "VictimName": f"Victim {victim_id}",
        "AgeYear": random.randint(15, 70),
        "GenderID": random.choice(["M", "F"]),
        "VictimPolice": 0
    })
    victim_id += 1

# ---- GENERATE ARRESTS ----
arrests = []
arrest_id = 1
for accused in accused_list:
    if random.random() > 0.4:
        arrests.append({
            "ArrestSurrenderID": arrest_id,
            "CaseMasterID": accused["CaseMasterID"],
            "AccusedMasterID": accused["AccusedMasterID"],
            "AccusedName": accused["AccusedName"],
            "ArrestSurrenderDate": random_date().strftime(
                "%Y-%m-%d"
            ),
            "PoliceStationID": random.randint(1, 6),
            "ArrestSurrenderTypeID": random.randint(1, 2),
            "Status": accused["Status"]
        })
        arrest_id += 1

# ---- SAVE ALL ----
os.makedirs("data", exist_ok=True)

pd.DataFrame(cases).to_csv(
    "data/case_master.csv", index=False)
pd.DataFrame(accused_list).to_csv(
    "data/accused.csv", index=False)
pd.DataFrame(victims).to_csv(
    "data/victims.csv", index=False)
pd.DataFrame(arrests).to_csv(
    "data/arrests.csv", index=False)
pd.DataFrame(units).to_csv(
    "data/units.csv", index=False)
pd.DataFrame(ipc_sections).to_csv(
    "data/ipc_sections.csv", index=False)
pd.DataFrame(crime_sub_heads).to_csv(
    "data/crime_sub_heads.csv", index=False)
pd.DataFrame(case_statuses).to_csv(
    "data/case_statuses.csv", index=False)
pd.DataFrame(officers).to_csv(
    "data/officers.csv", index=False)

print("✅ Data generated successfully!")
print(f"Cases:    {len(cases)}")
print(f"Accused:  {len(accused_list)}")
print(f"Victims:  {len(victims)}")
print(f"Arrests:  {len(arrests)}")
print(f"Officers: {len(officers)}")