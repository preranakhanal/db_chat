# --- Build Stage ---
FROM node:18 AS builder
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production deps
RUN npm ci --omit=dev

# Copy source files
COPY . .

# Build frontend
RUN npm run build

# --- Run Stage ---
FROM node:18-alpine AS runner
WORKDIR /app

# Copy everything from builder stage
COPY --from=builder /app /app

EXPOSE 3000
CMD ["npm", "start"]