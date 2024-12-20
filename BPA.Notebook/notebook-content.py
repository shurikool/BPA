# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "30cc3ed2-9a7f-4052-a70d-173f9a36a411",
# META       "default_lakehouse_name": "BPA",
# META       "default_lakehouse_workspace_id": "62454fb0-764d-4c6d-81a3-58b2487f6f5a"
# META     },
# META     "environment": {
# META       "environmentId": "d37027bb-1b51-4659-95aa-061f53d68e2e",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
# Welcome to your new notebook
# Type here in the cell editor to add code!
import sempy_labs as labs
from sempy_labs import migration, directlake, admin
from sempy_labs import lakehouse as lake
from sempy_labs import report as rep
from sempy_labs.tom import connect_semantic_model
from sempy_labs.report import ReportWrapper
from sempy_labs import ConnectWarehouse
from sempy_labs import ConnectLakehouse
import datetime

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

 # Ensure the table exists (create it if not)
spark.sql("""
    CREATE TABLE IF NOT EXISTS BPA.ErrorLog (
        timestamp STRING,
        workspace STRING,
        dataset STRING,
        error_message STRING
    )
    """)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load BPA.ModelsToAnalyze table
models_to_analyze_df = spark.sql("""
SELECT *
FROM BPA.ModelsToAnalyze
WHERE Timestamp > (
    SELECT MAX(Timestamp)
    FROM BPA.MaxModelToAnalyze
)
""")
models_to_analyze_df.show()



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Convert the result to a list of dictionaries
workspace_dataset_pairs = models_to_analyze_df.select('workspaceid', 'datasetid').collect()
# Convert the rows into a list of dictionaries
workspace_dataset_pairs = [{'workspace': row['workspaceid'], 'dataset': row['datasetid']} for row in workspace_dataset_pairs]
# Function to log errors into the ErrorLog table
def log_error(workspace, dataset, error_message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Escape single quotes in the error message by replacing them with two single quotes
    error_message = error_message.replace("'", "''")
    
    # Insert error into BPA.ErrorLog table
    spark.sql(f"""
    INSERT INTO BPA.ErrorLog (timestamp, workspace, dataset, error_message)
    VALUES ('{timestamp}', '{workspace}', '{dataset}', '{error_message}')
    """)
# Iterate through the pairs
for pair in workspace_dataset_pairs:
    workspace = pair['workspace']
    dataset = pair['dataset']
    try:
        print(f"Processing Workspace: {workspace}, Dataset: {dataset}")
        labs.run_model_bpa(
            dataset=dataset,
            workspace=workspace,
            export=True,
            extended=True
        )
    except Exception as e:
        # Log the error with relevant details
        error_message = str(e)
        print(f"Error processing Workspace: {workspace}, Dataset: {dataset} - {error_message}")
        log_error(workspace, dataset, error_message)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
