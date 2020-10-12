import mlflow.sklearn
import os
import re
import pandas as pd
import numpy as np
import json
import boto3


def get_artifact(run_id: str) -> dict:
    client = mlflow.tracking.MlflowClient()
    s3_path = client.get_run(run_id).info.artifact_uri
    result = re.search(r"s3://(.+?)/(.+)", s3_path)
    if result is None:
        raise ValueError('S3 path is wrong')
    bucket = result.group(1)
    key = os.path.join(result.group(2), '<artifact_file_name>')
    s3 = boto3.resource('s3')
    body = s3.Object(bucket, key).get()['Body'].read().decode('utf-8')
    return json.loads(body)

def predict(run_id: str, X: pd.DataFrame, artifact: dict) -> np.ndarray:
    """
    "sk_model" should be same as name used in `log_model` method
    e.g. mlflow.sklearn.log_model(model, "sk_model")
    """
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/sk_model")
    return model.predict(X)

def main():
    mlflow.set_tracking_uri('http://localhost:5000')
    mlflow_run_id = 'xxxxx'

    artifact = get_artifact(mlflow_run_id)
    X = pd.DataFrame()
    result = predict(mlflow_run_id, X, artifact)
    print(result)


if __name__ == '__main__':
    main()
