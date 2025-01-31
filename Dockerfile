#base image
FROM python:3.10

WORKDIR /usr/src/app

# Create a folder for persistent storage
RUN mkdir -p /usr/src/app/data

# Copy everything into the container
COPY . /usr/src/app/

# Install dependencies
RUN pip install -r requirements.txt

# Set the entrypoint (modify based on your Scrapy setup)
CMD ["python", "main.py"]
