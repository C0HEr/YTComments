# Real-time YouTube Comment Sentiment Analysis

This project performs real-time sentiment analysis on YouTube comments using Kafka, Spark, Docker, and Streamlit. It processes YouTube comments to determine the sentiment (positive, neutral, or negative) and visualizes the results in a web interface.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [License](#license)

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Python 3.9](https://www.python.org/)
- [Streamlit](https://streamlit.io/)

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/C0HEr/YTComments.git
   cd YTComments

2. **Build and start Docker containers:**
    The project uses Docker to manage services like Kafka, Spark. Use the following command to start them:
    
    ```bash
    docker-compose up --build

    This command will:
    - Build the necessary Docker images for your services.
    - Start the Kafka, Spark, and Streamlit services

    After the services start, you can access the Streamlit dashboard at http://localhost:8501.

3. **Project Structure:**
    ```bash
    ├── app/
    │   ├── spark.py              # Spark job for processing comments and performing sentiment analysis
    │   ├── kafka.py              # Kafka producer and consumer setup
    ├── dashboard.py              # Streamlit dashboard for visualizing sentiment analysis results
    ├── docker-compose.yml        # Docker configuration for Kafka, Spark, Zookeeper, and Streamlit
    ├── Dockerfile                # Dockerfile for building the Streamlit app container
    ├── requirements.txt          # Python dependencies
    ├── README.md                 # Project documentation (this file)
    ```

### Explanation of Key Files:
- **`app/spark.py`**: Contains the Spark logic for reading from Kafka, processing the comments, and performing sentiment analysis.
- **`app/kafka.py`**: Kafka producer/consumer logic for handling comment streams.
- **`dashboard.py`**: The Streamlit application that visualizes the processed sentiment data.
- **`docker-compose.yml`**: Defines the multi-container setup for Kafka, Spark, Zookeeper, and Streamlit services.
- **`Dockerfile`**: Builds the Docker image for the Streamlit application.
- **`requirements.txt`**: Lists the Python libraries needed for the project.
                
## Technologies Used
- **Kafka**: Message broker for real-time comment ingestion.
- **Apache Spark**: For processing and analyzing YouTube comments.
- **Streamlit**: To create an interactive web dashboard to display sentiment analysis results.
- **Docker**: To containerize all the services and make deployment easier.


### Instructions:
1. **Replace placeholders** (like `C0HEr` and `YTComments`) with actual values.
2. **Ensure your Docker and Python setup matches** the instructions in the file.
3. **List your project on GitHub** with this full `README.md`.


