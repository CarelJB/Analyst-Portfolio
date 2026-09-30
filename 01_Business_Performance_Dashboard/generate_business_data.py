import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(42)

# -----------------------------
# CONFIG
# -----------------------------
NUM_ROWS = 200
OUTPUT_FILE = "raw_business_data.xlsx"

customers = [
    "Alpha Mining",
    "Khula Engineering",
    "Rustenburg Crushers",
    "Mzansi Aggregates",
    "North Star Processing",
    "Horizon Minerals",
    "Delta Plant Hire",
    "Ubuntu Resources",
    "Apex Industrial",
    "Vuka Logistics",
    "Goldline Projects",
    "Siyakhula Services",
    "Titan Bulk Systems",
    "Imbokodo Materials",
    "Platinum Works"
]

categories = {
    "Product": [
        "Belt Supply",
        "Installation Kit",
        "Industrial Rollers"
    ],
    "Service": [
        "Cold Splicing",
        "Repair Service",
        "Emergency Callout"
    ],
    "Maintenance": [
        "Maintenance Visit",
        "Pulley Lagging",
        "Site Inspection"
    ],
    "Consumables": [
        "Consumable Kit",
        "Adhesive Pack",
        "Splicing Tools Refill"
    ],
    "Support": [
        "Support Retainer",
        "Technical Support Visit",
        "Monthly Support Package"
    ]
}

regions = ["Gauteng", "North West", "Free State", "Mpumalanga", "Limpopo"]
salespeople = ["Carel", "James", "Thabo", "Pieter", "Lerato"]

# Customers do not buy equally from all categories
customer_preferences = {
    "Alpha Mining": ["Service", "Maintenance", "Product"],
    "Khula Engineering": ["Product", "Consumables"],
    "Rustenburg Crushers": ["Maintenance", "Service"],
    "Mzansi Aggregates": ["Product", "Service", "Consumables"],
    "North Star Processing": ["Support", "Service"],
    "Horizon Minerals": ["Maintenance", "Support"],
    "Delta Plant Hire": ["Product", "Maintenance"],
    "Ubuntu Resources": ["Service", "Support"],
    "Apex Industrial": ["Product", "Consumables", "Service"],
    "Vuka Logistics": ["Support", "Consumables"],
    "Goldline Projects": ["Maintenance", "Service", "Product"],
    "Siyakhula Services": ["Support", "Service"],
    "Titan Bulk Systems": ["Product", "Maintenance"],
    "Imbokodo Materials": ["Consumables", "Product"],
    "Platinum Works": ["Service", "Maintenance", "Support"]
}

# More realistic unit price ranges by item
price_ranges = {
    "Belt Supply": (18000, 65000),
    "Installation Kit": (3500, 12000),
    "Industrial Rollers": (4500, 18000),
    "Cold Splicing": (12000, 45000),
    "Repair Service": (6000, 25000),
    "Emergency Callout": (10000, 30000),
    "Maintenance Visit": (5000, 18000),
    "Pulley Lagging": (10000, 35000),
    "Site Inspection": (2500, 8500),
    "Consumable Kit": (1200, 6000),
    "Adhesive Pack": (900, 3500),
    "Splicing Tools Refill": (800, 2800),
    "Support Retainer": (8000, 18000),
    "Technical Support Visit": (3000, 12000),
    "Monthly Support Package": (10000, 22000)
}

# Quantity rules by item type
quantity_ranges = {
    "Belt Supply": (1, 4),
    "Installation Kit": (1, 6),
    "Industrial Rollers": (1, 8),
    "Cold Splicing": (1, 3),
    "Repair Service": (1, 4),
    "Emergency Callout": (1, 2),
    "Maintenance Visit": (1, 4),
    "Pulley Lagging": (1, 3),
    "Site Inspection": (1, 5),
    "Consumable Kit": (1, 10),
    "Adhesive Pack": (2, 15),
    "Splicing Tools Refill": (1, 12),
    "Support Retainer": (1, 1),
    "Technical Support Visit": (1, 4),
    "Monthly Support Package": (1, 1)
}

# Margin ranges by category (higher margin = lower cost ratio)
cost_ratio_ranges = {
    "Product": (0.68, 0.82),       # lower margins
    "Service": (0.45, 0.65),       # better margins
    "Maintenance": (0.50, 0.68),
    "Consumables": (0.72, 0.88),   # tight margins
    "Support": (0.30, 0.50)        # high margins
}

# Regional weighting
region_weights = {
    "Gauteng": 0.28,
    "North West": 0.26,
    "Free State": 0.14,
    "Mpumalanga": 0.18,
    "Limpopo": 0.14
}

# Monthly weighting to avoid identical months
month_weights = {
    1: 0.07,
    2: 0.08,
    3: 0.09,
    4: 0.07,
    5: 0.08,
    6: 0.09,
    7: 0.10,
    8: 0.08,
    9: 0.09,
    10: 0.10,
    11: 0.08,
    12: 0.07
}

# -----------------------------
# HELPERS
# -----------------------------
def weighted_choice(weight_dict):
    items = list(weight_dict.keys())
    weights = list(weight_dict.values())
    return random.choices(items, weights=weights, k=1)[0]

def random_date_in_2025():
    month = weighted_choice(month_weights)
    start_date = datetime(2025, month, 1)
    if month == 12:
        end_date = datetime(2025, 12, 31)
    else:
        end_date = datetime(2025, month + 1, 1) - timedelta(days=1)
    delta_days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, delta_days))

def pick_customer():
    # Slight bias toward a few bigger customers
    weights = [1.4, 0.8, 1.2, 0.9, 1.0, 0.8, 0.9, 0.8, 1.1, 0.7, 1.2, 0.8, 0.9, 0.7, 0.8]
    return random.choices(customers, weights=weights, k=1)[0]

def pick_category_for_customer(customer):
    preferred = customer_preferences[customer]
    # Mostly preferred categories, sometimes any category
    if random.random() < 0.82:
        return random.choice(preferred)
    return random.choice(list(categories.keys()))

def generate_row():
    customer = pick_customer()
    category = pick_category_for_customer(customer)
    product_service = random.choice(categories[category])
    date = random_date_in_2025()
    quantity = random.randint(*quantity_ranges[product_service])

    unit_price = round(random.uniform(*price_ranges[product_service]), 2)

    # Slight customer-size effect
    if customer in ["Alpha Mining", "Rustenburg Crushers", "Goldline Projects"]:
        unit_price *= random.uniform(1.03, 1.18)
    elif customer in ["Vuka Logistics", "Imbokodo Materials"]:
        unit_price *= random.uniform(0.92, 1.02)

    unit_price = round(unit_price, 2)

    revenue = round(quantity * unit_price, 2)

    cost_ratio = random.uniform(*cost_ratio_ranges[category])

    # Some randomness by service type
    if product_service == "Emergency Callout":
        cost_ratio += random.uniform(0.03, 0.08)  # urgency costs
    if product_service in ["Support Retainer", "Monthly Support Package"]:
        cost_ratio -= random.uniform(0.03, 0.07)  # better margins

    cost_ratio = max(0.25, min(cost_ratio, 0.92))

    direct_cost = round(revenue * cost_ratio, 2)
    gross_profit = round(revenue - direct_cost, 2)

    region = weighted_choice(region_weights)
    salesperson = random.choices(
        salespeople,
        weights=[1.15, 0.95, 1.00, 0.90, 1.00],
        k=1
    )[0]

    return {
        "Date": date.date(),
        "Customer": customer,
        "Category": category,
        "Product_Service": product_service,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Revenue": revenue,
        "Direct_Cost": direct_cost,
        "Gross_Profit": gross_profit,
        "Region": region,
        "Salesperson": salesperson
    }

# -----------------------------
# GENERATE DATA
# -----------------------------
rows = [generate_row() for _ in range(NUM_ROWS)]
df = pd.DataFrame(rows)

# Sort by date for realism
df = df.sort_values("Date").reset_index(drop=True)

# -----------------------------
# SAVE TO EXCEL
# -----------------------------
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Raw_Data", index=False)

    ws = writer.book["Raw_Data"]

    # Freeze top row
    ws.freeze_panes = "A2"

    # Set column widths
    column_widths = {
        "A": 14,  # Date
        "B": 24,  # Customer
        "C": 16,  # Category
        "D": 24,  # Product_Service
        "E": 12,  # Quantity
        "F": 14,  # Unit_Price
        "G": 14,  # Revenue
        "H": 14,  # Direct_Cost
        "I": 14,  # Gross_Profit
        "J": 14,  # Region
        "K": 14   # Salesperson
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    # Currency formatting
    currency_cols = ["F", "G", "H", "I"]
    for col in currency_cols:
        for cell in ws[col][1:]:
            cell.number_format = '#,##0.00'

    # Quantity formatting
    for cell in ws["E"][1:]:
        cell.number_format = '0'

print(f"Dataset created successfully: {OUTPUT_FILE}")
print(df.head(10))