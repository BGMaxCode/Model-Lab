import mlflow
import random
import time

# 1. Set the Tracking URI to point to our local MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5002")

# 2. Set an Experiment Name
mlflow.set_experiment("ATM_Transaction_Logs")

print("Starting simulated tracking runs...")

# Simulate 3 different runs with varying parameters
for execution_id in range(1, 4):
    with mlflow.start_run(run_name=f"Simulation_Run_{execution_id}"):
        
        # Log parameters (Settings for this run)
        users_simulated = random.randint(10, 50)
        max_withdrawal = random.choice([500, 1000, 2000])
        mlflow.log_param("users_simulated", users_simulated)
        mlflow.log_param("max_withdrawal_limit", max_withdrawal)
        
        print(f"Executing Run {execution_id} - Users: {users_simulated}, Max Withdrawal: ${max_withdrawal}")
        
        # Simulate processing time
        time.sleep(1)
        
        # Log metrics (Results of the run)
        success_rate = random.uniform(85.0, 99.9)
        avg_latency = random.uniform(10.0, 50.0)
        
        mlflow.log_metric("transaction_success_rate", success_rate)
        mlflow.log_metric("avg_latency_ms", avg_latency)
        
        print(f"  -> Success Rate: {success_rate:.2f}% | Avg Latency: {avg_latency:.2f}ms\n")

print("Finished logging! Check the MLflow UI at http://127.0.0.1:5002 to see these results.")
