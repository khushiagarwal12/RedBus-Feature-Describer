# RedBus-Feature-Describer
![image](https://github.com/user-attachments/assets/7d163964-119d-4de8-a7ea-292533d9168b)

RedBus Feature Describer is a web-based tool that leverages a multimodal LLM to analyze and describe the features of the RedBus mobile app from screenshots. 
Users can upload screenshots of the app, provide optional context, and receive detailed descriptions of the app's functionalities, user interactions, and potential edge cases. 

## Overview

The RedBus Feature Describer is a tool that uses a multimodal LLM to describe features of the RedBus mobile app based on screenshots. It provides detailed descriptions of app features, user interactions, and potential edge cases.

## Features

- Upload screenshots of the RedBus app.
- Optional context box for additional information.
- Describes app features including functionality, user interactions, and edge cases.
- Filters and analyzes screenshots to ensure they are from the RedBus app.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Required Python packages listed in `backend/requirements.txt`

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/RedBus-Feature-Describer.git
    ```

2. **Navigate to the `backend` directory and install dependencies:**

    ```bash
    cd RedBus-Feature-Describer/backend
    pip install -r requirements.txt
    ```

3. **Set up environment variables for API keys and other secrets.**

4. **Run the backend server:**

    ```bash
    python app.py
    ```

5. **Navigate to the `frontend` directory and ensure static files are correctly linked.**

### Usage

1. **Open the frontend interface in your browser:**

    Access it at `http://localhost:5000`.

2. **Upload a screenshot of the RedBus app.**

3. **Provide optional context if needed.**

4. **Click 'Describe Features' to get detailed descriptions of app features.**


### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
