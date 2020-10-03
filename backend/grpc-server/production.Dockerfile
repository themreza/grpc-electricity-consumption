# Base image
FROM python:3.8

# Install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code
COPY src/ ./src

# Copy the data
COPY data/ ./data

# Set the working directory
WORKDIR /src

# Run the unit tests
RUN ["python", "server_test.py"]

# Expose the server port
EXPOSE 9090

# Run the gRPC server
CMD ["python", "server.py"]