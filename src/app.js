const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const dotenv = require('dotenv');

dotenv.config();

const app = express();

app.use(express.static('public'));

const server = http.createServer(app);

const wss = new WebSocket.Server({ server });

const rateLimit = (ws, limit, period) => {
  let messageCount = 0;
  const resetInterval = setInterval(() => {
    messageCount = 0;
  }, period);

  ws.on('close', () => {
    clearInterval(resetInterval);
  });

  return (callback) => {
    if (messageCount < limit) {
      messageCount++;
      callback();
    } else {
      console.log('Rate limit exceeded. Message skipped.');
      ws.send(JSON.stringify({ error: 'Rate limit exceeded. Please try again later.' }));
    }
  };
};

wss.on('connection', (ws) => {
  console.log('Client connected');

  const checkRateLimit = rateLimit(ws, 5, 10000);

  ws.on('message', function incoming(data) {
    checkRateLimit(() => {
      console.log('Message from client:', data);

      ws.send(`Echo from server: ${data}`);
    });
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});