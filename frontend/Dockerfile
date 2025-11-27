# Multi-stage Dockerfile for React frontend
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install all dependencies (including devDependencies needed for build)
# This layer will be cached if package files don't change
RUN npm ci --no-audit --no-fund

# Copy source code
COPY . .

# Build arguments for environment-specific configuration
ARG REACT_APP_API_BASE_URL=http://localhost:8000
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL

# Build the React application
RUN npm run build

# Stage 2: Production with nginx
FROM nginx:alpine

# Copy built static files from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check using nginx's built-in capabilities
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Start nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]

