from collections import namedtuple

DataIngestionConfig=namedtuple('DataIngestionConfig',['dataset_download_url','ingested_directory','raw_data_directory'])

DataTransformationConfig = namedtuple(
    'DataTransformationConfig',
    [
        'transformed_data_directory',
        'ratings_csv_file_path',
        'movies_csv_file_path',
        'links_csv_file_path',
        'tags_csv_file_path'
    ]
)

DataValidationConfig = namedtuple(
    "DataValidationConfig",
    [
        "validated_directory",
        "min_user_ratings_threshold",
        "min_movie_ratings_threshold",
        "ratings_file_name",
        "movies_file_name",
        "links_file_name",
        "tags_file_name"
    ]
)