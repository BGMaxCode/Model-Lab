import os

projects = {
    "event_registration": {
        "exp_name": "Event_Registration_Logs",
        "params": {"expected_attendees": [50, 100, 500], "ticket_tiers": [1, 2, 3]}
    },
    "student_management": {
        "exp_name": "Student_Management_Logs",
        "params": {"enrollment_batch_size": [10, 50, 200], "courses_offered": [5, 10, 20]}
    },
    "ticket_management": {
        "exp_name": "Ticket_Management_Logs",
        "params": {"support_staff_online": [2, 5, 10], "priority_queue_enabled": [True, False]}
    },
    "food_registration": {
        "exp_name": "Food_Order_Logs",
        "params": {"active_drivers": [5, 15, 30], "peak_hour_multiplier": [1.0, 1.5, 2.0]}
    },
    "registration_system": {
        "exp_name": "Base_System_Logs",
        "params": {"load_test_users": [10, 100, 1000], "cache_enabled": [True, False]}
    }
}

base_dir = "/home/max/Documents/SE-templates"

script_template = """import mlflow
import random
import time

mlflow.set_tracking_uri("http://127.0.0.1:5002")
mlflow.set_experiment("{exp_name}")

print("Starting simulated tracking runs for {exp_name}...")

param1_name = "{p1_name}"
param1_choices = {p1_choices}
param2_name = "{p2_name}"
param2_choices = {p2_choices}

for execution_id in range(1, 4):
    with mlflow.start_run(run_name=f"Simulation_Run_{{execution_id}}"):
        p1_val = random.choice(param1_choices)
        p2_val = random.choice(param2_choices)
        
        mlflow.log_param(param1_name, p1_val)
        mlflow.log_param(param2_name, p2_val)
        
        # Simulate processing time
        time.sleep(1)
        
        success_rate = random.uniform(85.0, 99.9)
        avg_latency = random.uniform(10.0, 50.0)
        
        mlflow.log_metric("transaction_success_rate", success_rate)
        mlflow.log_metric("avg_latency_ms", avg_latency)
        
        print(f"Executing Run {{execution_id}} - {{param1_name}}: {{p1_val}}, {{param2_name}}: {{p2_val}}")
        print(f"  -> Success Rate: {{success_rate:.2f}}% | Avg Latency: {{avg_latency:.2f}}ms\\n")

print("Finished logging! Check the MLflow UI at http://127.0.0.1:5002 to see these results.")
"""

for folder, config in projects.items():
    folder_path = os.path.join(base_dir, folder)
    target_path = os.path.join(folder_path, "mlflow_demo.py")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        p_names = list(config["params"].keys())
        content = script_template.format(
            exp_name=config["exp_name"],
            p1_name=p_names[0],
            p1_choices=config["params"][p_names[0]],
            p2_name=p_names[1],
            p2_choices=config["params"][p_names[1]]
        )
        with open(target_path, "w") as f:
            f.write(content)
        print(f"Created {target_path}")
