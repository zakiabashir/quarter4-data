import OpenAI from 'openai';

const openai = process.env.OPENAI_API_KEY ? new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
}) : null;

export async function getEmbedding(text) {
  if (!openai) {
    console.warn("OpenAI not configured, returning dummy embedding");
    return new Array(1536).fill(0);
  }
  try {
    const response = await openai.embeddings.create({
      model: 'text-embedding-ada-002',
      input: text.replace(/\n/g, ' ').trim()
    });
    return response.data[0].embedding;
  } catch (error) {
    console.error('Error getting embedding:', error);
    throw error;
  }
}

export function chunkText(text, maxSize = 1000, overlap = 100) {
  const chunks = [];
  let start = 0;

  while (start < text.length) {
    let end = start + maxSize;

    // Try to break at word boundary
    if (end < text.length) {
      const lastSpace = text.lastIndexOf(' ', end);
      if (lastSpace > start) {
        end = lastSpace;
      }
    }

    chunks.push(text.slice(start, end).trim());
    start = end - overlap;
  }

  return chunks.filter(chunk => chunk.length > 0);
}