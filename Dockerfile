# Use an official Node.js runtime as a base image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) first to leverage Docker cache
# A wildcard is used to ensure both package.json and package-lock.json are copied.
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (e.g., 3000, 8080)
EXPOSE 3000

# Define the command to run the application
CMD ["npm", "start"]
