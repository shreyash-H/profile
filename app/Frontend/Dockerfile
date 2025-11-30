FROM node:18-alpine AS build
WORKDIR /app
COPY app/frontend/package*.json ./
RUN npm ci --silent
COPY app/frontend/ ./
RUN npm run build
FROM node:18-alpine AS runtime
WORKDIR /app
RUN npm install -g serve@14.2.0
COPY --from=build /app/build /app/build
ENV PORT=3000
EXPOSE 3000
CMD ["serve","-s","build","-l","3000"]
