# Set the base image to Node 18
FROM node:18

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY package*.json /app/

# Install any needed packages specified in package.json
RUN npm install

# Copy the current directory contents into the container at /app
COPY index.js /app/

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run app.js when the container launches
CMD ["node", "index.js"]