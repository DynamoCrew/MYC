# Use an official Python runtime as a parent image
FROM python:3.10.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=iris_scrapper.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
