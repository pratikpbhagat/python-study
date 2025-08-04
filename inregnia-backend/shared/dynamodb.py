# shared/dynamodb.py
import boto3

from shared.config import settings


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        region_name=settings.dynamodb_region,
        endpoint_url=settings.dynamodb_endpoint
    )


def get_table():
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(settings.dynamodb_table_name)
