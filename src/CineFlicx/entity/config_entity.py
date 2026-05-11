from collections import namedtuple

DataIngestionConfig=namedtuple('DataIngestionConfig',['dataset_download_url','ingested_directory','raw_data_directory'])