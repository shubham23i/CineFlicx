import os
from pathlib import Path
import logging

project_name="CineFlicx"

list_of_files = [

    ".github/workflows/.gitkeep",

    "artifacts/.gitkeep",
    "logs/.gitkeep",

    "research/trials.ipynb",

    "config/config.yaml",
    "config/schema.yaml",
    "config/model_params.yaml",

    "app.py",
    "requirements.txt",
    "setup.py",
    "Dockerfile",
    ".dockerignore",
    ".env",
    "README.md",

    "frontend/templates/index.html",
    "frontend/templates/movie.html",
    "frontend/templates/actor.html",
    "frontend/templates/director.html",
    "frontend/templates/search.html",
    "frontend/templates/base.html",

    "frontend/static/css/style.css",
    "frontend/static/js/main.js",
    "frontend/static/images/.gitkeep",

    f"src/{project_name}/__init__.py",

    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_validation.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/embedding_generator.py",
    f"src/{project_name}/components/faiss_index_builder.py",
    f"src/{project_name}/components/recommender.py",
    f"src/{project_name}/components/tmdb_fetcher.py",

    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/pipelines/training_pipeline.py",
    f"src/{project_name}/pipelines/prediction_pipeline.py",

    f"src/{project_name}/configuration/__init__.py",
    f"src/{project_name}/configuration/configuration.py",

    f"src/{project_name}/constants/__init__.py",

    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/entity/artifact_entity.py",

    f"src/{project_name}/exception/__init__.py",
    f"src/{project_name}/exception/exception_handler.py",

    f"src/{project_name}/logger/__init__.py",
    f"src/{project_name}/logger/log.py",

    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",

    f"src/{project_name}/recommender/__init__.py",
    f"src/{project_name}/recommender/content_based.py",
    f"src/{project_name}/recommender/collaborative.py",
    f"src/{project_name}/recommender/hybrid.py",
    f"src/{project_name}/recommender/semantic_search.py",

    f"src/{project_name}/llm/__init__.py",
    f"src/{project_name}/llm/summary_generator.py",
    f"src/{project_name}/llm/recommendation_explainer.py",

    f"src/{project_name}/database/__init__.py",
    f"src/{project_name}/database/db_connection.py",
    f"src/{project_name}/database/models.py",

    f"src/{project_name}/api/__init__.py",
    f"src/{project_name}/api/movie_routes.py",
    f"src/{project_name}/api/actor_routes.py",
    f"src/{project_name}/api/director_routes.py",
    f"src/{project_name}/api/recommendation_routes.py",

    "tests/__init__.py",
    "tests/test_api.py",
    "tests/test_recommender.py",
    "main.py"

]


for file in list_of_files:
    file_path = Path(file)
    file_dir,file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory {file_dir}")

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
        logging.info(f"Created file {file_path}")   
    else:
        logging.info(f"File {file_path} already exists")