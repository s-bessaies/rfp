FROM node:18-bullseye

WORKDIR /app

COPY package.json /app/
COPY package-lock.json /app/
RUN npm install --legacy-peer-deps

COPY . /app/



CMD ["npm", "start"]
