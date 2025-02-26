# Use an official Node.js image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package files first (better for caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy frontend source files
COPY . .

# Expose frontend port
EXPOSE 3000

# Start frontend
CMD ["npm", "start"]
