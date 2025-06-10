from sklearn.metrics.pairwise import cosine_similarity
import uuid
import logging
import os
COSINE_SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.8"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_or_create_theme(thesis_vec, existing_themes):
    highest_similarity = 0.0
    closest_theme_id = None

    for theme_id, vec in existing_themes.items():
        similarity = cosine_similarity([thesis_vec], [vec])[0][0]
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_theme_id = theme_id

    logger.info(f"Highest similarity: {highest_similarity:.4f} for theme_id: {closest_theme_id}")

    if highest_similarity >= COSINE_SIMILARITY_THRESHOLD:
        return closest_theme_id
    else:
        return str(uuid.uuid4())
