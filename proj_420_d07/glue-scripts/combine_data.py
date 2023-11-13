import os
import io
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import boto3


S3_BUCKET_GLUE = "glue-bucket-420d07"  # os.getenv("GLUE_S3_BUCKET")
S3_BUCKET_DATA = "source-bucket-420d07"  # os.getenv("SOURCE_S3_BUCKET")


def fetch_content(prefix):
    print(f"Recherche des donnees dans '{prefix}'.")
    response = s3.list_objects_v2(Bucket=S3_BUCKET_DATA, Prefix=prefix)

    for obj in response.get("Contents", []):
        object_key = obj["Key"]

        # Si dossier (se termine avec '/')
        if object_key.endswith("/"):
            # Récurivité sur les sous-dossier
            fetch_content(object_key)
        else:
            # Traitement parallel
            executor.submit(process_files, object_key)


def process_files(object_key):
    # Traiter juste les fichiers CSV
    if object_key.lower().endswith(".csv"):
        print(f"Traitement du fichier '{object_key}'.")

        response = s3.get_object(Bucket=S3_BUCKET_DATA, Key=object_key)
        content = response["Body"].read()
        content_str = content.decode("utf-8")

        df = spark.read.csv(
            io.StringIO(content_str),
            header=True,
            inferSchema=True,
        )
        # chunks = pd.read_csv(pd.compat.StringIO(content_str), chunksize=5000)

        # def append_csv_chunk(chunk):
        #     dfs.append(chunk)

        # with ThreadPoolExecutor() as chuncks_executor:
        #     chuncks_executor.map(append_csv_chunk, chunks)

        # df = pd.read_csv(io.BytesIO(content))
        print(f"DataFrame Shape: {df.shape}")
        dfs.append(df)
        print(f"dfs length : {len(dfs)}")


def save_result(result):
    print(f"Enregistrement dans le bucket S3 '{S3_BUCKET_GLUE}'.")

    result.write.csv(
        f"s3://{S3_BUCKET_GLUE}/data/original/combined.csv",  # destination_bucket_name, destination_folder, destination_filename
        header=True,
        mode="overwrite",
    )
    # result.to_csv("combined.csv", index=False)
    # s3.upload_file(
    #     "combined.csv",
    #     S3_BUCKET_GLUE,
    #     "data/original/combined.csv",
    # )
    # csv_buffer = io.StringIO()
    # result.to_csv(csv_buffer, index=False)
    # s3.Bucket(S3_BUCKET_GLUE).put_object(
    #     Body=csv_buffer.getvalue(),
    #     Key="data/original/combined.csv",
    # )
    print(
        f"Donnees combinees enregistrees avec succes dans le bucket S3 '{S3_BUCKET_GLUE}'."
    )


if __name__ == "__main__":
    try:
        print(f"Acces au bucket S3 '{S3_BUCKET_DATA}'.")
        s3 = boto3.client("s3")

        spark = SparkSession(SparkContext())
        dfs = []
        # Crée un pool d'éxecution avec fils (threads) parallels
        with ThreadPoolExecutor(max_workers=10) as executor:
            print("Debut du pool d'execution parallele.")
            fetch_content("")

        # Attendre que toutes les tâches se terminent
        executor.shutdown(wait=True)

        final_df = dfs[0]
        for df in dfs[1:]:
            final_df = final_df.union(df)

        # final_df = pd.concat(dfs, ignore_index=True)
        save_result(final_df)
        spark.stop()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
