import { QdrantClient } from '@qdrant/js-client-rest';
import OpenAI from 'openai';
import { getEmbedding } from '../utils/embeddings.js';

export class RAGService {
  constructor() {
    this.qdrant = new QdrantClient({
      url: process.env.QDRANT_URL || 'http://localhost:6333',
      apiKey: process.env.QDRANT_API_KEY
    });

    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    });

    this.collectionName = 'textbook_content';
    this.initCollection();
  }

  async initCollection() {
    try {
      const collections = await this.qdrant.getCollections();
      const exists = collections.collections.find(c => c.name === this.collectionName);

      if (!exists) {
        await this.qdrant.createCollection(this.collectionName, {
          vectors: {
            size: 1536,
            distance: 'Cosine'
          }
        });
        console.log(`✅ Created collection: ${this.collectionName}`);
      }
    } catch (error) {
      console.error('Error initializing collection:', error);
    }
  }

  async addDocument(doc) {
    const embedding = await getEmbedding(doc.content);

    await this.qdrant.upsert(this.collectionName, {
      points: [{
        id: doc.id,
        vector: embedding,
        payload: {
          content: doc.content,
          metadata: doc.metadata || {},
          chapter: doc.chapter,
          section: doc.section
        }
      }]
    });
  }

  async search(query, context = '', limit = 5) {
    const queryEmbedding = await getEmbedding(query);

    const searchResult = await this.qdrant.search(this.collectionName, {
      vector: queryEmbedding,
      limit: limit,
      with_payload: true,
      score_threshold: 0.7
    });

    // Filter results based on context if provided
    let filteredResults = searchResult;
    if (context) {
      filteredResults = searchResult.filter(result =>
        result.payload.chapter === context ||
        result.payload.section === context
      );
    }

    return {
      query,
      context,
      results: filteredResults.map(r => ({
        content: r.payload.content,
        metadata: r.payload.metadata,
        chapter: r.payload.chapter,
        section: r.payload.section,
        score: r.score
      }))
    };
  }

  async generateResponse(query, context = '') {
    // Search for relevant content
    const searchResults = await this.search(query, context);

    // Build context from search results
    const relevantContent = searchResults.results
      .map(r => r.content)
      .join('\n\n');

    // Create system message
    const systemMessage = `You are an AI tutor for Physical AI and Humanoid Robotics.
    Use the provided textbook content to answer questions accurately and helpfully.
    Always cite which chapter/section the information comes from.
    If the information isn't in the provided content, say so clearly.
    Keep answers educational and at an appropriate level for university students.`;

    // Create user message with context
    const userMessage = `
Context from textbook:
${relevantContent}

Question: ${query}

Please provide a helpful answer based on the textbook content above.`;

    try {
      const completion = await this.openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: systemMessage },
          { role: 'user', content: userMessage }
        ],
        temperature: 0.7,
        max_tokens: 500
      });

      return {
        response: completion.choices[0].message.content,
        sources: searchResults.results.map(r => ({
          chapter: r.chapter,
          section: r.section,
          score: r.score
        }))
      };
    } catch (error) {
      console.error('Error generating response:', error);
      throw new Error('Failed to generate AI response');
    }
  }

  async deleteDocument(docId) {
    await this.qdrant.delete(this.collectionName, {
      points: [docId]
    });
  }

  async clearCollection() {
    try {
      await this.qdrant.deleteCollection(this.collectionName);
      await this.initCollection();
    } catch (error) {
      console.error('Error clearing collection:', error);
    }
  }
}