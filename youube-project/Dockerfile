# Stage 1: Build the React frontend
FROM node:18-slim as frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
COPY frontend/public/ ./public
COPY frontend/src/ ./src
RUN npm run build --legacy-peer-deps


# Stage 2: Build the Node.js backend
FROM node:18-slim as backend-builder

WORKDIR /app/backend

# Install FFmpeg and other necessary packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY backend/package*.json ./
RUN npm install

# Copy backend source code
COPY backend/server.js ./server.js
COPY backend/assets/ ./assets


# Stage 3: Combine frontend and backend into a single image
FROM node:18-slim

WORKDIR /app

# Install FFmpeg and other necessary packages for the final image
RUN apt-get update && apt-get install -y \
    ffmpeg \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy backend dependencies and source from backend-builder
COPY --from=backend-builder /app/backend/node_modules ./backend/node_modules
COPY --from=backend-builder /app/backend/server.js ./backend/server.js
COPY --from=backend-builder /app/backend/assets/ ./backend/assets

# Copy frontend build output from frontend-builder
COPY --from=frontend-builder /app/frontend/build ./backend/public_html # Renamed to avoid conflict

# Create storage directories
RUN mkdir -p backend/storage/audio backend/storage/videos

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables
ENV PORT=5000 \
    FFMPEG_PATH=/usr/bin/ffmpeg \
    FFPROBE_PATH=/usr/bin/ffprobe

# Command to run the backend server
CMD [ "node", "backend/server.js" ]
