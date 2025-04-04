# Use Node.js for building the React frontend
FROM node:18-alpine AS build
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Serve the built frontend
FROM nginx:alpine
# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]