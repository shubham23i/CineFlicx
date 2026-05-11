from src.CineFlicx.components.data_ingestion import DataIngestion



class TrainingPipeline:
    def __init__(self):
        self.data_ingestion=DataIngestion()



    def Train(self):
        self.data_ingestion.initiate_data_ingestion()