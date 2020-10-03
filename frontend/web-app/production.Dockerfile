FROM node:lts-alpine

# Install an HTTP server to serve the static app
RUN npm install -g http-server

# Set the app's working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install the dependencies
RUN yarn install

# Copy the app files
COPY . .

# Enable the production environment variables file
RUN mv env.production.rename .env.production

# Build the static app
RUN yarn build

# Expose the internal HTTP server
EXPOSE 3000

# Run the HTTP server
CMD [ "http-server", "-p", "3000", "dist" ]