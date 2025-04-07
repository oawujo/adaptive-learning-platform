FROM node:18-alpine

WORKDIR /app

COPY deployment/frontend/package*.json ./
RUN npm install

COPY deployment/frontend/ .

# Build the static site
RUN npm run build

# Use a static web server to serve the build (Vite is dev-only)
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
