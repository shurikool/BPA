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
# META     }
# META   }
# META }

# CELL ********************

 # Ensure the table exists (create it if not)
spark.sql("""
    CREATE TABLE IF NOT EXISTS ModelsToAnalyze (
        timestamp Timestamp,
        EmailAddress STRING,
        WorkspaceId STRING,
        DatasetId STRING
    )
    """)

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

 # Ensure the table exists (create it if not)
spark.sql("""
    CREATE TABLE IF NOT EXISTS MaxModelToAnalyze(
        timestamp Timestamp
    )
    """)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
