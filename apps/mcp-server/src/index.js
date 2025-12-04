import express from 'express';
import cors from 'cors';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import chokidar from 'chokidar';

import { RAGService } from './services/rag.js';
import { ContentHandler } from './handlers/content.js';
import { ChatHandler } from './handlers/chat.js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

class MCPServer {
  constructor() {
    this.app = express();
    this.server = null;
    this.mcpServer = null;
    this.ragService = new RAGService();
    this.contentHandler = new ContentHandler();
    this.chatHandler = new ChatHandler(this.ragService);
    this.docsPath = process.env.DOCS_PATH || join(__dirname, '../../book-docusaurus/docs');

    this.setupExpress();
    this.setupMCPServer();
    this.setupFileWatcher();
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

    // Content ingestion endpoint
    this.app.post('/ingest', async (req, res) => {
      try {
        const result = await this.contentHandler.ingestContent(this.docsPath);
        res.json(result);
      } catch (error) {
        console.error('Ingestion error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Chat endpoint
    this.app.post('/chat', async (req, res) => {
      try {
        const { message, context } = req.body;
        const response = await this.chatHandler.handleMessage(message, context);
        res.json(response);
      } catch (error) {
        console.error('Chat error:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  setupMCPServer() {
    this.mcpServer = new Server(
      {
        name: 'ai-textbook-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // Register tools
    this.mcpServer.setRequestHandler('tools/list', async () => ({
      tools: [
        {
          name: 'search_content',
          description: 'Search textbook content using RAG',
          inputSchema: {
            type: 'object',
            properties: {
              query: { type: 'string' },
              context: { type: 'string' }
            },
            required: ['query']
          }
        },
        {
          name: 'explain_code',
          description: 'Explain code snippets from the textbook',
          inputSchema: {
            type: 'object',
            properties: {
              code: { type: 'string' },
              language: { type: 'string' }
            },
            required: ['code']
          }
        }
      ]
    }));

    this.mcpServer.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'search_content':
          const results = await this.ragService.search(args.query, args.context);
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify(results, null, 2)
              }
            ]
          };

        case 'explain_code':
          const explanation = await this.chatHandler.explainCode(args.code, args.language);
          return {
            content: [
              {
                type: 'text',
                text: explanation
              }
            ]
          };

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  setupFileWatcher() {
    // Watch for changes in documentation
    const watcher = chokidar.watch(`${this.docsPath}/**/*.md`, {
      ignored: /node_modules/,
      persistent: true
    });

    watcher.on('change', async (path) => {
      console.log(`File changed: ${path}`);
      try {
        await this.contentHandler.processFile(path);
        console.log(`Successfully processed: ${path}`);
      } catch (error) {
        console.error(`Error processing ${path}:`, error);
      }
    });

    watcher.on('add', async (path) => {
      console.log(`File added: ${path}`);
      try {
        await this.contentHandler.processFile(path);
        console.log(`Successfully processed: ${path}`);
      } catch (error) {
        console.error(`Error processing ${path}:`, error);
      }
    });
  }

  async start() {
    const port = process.env.PORT || 3001;

    // Start Express server
    this.app.listen(port, () => {
      console.log(`🚀 MCP Server running on http://localhost:${port}`);
    });

    // Start MCP server with stdio transport
    const transport = new StdioServerTransport();
    await this.mcpServer.connect(transport);

    console.log('📡 MCP Server connected via stdio');
  }
}

// Start the server
const server = new MCPServer();
server.start().catch(console.error);