

FROM node:20-alpine AS runner
WORKDIR /app

# Copy only what's needed to serve the built app
COPY package*.json ./
COPY .next ./.next
COPY public ./public
COPY node_modules ./node_modules
COPY next.config.mjs ./next.config.mjs
COPY .env ./.env

EXPOSE 3000
CMD ["npm", "start"]