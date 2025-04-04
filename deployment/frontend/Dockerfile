FROM node:18
WORKDIR /app
COPY deployment/frontend/package*.json ./
RUN npm install
COPY deployment/frontend/ .
RUN npm run build
CMD ["npm", "run", "dev"]