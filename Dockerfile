# Pull base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /MovieShelf

# Install dependencies
COPY requirements.txt /MovieShelf/
RUN pip install -r requirements.txt

# Copy project
COPY . /MovieShelf/