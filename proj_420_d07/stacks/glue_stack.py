import os
import aws_cdk as cdk
from aws_cdk import (
    aws_glue as glue,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)


class GlueStack(cdk.Stack):
    def __init__(
        self, scope: cdk.App, construct_id: str, source_bucket, rds_instance, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Role IAM et policy pour Glue
        self.glue_role = iam.Role(
            scope=self,
            id="GlueRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            role_name="glue-role-420d07",  # os.getenv("GLUE_ROLE_NAME"),
        )

        self.glue_policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AWSGlueServiceRole"
        )
        self.glue_role.add_managed_policy(self.glue_policy)

        # Bucket S3 pour Glue
        self.glue_bucket = s3.Bucket(
            scope=self,
            id="GlueBucket",
            versioned=True,
            bucket_name="glue-bucket-420d07",  # os.getenv("GLUE_S3_BUCKET"),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            auto_delete_objects=True,
        )

        # Permission au role pour lire/écrire dans le bucket de Glue
        self.glue_bucket.grant_read_write(self.glue_role)

        # Permission au role pour lire dans le bucket source
        source_bucket.grant_read(self.glue_role)

        self.glue_job = glue.CfnJob(
            scope=self,
            id="GlueJob",
            role=self.glue_role.role_arn,
            name="glue-job-420d07",
            # max_capacity=1,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                python_version="3",
                script_location=f"s3://{self.glue_bucket.bucket_name}/glue-scripts/combine_data.py",
            ),
        )

        # Déploiement des scripts à exécuter par Glue Job vers le bucket de Glue
        s3deploy.BucketDeployment(
            scope=self,
            id="BucketDeployment",
            sources=[s3deploy.Source.asset("./proj_420_d07/glue-scripts")],
            destination_bucket=self.glue_bucket,
            destination_key_prefix="glue-scripts",
        )

        # TODO
        # BD pour Glue
        # glue_db = glue.Database(self, "MyGlueDatabase", database_name="mydatabase")

        # # Glue Table
        # glue_table = glue.Table(
        #     self,
        #     "MyGlueTable",
        #     database=glue_db,
        #     table_name="mytable",
        #     columns=[
        #         # Define your columns here
        #     ],
        #     partition_keys=[
        #         # Define your partition keys here
        #     ],
        #     data_format=glue.DataFormat.PARQUET,
        #     s3_prefix=f"{s3_bucket.bucket_name}/",
        # )

        # rds_instance.grant_connect(glue_role)

        # TODO
        # Glue Job 2 (pour RDS)
        # glue_job = glue.Job(
        #     self,
        #     "MyGlueJob",
        #     role=glue_role,
        #     command={
        #         "name": "glueetl",
        #         "script_location": "s3://path/to/glue/script.py",
        #     },
        #     default_arguments={
        #         "--TempDir": f"s3://{s3_bucket.bucket_name}/temp/",
        #         "--job-bookmark-option": "job-bookmark-enable",
        #     },
        #     connections={"connections": [f"{rds_instance.instance_endpoint}"]},
        # )
