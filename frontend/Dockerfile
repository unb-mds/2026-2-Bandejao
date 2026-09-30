FROM node:22-slim

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .

ARG VITE_API_BASE_URL=http://localhost:8000
RUN npm run build

# A prévia estática evita depender do WebSocket de HMR fora do ambiente de desenvolvimento.
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
