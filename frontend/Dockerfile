FROM node:22-slim

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .

RUN npm run build

# A prévia estática evita depender do WebSocket de HMR fora do ambiente de desenvolvimento.
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
