# Use an official Node.js runtime as a parent image
FROM node:18-slim

# Set the working directory to /app
WORKDIR /app

# Install FFmpeg and other necessary packages
# This is crucial for the video generation to work inside the container
RUN apt-get update && apt-get install -y \
    ffmpeg \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy package.json and package-lock.json (if available)
COPY backend/package*.json .

# Install dependencies
RUN npm install

# Copy the rest of the backend source code
COPY backend/ .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables (can be overridden at runtime)
ENV PORT=5000 \
    FFMPEG_PATH=/usr/bin/ffmpeg \
    FFPROBE_PATH=/usr/bin/ffprobe

# Run the backend server
CMD [ "node", "server.js" ]