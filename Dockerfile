

FROM node:20-alpine AS runner
WORKDIR /app

# Copy package files and source
COPY package*.json ./
COPY public ./public
COPY next.config.mjs ./next.config.mjs
COPY . .

# Install dependencies and build
RUN npm install && npm run build

EXPOSE 3000
CMD ["npm", "start"]