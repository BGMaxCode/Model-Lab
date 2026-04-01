import os
import shutil

TEMPLATE_DIR = "/home/max/Documents/SE-templates/registration_system"
OUTPUT_BASE = "/home/max/Documents/SE-templates"

EXAMPLES = [
    {
        "APP_NAME": "ATM System",
        "APP_NAME_LOWER": "atm_system",
        "ITEM_LABEL": "Transaction",
        "ITEMS_LABEL": "Transactions",
        "ITEMS_LABEL_LOWER": "transactions",
        "CATEGORY_1": "Deposit",
        "CATEGORY_2": "Withdrawal",
        "CATEGORY_3": "Transfer"
    },
    {
        "APP_NAME": "Event Registration",
        "APP_NAME_LOWER": "event_registration",
        "ITEM_LABEL": "Registration",
        "ITEMS_LABEL": "Registrations",
        "ITEMS_LABEL_LOWER": "registrations",
        "CATEGORY_1": "General Admission",
        "CATEGORY_2": "VIP",
        "CATEGORY_3": "Early Bird"
    },
    {
        "APP_NAME": "Student Management",
        "APP_NAME_LOWER": "student_management",
        "ITEM_LABEL": "Student",
        "ITEMS_LABEL": "Students",
        "ITEMS_LABEL_LOWER": "students",
        "CATEGORY_1": "Undergraduate",
        "CATEGORY_2": "Graduate",
        "CATEGORY_3": "PhD"
    },
    {
        "APP_NAME": "Ticket Management",
        "APP_NAME_LOWER": "ticket_management",
        "ITEM_LABEL": "Ticket",
        "ITEMS_LABEL": "Tickets",
        "ITEMS_LABEL_LOWER": "tickets",
        "CATEGORY_1": "Bug Report",
        "CATEGORY_2": "Feature Request",
        "CATEGORY_3": "General Inquiry"
    },
    {
        "APP_NAME": "Food Registration",
        "APP_NAME_LOWER": "food_registration",
        "ITEM_LABEL": "Order",
        "ITEMS_LABEL": "Orders",
        "ITEMS_LABEL_LOWER": "orders",
        "CATEGORY_1": "Dine-in",
        "CATEGORY_2": "Takeaway",
        "CATEGORY_3": "Delivery"
    }
]

def generate_example(config):
    app_lower = config["APP_NAME_LOWER"]
    target_dir = os.path.join(OUTPUT_BASE, app_lower)
    
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    
    # Files to process
    files_to_process = [
        "app.py",
        "requirements.txt",
        "templates/base.html",
        "templates/auth.html",
        "templates/dashboard.html",
        "templates/form.html",
        "templates/items.html"
    ]
    
    os.makedirs(os.path.join(target_dir, "templates"), exist_ok=True)
    
    for rel_path in files_to_process:
        src_path = os.path.join(TEMPLATE_DIR, rel_path)
        dst_path = os.path.join(target_dir, rel_path)
        
        if not os.path.exists(src_path):
            print(f"Warning: {src_path} not found.")
            continue
            
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace placeholders
        for key, value in config.items():
            content = content.replace(f"[{key}]", value)
            
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"Generated {app_lower} in {target_dir}")

def main():
    print("Starting generation...")
    for example in EXAMPLES:
        generate_example(example)
    print("Done!")

if __name__ == "__main__":
    main()
