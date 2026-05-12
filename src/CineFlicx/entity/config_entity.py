from collections import namedtuple


DataIngestionConfig = namedtuple(
    "DataIngestionConfig",
    [
        "dataset_download_url",
        "ingested_directory",
        "raw_data_directory"
    ]
)


DataValidationConfig = namedtuple(
    "DataValidationConfig",
    [
        "validated_directory",
        "ratings_file_name",
        "movies_file_name",
        "links_file_name",
        "tags_file_name"
    ]
)


DataTransformationConfig = namedtuple(
    "DataTransformationConfig",
    [
        "transformed_data_directory",
        "min_user_ratings_threshold",
        "min_movie_ratings_threshold"
    ]
)


PredictionPipelineConfig = namedtuple(
    "PredictionPipelineConfig",
    [
        "transformed_data_directory",
        "model_name",

        "metadata_file",
        "movie_pivot_file",
        "similarity_file",

        "title_to_movieid_file",
        "movieid_to_title_file",

        "embeddings_file",
        "faiss_index_file"
    ]
)

