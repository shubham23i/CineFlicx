from src.CineFlicx.components.data_ingestion import DataIngestion
from src.CineFlicx.components.data_transformation import DataTransformation
from src.CineFlicx.components.data_validation import DataValidation



class TrainingPipeline:
    def __init__(self):
        self.data_ingestion=DataIngestion()
        self.data_validation=DataValidation()
        self.data_transformation=DataTransformation()
        



    def Train(self):
        self.data_ingestion.initiate_data_ingestion()
        self.data_validation.initiate_data_validation()
        self.data_transformation.initiate_data_transformation()
        