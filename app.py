import os
import aws_cdk as cdk
from aws_cdk import aws_rds as rds
from proj_420_d07.stacks.s3_stack import S3Stack
from proj_420_d07.stacks.glue_stack import GlueStack


class Projet007(cdk.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._environment = cdk.Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"),
            region=os.getenv("CDK_DEFAULT_REGION"),
        )

        s3_stack = S3Stack(
            scope=self,
            construct_id="S3Stack",
            description="Definit le stockage S3 qui accueille les donnees sources",
            env=self._environment,
        )

        # TODO
        # rds_instance = rds.DatabaseInstance(
        #     self,
        #     id="MyRDSInstance",
        #     engine=rds.DatabaseInstanceEngine.mysql(
        #         version=rds.MysqlEngineVersion.VER_8_0
        #     ),
        #     instance_class=core.InstanceType.of(
        #         core.InstanceClass.BURSTABLE2, core.InstanceSize.MICRO
        #     ),
        #     master_username="admin",
        #     master_user_password=core.SecretValue.plain_text("password"),
        #     # removal_policy=core.RemovalPolicy.DESTROY,
        # )

        glue_stack = GlueStack(
            scope=self,
            construct_id="GlueStack",
            source_bucket=s3_stack.bucket,
            rds_instance=None,  # rds_instance,
            description="Definit le AWS Glue qui extrait les donnees depuis la source et les transforme",
            env=self._environment,
        )


app = Projet007()
app.synth()
