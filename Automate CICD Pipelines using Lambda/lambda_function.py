
import boto3

codepipeline = boto3.client('codepipeline')

def lambda_handler(event, context):
    return codepipeline.start_pipeline_execution(
        name='auto-cicd-pipeline'
    )
