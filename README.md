# 🧠 Claudron Insight Extractor

A lightweight FastAPI service that ingests RSS feeds, extracts thesis-level insights using NLP, clusters them into thematic groups, and stores the results in Neo4j for semantic querying and timeline generation.

---

## 📘 Why Neo4j?

We use **Neo4j**, a graph database, because it enables efficient storage and querying of complex relationships between content, ideas, and themes — something that would be cumbersome with traditional relational databases.

### 🔗 Key reasons:

-   **Natural Graph Structure**: Posts contain multiple theses, and theses belong to themes. This 3-level structure maps cleanly to a graph:
    -   `(Post)-[:HAS_THESIS]->(Thesis)-[:BELONGS_TO]->(Theme)`
-   **Semantic Connectivity**: Enables graph traversal queries like:
    -   "Show all thesis statements under a theme"
    -   "Trace a theme's evolution over time"
-   **Performance**: Graph databases outperform SQL for deep-link queries (e.g., `k`-hop relationships) due to index-free adjacency.

### 📊 Metrics that benefit from Neo4j:
-   Time-series trends of content under a theme
-   Post counts per theme over time
-   Semantic density or node degree of a theme (how many theses connect to it)
-   Clustering coefficient to identify highly connected thematic pockets
-   Query latency when resolving related content across layers (theses → themes → posts)

---

## 📦 Features

-   🌐 Ingests blog/news articles via RSS feeds  
-   🧠 Extracts key thesis sentences using Sentence Transformers  
-   🔗 Clusters thesis statements based on semantic similarity (cosine distance)  
-   🕸️ Persists content and relationships in a Neo4j graph  
-   📊 Provides REST endpoints for querying themes and timelines  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/claudron-insight-extractor.git](https://github.com/yourusername/claudron-insight-extractor.git)
cd claudron-insight-extractor

2. Create and Activate Virtual Environment
python -m venv claudron
source claudron/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Environment Variables
Create a .env file in the root directory:

# Neo4j connection settings
NEO4J_URI="neo4j+s://your-neo4j-endpoint.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your-secure-password"
NEO4J_DATABASE="neo4j"

# Number of top thesis sentences to extract from each post
# Set TOP_THEMES=-1 to use all sentences, or a positive integer like 2 or 5
TOP_THEMES=2

5. Run the App
uvicorn app.main:app --reload

Visit: http://localhost:8000/docs for interactive Swagger UI documentation.

🧪 API Endpoints
POST /ingest
Ingests content from an RSS feed.

Body:

{
  "feed_url": "[https://example.com/rss](https://example.com/rss)"
}

GET /themes
Returns a list of all themes and the number of theses in each.

GET /themes/{theme_id}
Returns a timeline of thesis statements and their source posts under the given theme.

🐳 Docker Support (Optional)
Make sure Docker is installed and running.
Add a Dockerfile and docker-compose.yml if not present.

Run the app using:

docker-compose up --build

You can optionally connect to a remote Neo4j instance (e.g., AuraDB) instead of running Neo4j inside Docker. Just ensure your .env has correct external credentials.

✅ Example Feeds to Test With
[https://www.theverge.com/rss/index.xml](https://www.theverge.com/rss/index.xml)
[https://www.technologyreview.com/feed/](https://www.technologyreview.com/feed/)
[https://feeds.feedburner.com/oreilly/radar/atom](https://feeds.feedburner.com/oreilly/radar/atom)

🧼 Maintenance
To delete all data from Neo4j:

MATCH (n) DETACH DELETE n;
