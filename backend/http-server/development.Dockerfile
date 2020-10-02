# Base image
FROM python:3.8

# Install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# In the development Dockerfile, files are mounted rather than copied to avoid unnecessary image builds

# Set the working directory
WORKDIR /src

# Expose the server port
EXPOSE 8080

# Run the gRPC server
CMD ["python", "server.py"]