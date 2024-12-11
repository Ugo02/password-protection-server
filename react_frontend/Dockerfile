# Use an official Node.js runtime as a base image
FROM node:14-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Set environment variables so the app runs on port 3001 and listens on all interfaces
ENV PORT=3001
ENV HOST=0.0.0.0

# Expose port 3001
EXPOSE 3001

# Start the React application
CMD ["npm", "start"]
