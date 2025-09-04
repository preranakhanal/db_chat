

FROM node:20-alpine AS runner
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Copy build output and config
COPY .next ./.next
COPY public ./public
COPY next.config.mjs ./next.config.mjs
# Copy .env if it exists
COPY .env ./.env

EXPOSE 3000
CMD ["npm", "start"]