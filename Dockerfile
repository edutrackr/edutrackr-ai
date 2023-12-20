FROM python:3.10

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy source code
COPY . .

# Run the application
CMD ["python", "main.py"]
