"""
- download: zipファイルをメモリ上にダウンロードして解凍する
- upload: localのディレクトリをメモリ上にダzipファイルとして読み込み、アップロードする
"""

import boto3
from zipfile import ZipFile
from io import BytesIO, StringIO
import re
import os
from typing import List
import csv
import tarfile

bucket, key = "my-bucket", "key/key.zip"


def download_code():
    obj = boto3.client('s3').get_object(Bucket=bucket, Key=key)
    dest_dir = '/home/foo/abc'
    with ZipFile(BytesIO(obj['Body'].read()), "r") as zf:
        zf.extractall(dest_dir)
    return dest_dir


def upload(local_dir):
    mem_zip = BytesIO()
    local_dir_reg = re.compile(local_dir + '/?')
    with ZipFile(mem_zip, "w") as zf:
        for dirname, subdirs, files in os.walk(local_dir):
            zip_dirname = local_dir_reg.sub("", dirname, 1)
            for filename in files:
                zf.write(os.path.join(dirname, filename),
                         os.path.join(zip_dirname, filename))
    boto3.client('s3').put_object(Body=mem_zip.getvalue(),
                                  Bucket=bucket,
                                  Key=key)


def upload_csv_gzip(bucket: str, key: str, rows: List[List[str]]):
    csv_io = StringIO()
    csv.writer(csv_io).writerows(rows)
    input_io = BytesIO(csv_io.getvalue().encode('utf-8'))
    filename = os.path.basename(key)
    csv_filename = filename.replace('tar.gz', '')

    tarinfo = tarfile.TarInfo(csv_filename)
    tarinfo.size = input_io.getbuffer().nbytes
    tar_io = BytesIO()
    with tarfile.open(fileobj=tar_io, mode='w:gz') as tar:
        tar.addfile(tarinfo, input_io)

    boto3.client('s3').put_object(Body=tar_io.getbuffer(),
                                  Bucket=bucket,
                                  Key=key)
