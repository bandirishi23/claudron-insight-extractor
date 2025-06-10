# RSS Feed Analysis and Theme Clustering System

A FastAPI-based application that ingests RSS feeds, extracts key theses from articles, and clusters them into themes using natural language processing and machine learning techniques.

## Features

- RSS feed ingestion and parsing
- Natural Language Processing (NLP) for thesis extraction
- Semantic clustering of theses into themes
- Neo4j graph database integration for data persistence
- RESTful API endpoints for data access
- Docker containerization support

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
git clone <repository-url>
cd <repository-name>
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

1. **Enhanced NLP**:
   - Implement more sophisticated thesis extraction algorithms
   - Add support for multiple languages
   - Improve theme clustering accuracy
   - Add sentiment analysis for theses

2. **Scalability Improvements**:
   - Add caching layer for frequently accessed data
   - Implement rate limiting for API endpoints
   - Add support for batch processing of feeds
   - Implement pagination for large result sets

3. **Feature Additions**:
   - User authentication and authorization
   - Custom theme creation and management
   - Advanced search capabilities
   - Analytics dashboard
   - Webhook support for real-time updates
   - Theme evolution tracking over time

4. **Monitoring and Maintenance**:
   - Add comprehensive metrics collection
   - Implement automated testing
   - Add health check endpoints
   - Improve error handling and recovery
   - Add database migration tools

5. **Performance Optimization**:
   - Implement connection pooling for Neo4j
   - Add background task processing
   - Optimize embedding generation and storage
   - Implement efficient caching strategies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the terms of the included LICENSE file.

