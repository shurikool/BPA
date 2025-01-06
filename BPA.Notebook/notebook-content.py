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
# META       "environmentId": "3193f667-0746-43d4-962c-613d3cda89f4",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# CELL ********************

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

# Sélectionnez la dernière date pour que seuls les nouveaux modèles sémantiques soient pris en compte
models_to_analyze_df = spark.sql("""
SELECT *
FROM BPA.ModelsToAnalyze
WHERE Timestamp > (
    SELECT COALESCE(MAX(Timestamp),CAST('2000-01-01 00:00:00' AS TIMESTAMP) )
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

# Convertir le résultat en une liste de dictionnaires
workspace_dataset_pairs = models_to_analyze_df.select('workspaceid', 'datasetid').collect()
# Convertir les lignes en une liste de dictionnaires
workspace_dataset_pairs = [{'workspace': row['workspaceid'], 'dataset': row['datasetid']} for row in workspace_dataset_pairs]
# Fonction pour enregistrer les erreurs dans la table ErrorLog
def log_error(workspace, dataset, error_message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Échapper aux guillemets simples dans le message d'erreur en les remplaçant par deux guillemets simples
    error_message = error_message.replace("'", "''")
    
    # Insérer une erreur dans la table BPA.ErrorLog
    spark.sql(f"""
    INSERT INTO BPA.ErrorLog (timestamp, workspace, dataset, error_message)
    VALUES ('{timestamp}', '{workspace}', '{dataset}', '{error_message}')
    """)
# Parcourez les paires
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
        # Enregistrez l'erreur avec les détails pertinents
        error_message = str(e)
        print(f"Error processing Workspace: {workspace}, Dataset: {dataset} - {error_message}")
        log_error(workspace, dataset, error_message)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Vérifier si la table est vide
result = spark.sql("SELECT COUNT(*) AS row_count FROM maxmodeltoanalyze").collect()[0]["row_count"]

# Construire et exécuter la requête SQL appropriée
if result == 0:
    spark.sql("""
        INSERT INTO maxmodeltoanalyze (timestamp)
        VALUES (CAST('2000-01-01 00:00:00' AS TIMESTAMP))
    """)
else:
    spark.sql("""
        INSERT INTO maxmodeltoanalyze (timestamp)
        SELECT MAX(timestamp) FROM modelstoanalyze
    """)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
