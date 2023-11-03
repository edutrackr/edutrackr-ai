# Edutrack AI

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:
- [Python](https://www.python.org/downloads/)
- [CMake](https://cmake.org/download/) (required for installing `dlib`)
- [FFmpeg](https://ffmpeg.org/download.html) (required for installing `ffmpeg-python`)

### Setup

> We recommend using a virtual environment for this project. Use the following command to create a virtual environment: `python -m venv .venv`

1. Clone the repository
2. Install the required packages using `pip install -r requirements.txt`
3. Configure the project environment variables in the `.env` file (see the `.env.example` file for reference). This configuration will only be used in development mode.

## API

### Development

To run the API in development mode, run the following command:

```bash
python main.py --dev
```

> To open the API documentation, go to `http://localhost:8000/docs` (change the port number if necessary).

To run the API in development mode with auto-reload, run the following command:

```bash
python main.py --dev --watch
```

> Reading environment variables from `.env` file and auto-reload are only available in development mode.

### Deployment

To run the API, run the following command:

```bash
python main.py
```

> To open the API documentation, go to `http://<base_url>/docs`.

## Samples

To run any AI sample, run the following command:

```bash
python <sample_name>.py --dev
```

> To run the sample in development mode, add the `--dev` flag in order to read the environment variables from the `.env` file.

## Project Structure

The project is divided into the following sub-directories:
- `api`: Contains the logic for the Web API.
- `resources`: Contains the static resources used in the project.
- `samples`: Contains the sample code for testing the AI models.
- `tests`: Contains the unit tests for the project.
