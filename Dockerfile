# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /

# Copy the requirements.txt file to the container
COPY ./requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

EXPOSE 4545

# Set the command to run when the container starts
CMD ["python", "/app/main.py"]
