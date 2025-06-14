# RSS Feed Analysis and Theme Clustering System

A FastAPI-based application that ingests RSS feeds, extracts key theses from articles, and clusters them into themes using natural language processing and machine learning techniques.

---

## Why Neo4j?

We use **Neo4j**, a graph database, because it enables efficient storage and querying of complex relationships between content, ideas, and themes — something that would be cumbersome with traditional relational databases.

### Key reasons:

-   **Natural Graph Structure**: Posts contain multiple theses, and theses belong to themes. This 3-level structure maps cleanly to a graph:
    -   `(Post)-[:HAS_THESIS]->(Thesis)-[:BELONGS_TO]->(Theme)`
-   **Semantic Connectivity**: Enables graph traversal queries like:
    -   "Show all thesis statements under a theme"
    -   "Trace a theme's evolution over time"
-   **Performance**: Graph databases outperform SQL for deep-link queries (e.g., `k`-hop relationships) due to index-free adjacency.

###  Metrics that benefit from Neo4j:
-   Time-series trends of content under a theme
-   Post counts per theme over time
-   Semantic density or node degree of a theme (how many theses connect to it)
-   Clustering coefficient to identify highly connected thematic pockets
-   Query latency when resolving related content across layers (theses → themes → posts)

---

##  Features

-    Ingests blog/news articles via RSS feeds  
-    Extracts key thesis sentences using Sentence Transformers  
-    Clusters thesis statements based on semantic similarity (cosine distance)  
-    Persists content and relationships in a Neo4j graph  
-    Provides REST endpoints for querying themes and timelines  


## Tech Stack

- **Backend Framework**: FastAPI
- **NLP**: Sentence Transformers
- **Database**: Neo4j
- **Machine Learning**: scikit-learn
- **RSS Processing**: feedparser
- **Containerization**: Docker

## Prerequisites

- Python 3.8+
- Neo4j Database
- Docker and Docker Compose (for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bandirishi23/culldron-insight-extractor.git
cd culldron-insight-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
NEO4J_URI=<your-neo4j-uri>
NEO4J_USERNAME=<your-neo4j-username>
NEO4J_PASSWORD=<your-neo4j-password>

# Set TOP_THEMES=-1 to use all sentences, or a positive integer like 2 or 5. (Default is 2)
TOP_THEMES=2
# Sets up the cosine similarity, use a float value between 0 and 1 (Defaults to 0.8)
SIMILARITY_THRESHOLD=0.80
```

## Running the Application

### Local Development

1. Start the Neo4j database (if running locally)
2. Run the FastAPI application:
```bash
uvicorn app.main:app --reload
```

### Docker Deployment

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

### After running your FastAPI app, visit:

Swagger UI: http://localhost:8000/docs,
ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /ingest
Ingest a new RSS feed for processing.
- **Input**: Feed URL
- **Output**: Status and number of new posts ingested

### GET /themes
Retrieve all identified themes.
- **Output**: List of themes with their metadata

### GET /themes/{theme_id}
Get timeline of posts for a specific theme.
- **Input**: Theme ID
- **Output**: Chronological list of posts associated with the theme


## Design Decisions

1. **NLP Pipeline**:
   - Uses Sentence Transformers for generating semantic embeddings
   - Extracts thesis statements from article summaries
   - Employs clustering to group similar theses into themes

2. **Database Choice**:
   - Neo4j was chosen for its graph database capabilities
   - Enables efficient storage and querying of relationships between posts, theses, and themes
   - Supports complex timeline queries and relationship traversal

3. **API Design**:
   - RESTful architecture for clear resource management
   - Asynchronous processing for feed ingestion
   - Comprehensive logging for monitoring and debugging

4. **Data Model**:
   - Posts: Represent articles with metadata (URL, title, publication date)
   - Theses: Key statements extracted from articles with embeddings
   - Themes: Clusters of related theses
   - Relationships: Posts -> Theses -> Themes

## Future Work

1. **Smarter NLP**:
   - Enhance thesis extraction with advanced algorithms and multilingual support
   - Improve clustering quality and add sentiment insights to theses

2. **Scalability Improvements**:
   - Add caching layer for frequently accessed data
   - Implement rate limiting for API endpoints


3. **Feature Additions**:
   - User authentication and authorization
   - Advanced search capabilities
   - Analytics dashboard


4. **Monitoring and Maintenance**:
   - Add comprehensive metrics collection
   - Add health check endpoints


5. **Performance Optimization**:
   - Implement connection pooling for Neo4j
   - Add background task processing


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the terms of the included LICENSE file.

