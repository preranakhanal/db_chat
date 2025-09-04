

FROM node:20-alpine AS runner
WORKDIR /app

# Copy package files and source
COPY package*.json ./
COPY public ./public
COPY next.config.mjs ./next.config.mjs
COPY . .

# Install dependencies and build
RUN npm install --omit=dev && npm run build

# Optionally copy .env if present (ignore error if missing)
COPY .env ./.env

EXPOSE 3000
CMD ["npm", "start"]