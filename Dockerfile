# Use official Node
FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
COPY pnpm-lock.yaml* ./

RUN npm install -g pnpm

# Install only prod deps in build
RUN pnpm install --frozen-lockfile --prod

COPY . .

RUN pnpm build

# Run with a smaller final image (optional)
FROM node:18-alpine AS runner
WORKDIR /app

COPY --from=builder /app ./

EXPOSE 3000
CMD ["pnpm", "start"]