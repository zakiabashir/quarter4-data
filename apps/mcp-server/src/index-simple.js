import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

class SimpleServer {
  constructor() {
    this.app = express();
    this.setupExpress();
  }

  setupExpress() {
    this.app.use(cors());
    this.app.use(express.json());

    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        service: 'mcp-server',
        timestamp: new Date().toISOString()
      });
    });

    // Search endpoint (dummy implementation)
    this.app.post('/search', async (req, res) => {
      try {
        const { query } = req.body;
        console.log('Search query:', query);

        // Return dummy results for now
        res.json({
          results: [{
            content: `Dummy result for: ${query}`,
            metadata: { source: 'test' },
            score: 0.9
          }],
          total_found: 1,
          search_time_ms: 10
        });
      } catch (error) {
        console.error('Search error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Chat endpoint (dummy implementation)
    this.app.post('/chat', async (req, res) => {
      try {
        const { message } = req.body;
        console.log('Chat message:', message);

        // Return dummy response for now
        res.json({
          response: `This is a dummy response to: ${message}`,
          sources: []
        });
      } catch (error) {
        console.error('Chat error:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  async start() {
    const port = process.env.PORT || 3001;

    // Start Express server
    this.app.listen(port, () => {
      console.log(`🚀 MCP Server running on http://localhost:${port}`);
      console.log('RAG features disabled - running in simple mode');
    });
  }
}

// Start the server
const server = new SimpleServer();
server.start().catch(console.error);