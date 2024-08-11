# Description: Dockerfile for the python application
FROM python:3.12.5-alpine


# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your Flask app will run on
EXPOSE 5000


# Command to run your app
CMD ["python", "run.py"]
