# Use an official Python runtime as a parent image
FROM python:3.11.14-trixie

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src

# Run Python script when the container launches
CMD ["python", "-m", "src.ui.test_ui"]