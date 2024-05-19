FROM node

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

EXPOSE 3040


CMD ["npm", "start"]