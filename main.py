from src.CineFlicx.pipelines.training_pipeline import (
    TrainingPipeline
)

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)


# =====================================================
# TRAINING PIPELINE
# =====================================================

train_obj = TrainingPipeline()

train_obj.Train()


# =====================================================
# PREDICTION PIPELINE
# =====================================================

prediction_obj = PredictionPipeline()


# =====================================================
# COLLABORATIVE FILTERING
# =====================================================

collaborative_results = (
    prediction_obj.collaborative_pipeline(
        movie_title="Toy Story (1995)",
        top_k=5
    )
)

print("\n==============================")
print("Collaborative Recommendations")
print("==============================\n")

for movie in collaborative_results:

    print(movie)


# =====================================================
# SEMANTIC SEARCH
# =====================================================

semantic_results = (
    prediction_obj.semantic_pipeline(
        query="animated friendship adventure toys",
        top_k=5
    )
)

print("\n========================")
print("Semantic Recommendations")
print("========================\n")

for movie in semantic_results:

    print(movie)


# =====================================================
# HYBRID RECOMMENDATION
# =====================================================

hybrid_results = (
    prediction_obj.hybrid_pipeline(
        movie_title="Toy Story (1995)",
        query="animated adventure friendship",
        top_k=5
    )
)

print("\n======================")
print("Hybrid Recommendations")
print("======================\n")

for movie in hybrid_results:

    print(movie)