import logging
from fastapi import FastAPI, Body
from app import rss, nlp, clustering
from app.db import Neo4jClient
from datetime import datetime
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
neo4j = Neo4jClient()


@app.post("/ingest")
def ingest_feed(feed_url: str = Body(...)):
    logger.info(f"Starting ingestion for feed: {feed_url}")
    
    entries = rss.fetch_feed(feed_url)
    logger.info(f"Fetched {len(entries)} entries from feed.")

    existing_urls = neo4j.fetch_all_post_urls()
    logger.info(f"{len(existing_urls)} posts already in DB.")

    new_posts = 0

    for entry in entries:
        if entry.link in existing_urls:
            logger.info(f"Skipping already ingested post: {entry.link}")
            continue

        sentences = entry.summary.split(". ")
        thesis_sentences = nlp.extract_thesis(sentences)
        logger.info(f"Extracted {len(thesis_sentences)} thesis sentences.")

        vectors = nlp.model.encode(thesis_sentences)
        logger.info("Generated embeddings.")

        existing = neo4j.fetch_all_theses()
        theme_map = {
            th["theme_id"]: th["embedding"]
            for th in existing if th.get("embedding")
        }

        theses_with_themes = []
        for text, vec in zip(thesis_sentences, vectors):
            theme_id = clustering.find_or_create_theme(vec, theme_map)
            theses_with_themes.append({
                "text": text,
                "theme_id": theme_id,
                "embedding": vec.tolist()
            })

        post = {
            "url": entry.link,
            "title": entry.title,
            "published_at": datetime(*entry.published_parsed[:6]).isoformat(),
            "ingested_at": datetime.utcnow().isoformat()
        }

        neo4j.ingest_post(post, theses_with_themes)
        logger.info(f"Ingested post: {entry.title} ({entry.link}) with {len(theses_with_themes)} theses.")
        new_posts += 1

    logger.info(f"Ingestion complete. {new_posts} new posts ingested.")

    return {"status": "ok", "new_posts": new_posts}


@app.get("/themes")
def get_themes():
    logger.info("Fetching all themes from DB.")
    return neo4j.get_all_themes()


@app.get("/themes/{theme_id}")
def get_theme_timeline(theme_id: str):
    logger.info(f"Fetching timeline for theme_id: {theme_id}")
    return neo4j.get_theme_timeline(theme_id)