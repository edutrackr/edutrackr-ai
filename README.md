# Edutrack AI

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:
- [Python](https://www.python.org/downloads/)
- [CMake](https://cmake.org/download/) (this is required for installing `dlib`)

### Setup

> We recommend using a virtual environment for this project. Use the following command to create a virtual environment: `python -m venv .venv`

1. Clone the repository
2. Install the required packages using `pip install -r requirements.txt`
3. Configure the project environment variables in the `.env` file (see the `.env.example` file for reference)

## API

### Development

To run the API in development mode, run the following command:

```bash
uvicorn main:app --reload
```

> To open the API documentation, go to `http://localhost:8000/docs` (change the port number if necessary).

### Deployment

To run the API, run the following command:

```bash
uvicorn main:app
```

> To open the API documentation, go to `http://<base_url>/docs`.

## Project Structure

The project is divided into the following sub-directories:
- `algorithms`: Contains the logic for the AI algorithms used in the project.
- `api`: Contains the logic for the Web API.
- `resources`: Contains the static resources used in the project.
- `samples`: Contains the sample code for testing the models using the webcam.
- `video_samples`: Contains the sample videos for testing the models.
