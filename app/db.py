from neo4j import GraphDatabase
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class Neo4jClient:
    def __init__(self):
        uri = os.environ["NEO4J_URI"]
        user = os.environ["NEO4J_USERNAME"]
        password = os.environ["NEO4J_PASSWORD"]

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def ingest_post(self, post: Dict[str, Any], theses_with_themes: List[Dict[str, Any]]):
        def add_post(tx, post, theses):
            tx.run("""
                MERGE (p:Post {url: $url})
                  ON CREATE SET p.title = $title, p.published_at = $published_at, p.ingested_at = $ingested_at
                WITH p
                UNWIND $theses as t
                  MERGE (th:Thesis {text: t.text})
                  ON CREATE SET th.embedding = t.embedding
                  MERGE (theme:Theme {id: t.theme_id})
                  MERGE (p)-[:HAS_THESIS]->(th)
                  MERGE (th)-[:BELONGS_TO]->(theme)
            """, {
                "url": post["url"],
                "title": post["title"],
                "published_at": post["published_at"],
                "ingested_at": post["ingested_at"],
                "theses": [
                    {
                        "text": th["text"],
                        "theme_id": th["theme_id"],
                        "embedding": th["embedding"]
                    } for th in theses
                ]
            })

        with self.driver.session() as session:
            session.execute_write(add_post, post, theses_with_themes)

    def fetch_all_theses(self) -> List[Dict[str, Any]]:
        def get_all(tx):
            result = tx.run("""
                MATCH (th:Thesis)-[:BELONGS_TO]->(theme:Theme)
                RETURN th.text AS thesis_text, th.embedding AS embedding, theme.id AS theme_id
            """)
            return [{"text": r["thesis_text"], "embedding": r["embedding"], "theme_id": r["theme_id"]} for r in result]

        with self.driver.session() as session:
            return session.execute_read(get_all)

    def fetch_all_post_urls(self) -> List[str]:
        def get_urls(tx):
            result = tx.run("MATCH (p:Post) RETURN p.url AS url")
            return [r["url"] for r in result]

        with self.driver.session() as session:
            return session.execute_read(get_urls)

    def get_all_themes(self) -> List[Dict[str, Any]]:
        def query(tx):
            result = tx.run("""
                MATCH (t:Thesis)-[:BELONGS_TO]->(theme:Theme)
                RETURN theme.id AS theme_id, count(t) AS post_count
            """)
            return [{"theme_id": r["theme_id"], "post_count": r["post_count"]} for r in result]

        with self.driver.session() as session:
            return session.execute_read(query)

    def get_theme_timeline(self, theme_id: str) -> List[Dict[str, Any]]:
        def query(tx):
            result = tx.run("""
                MATCH (th:Thesis)-[:BELONGS_TO]->(theme:Theme {id: $theme_id})<-[:BELONGS_TO]-(th2)<-[:HAS_THESIS]-(p:Post)
                RETURN th2.text AS thesis_text, p.title AS post_title, p.url AS post_url, p.published_at AS published_at
                ORDER BY p.published_at
            """, {"theme_id": theme_id})
            return [dict(record) for record in result]

        with self.driver.session() as session:
            return session.execute_read(query)
