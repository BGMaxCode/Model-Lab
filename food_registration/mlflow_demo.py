import mlflow
import random
import time

mlflow.set_tracking_uri("http://127.0.0.1:5002")
mlflow.set_experiment("Food_Order_Logs")

print("Starting simulated tracking runs for Food_Order_Logs...")

param1_name = "active_drivers"
param1_choices = [5, 15, 30]
param2_name = "peak_hour_multiplier"
param2_choices = [1.0, 1.5, 2.0]

for execution_id in range(1, 4):
    with mlflow.start_run(run_name=f"Simulation_Run_{execution_id}"):
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
        
        print(f"Executing Run {execution_id} - {param1_name}: {p1_val}, {param2_name}: {p2_val}")
        print(f"  -> Success Rate: {success_rate:.2f}% | Avg Latency: {avg_latency:.2f}ms\n")

print("Finished logging! Check the MLflow UI at http://127.0.0.1:5002 to see these results.")
