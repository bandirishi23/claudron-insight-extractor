\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{geometry}

% Adjust margins for better readability
\geometry{a4paper, margin=1in}

% Custom colors for code highlighting
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

% Listing style for code blocks
\lstset{
  backgroundcolor=\color{backcolour},
  commentstyle=\color{codegreen},
  keywordstyle=\color{magenta},
  numberstyle=\tiny\color{codegray},
  stringstyle=\color{codepurple},
  basicstyle=\ttfamily\footnotesize,
  breakatwhitespace=false,
  breaklines=true,
  captionpos=b,
  keepspaces=true,
  numbers=none, % No line numbers
  numbersep=5pt,
  showspaces=false,
  showstringspaces=false,
  showtabs=false,
  tabsize=2
}

\title{\textbf{Claudron Insight Extractor}}
\author{}
\date{}

\begin{document}

\maketitle

\begin{abstract}
A lightweight FastAPI service that ingests RSS feeds, extracts thesis-level insights using NLP, clusters them into thematic groups, and stores the results in Neo4j for semantic querying and timeline generation.
\end{abstract}

---

\section*{Why Neo4j?}

We use \textbf{Neo4j}, a graph database, because it enables efficient storage and querying of complex relationships between content, ideas, and themes --- something that would be cumbersome with traditional relational databases.

\subsection*{Key Reasons:}

\begin{itemize}
    \item \textbf{Natural Graph Structure}: Posts contain multiple theses, and theses belong to themes. This 3-level structure maps cleanly to a graph:
    \begin{itemize}
        \item \texttt{(Post)-[:HAS\_THESIS]->(Thesis)-[:BELONGS\_TO]->(Theme)}
    \end{itemize}
    \item \textbf{Semantic Connectivity}: Enables graph traversal queries like:
    \begin{itemize}
        \item "Show all thesis statements under a theme"
        \item "Trace a theme's evolution over time"
    \end{itemize}
    \item \textbf{Performance}: Graph databases outperform SQL for deep-link queries (e.g., $k$-hop relationships) due to index-free adjacency.
\end{itemize}

\subsection*{Metrics that benefit from Neo4j:}

\begin{itemize}
    \item Time-series trends of content under a theme
    \item Post counts per theme over time
    \item Semantic density or node degree of a theme (how many theses connect to it)
    \item Clustering coefficient to identify highly connected thematic pockets
    \item Query latency when resolving related content across layers (theses $\rightarrow$ themes $\rightarrow$ posts)
\end{itemize}

---

\section*{Features}

\begin{itemize}
    \item \textbf{🌐 Ingests blog/news articles via RSS feeds}
    \item \textbf{🧠 Extracts key thesis sentences using Sentence Transformers}
    \item \textbf{🔗 Clusters thesis statements based on semantic similarity (cosine distance)}
    \item \textbf{🕸️ Persists content and relationships in a Neo4j graph}
    \item \textbf{📊 Provides REST endpoints for querying themes and timelines}
\end{itemize}

---

\section*{Getting Started}

\subsection*{1. Clone the Repository}
\begin{lstlisting}[language=bash]
git clone https://github.com/yourusername/claudron-insight-extractor.git
cd claudron-insight-extractor
\end{lstlisting}

\subsection*{2. Create and Activate Virtual Environment}
\begin{lstlisting}[language=bash]
python -m venv claudron
source claudron/bin/activate
\end{lstlisting}

\subsection*{3. Install Dependencies}
\begin{lstlisting}[language=bash]
pip install -r requirements.txt
\end{lstlisting}

\subsection*{4. Set Environment Variables}
Create a \texttt{.env} file in the root directory:
\begin{lstlisting}[language=bash]
# Neo4j connection settings
NEO4J_URI="neo4j+s://your-neo4j-endpoint.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your-secure-password"
NEO4J_DATABASE="neo4j"

# Number of top thesis sentences to extract from each post
# Set TOP_THEMES=-1 to use all sentences, or a positive integer like 2 or 5
TOP_THEMES=2
\end{lstlisting}

\subsection*{5. Run the App}
\begin{lstlisting}[language=bash]
uvicorn app.main:app --reload
\end{lstlisting}
Visit: \url{http://localhost:8000/docs} for interactive Swagger UI documentation.

\subsection*{API Endpoints}

\subsubsection*{POST /ingest}
Ingests content from an RSS feed.
\begin{lstlisting}[language=json]
Body:
{
  "feed_url": "https://example.com/rss"
}
\end{lstlisting}

\subsubsection*{GET /themes}
Returns a list of all themes and the number of theses in each.

\subsubsection*{GET /themes/\{theme\_id\}}
Returns a timeline of thesis statements and their source posts under the given theme.

\subsection*{Docker Support (Optional)}
Make sure Docker is installed and running.
Add a \texttt{Dockerfile} and \texttt{docker-compose.yml} if not present.

Run the app using:
\begin{lstlisting}[language=bash]
docker-compose up --build
\end{lstlisting}
You can optionally connect to a remote Neo4j instance (e.g., AuraDB) instead of running Neo4j inside Docker. Just ensure your \texttt{.env} has correct external credentials.

\subsection*{Example Feeds to Test With}
\begin{itemize}
    \item \url{https://www.theverge.com/rss/index.xml}
    \item \url{https://www.technologyreview.com/feed/}
    \item \url{https://feeds.feedburner.com/oreilly/radar/atom}
\end{itemize}

\subsection*{Maintenance}
To delete all data from Neo4j:
\begin{lstlisting}[language=cypher]
MATCH (n) DETACH DELETE n;
\end{lstlisting}

\end{document}
