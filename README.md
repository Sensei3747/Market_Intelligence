# Assessment1: Social Media Data Analysis

This project focuses on analyzing social media data from various platforms (Facebook, Google, TikTok, and general business data) to extract insights, perform sentiment analysis, and visualize trends. It leverages AI models for deeper insights and provides a dashboard for interactive exploration.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [AI Insights](#ai-insights)
- [Analysis & Visualization](#analysis--visualization)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Assessment1.git
    cd Assessment1
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

After installation, you can run the main application or explore specific components.

To run the main application (if `app.py` is the entry point):

```bash
python app.py
```

Further instructions for specific modules or notebooks will be provided within their respective directories.

## Project Structure

-   `app.py`: The main application entry point.
-   `config.py`: Configuration settings for the project.
-   `requirements.txt`: Lists all project dependencies.
-   `dataset/`: Contains the raw social media data files.
    -   `business.csv`
    -   `Facebook.csv`
    -   `Google.csv`
    -   `TikTok.csv`
-   `notebooks/`: Jupyter notebooks for exploratory data analysis, model development, and experimentation.
-   `src/`: Source code for the project.
    -   `ai/`: Modules related to AI models and insights.
        -   `ai_insights.py`: Logic for generating AI-driven insights.
        -   `llm_service.py`: Service for interacting with Large Language Models.
    -   `analysis/`: Modules for data analysis and processing.
    -   `data/`: Modules for data ingestion, cleaning, and preprocessing.
        -   `data_processor.py`: Handles data loading and initial processing.
    -   `utils/`: Utility functions and helper scripts.
    -   `visualization/`: Modules for data visualization and dashboard components.
        -   `dashboard_components.py`: Reusable components for the data dashboard.

## Dataset

The `dataset/` directory contains CSV files with social media data:

-   `business.csv`: General business-related data.
-   `Facebook.csv`: Data specifically from Facebook.
-   `Google.csv`: Data specifically from Google.
-   `TikTok.csv`: Data specifically from TikTok.

## AI Insights

The `src/ai/` directory houses the components responsible for generating insights using artificial intelligence, including interactions with Large Language Models.

## Analysis & Visualization

Data analysis modules are located in `src/analysis/`, while `src/visualization/` contains code for creating interactive dashboards and visual representations of the data.

## Contributing

Contributions are welcome! Please refer to the contributing guidelines (if any) for more information.

## License

This project is licensed under the [MIT License](LICENSE.md) - see the `LICENSE.md` file for details.