const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(express.static('public'));

const httpServer = http.createServer(app);
const websocketServer = new WebSocket.Server({ server: httpServer });

const messageRateLimitCache = new Map();

const enforceRateLimit = (websocket, messagesAllowed, periodMs) => {
  let cacheEntry = messageRateLimitCache.get(websocket);
  
  if (!cacheEntry) {
    cacheEntry = { messageCount: 0, resetTimer: null };
    messageRateLimitCache.set(websocket, cacheEntry);

    websocket.on('close', () => {
      if (cacheEntry.resetTimer) {
        clearInterval(cacheEntry.resetTimer);
      }
      messageRateLimitFcn.delete(websocket);
    });
  }

  if (!cacheEntry.resetTimer) {
    cacheEntry.resetTimer = setInterval(() => {
      cacheEntry.messageCount = 0;
    }, periodMs);
    
    websocket.once('close', () => clearInterval(cacheEntry.resetTimer));
  }

  return (executeAction) => {
    if (cacheEntry.messageCount < messagesAllowed) {
      cacheEntry.messageCount++;
      executeAction();
    } else {
      console.log('Rate limit exceeded. Message not sent.');
      websocket.send(JSON.stringify({ error: 'Rate limit exceeded. Please wait before retrying.' }));
    }
  };
};

websocketServer.on('connection', (websocket) => {
  console.log('Client connected');
  const applyRateLimit = enforceRateLimit(websocket, 5, 10000);

  websocket.on('message', (messageData) => {
    applyRateLimit(() => {
      console.log('Message received from client:', messageData);
      websocket.send(`Echo from server: ${messageData}`);
    });
  });

  websocket.on('close', => {
    console.log('Client disconnected');
  });
});

const PORT = process.env.PORT || 3000;
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});