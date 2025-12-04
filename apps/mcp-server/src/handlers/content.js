import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import MarkdownIt from 'markdown-it';
import { chunkText } from '../utils/embeddings.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export class ContentHandler {
  constructor() {
    this.md = new MarkdownIt();
  }

  async ingestContent(docsPath) {
    console.log(`📚 Ingesting content from: ${docsPath}`);

    const results = {
      filesProcessed: 0,
      documentsCreated: 0,
      errors: []
    };

    try {
      const files = await this.getAllMarkdownFiles(docsPath);

      for (const file of files) {
        try {
          await this.processFile(file);
          results.filesProcessed++;
        } catch (error) {
          console.error(`Error processing ${file}:`, error);
          results.errors.push({ file, error: error.message });
        }
      }

      console.log(`✅ Ingestion complete: ${results.filesProcessed} files processed`);
      return results;
    } catch (error) {
      console.error('Ingestion failed:', error);
      throw error;
    }
  }

  async getAllMarkdownFiles(dir) {
    const files = [];

    async function scanDir(currentDir) {
      const items = await fs.readdir(currentDir);

      for (const item of items) {
        const fullPath = path.join(currentDir, item);
        const stat = await fs.stat(fullPath);

        if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
          await scanDir(fullPath);
        } else if (item.endsWith('.md')) {
          files.push(fullPath);
        }
      }
    }

    await scanDir(dir);
    return files;
  }

  async processFile(filePath) {
    const content = await fs.readFile(filePath, 'utf-8');

    // Extract metadata from file path
    const relativePath = path.relative(process.env.DOCS_PATH || '', filePath);
    const pathParts = relativePath.split(path.sep);

    let chapter = '';
    let section = '';

    // Extract chapter and section from path
    if (pathParts.length >= 2 && pathParts[0].startsWith('chapter')) {
      chapter = pathParts[0];
      section = pathParts[1].replace('.md', '');
    }

    // Parse markdown to separate content
    const tokens = this.md.parse(content, {});
    let markdownContent = '';

    // Re-render without the frontmatter
    for (const token of tokens) {
      if (token.type === 'heading_open' || token.type === 'heading_close' ||
          token.type === 'paragraph_open' || token.type === 'paragraph_close' ||
          token.type === 'list_item_open' || token.type === 'list_item_close' ||
          token.type === 'bullet_list_open' || token.type === 'bullet_list_close' ||
          token.type === 'ordered_list_open' || token.type === 'ordered_list_close' ||
          token.type === 'code_block' || token.type === 'fence' ||
          token.type === 'inline') {
        markdownContent += this.md.renderer.render([token]);
      }
    }

    // Clean up the markdown
    markdownContent = markdownContent
      .replace(/<[^>]*>/g, '') // Remove HTML tags
      .replace(/```[\s\S]*?```/g, '') // Remove code blocks
      .replace(/`[^`]*`/g, '') // Remove inline code
      .replace(/\n{3,}/g, '\n\n') // Normalize whitespace
      .trim();

    // Split into chunks for embedding
    const chunks = chunkText(markdownContent, 800, 100);

    console.log(`  📄 Processing ${relativePath}: ${chunks.length} chunks`);

    // Return documents for RAG service to process
    return {
      filePath,
      chapter,
      section,
      chunks: chunks.map((chunk, index) => ({
        id: `${relativePath}-${index}`,
        content: chunk,
        metadata: {
          filePath: relativePath,
          chapter,
          section,
          chunkIndex: index,
          totalChunks: chunks.length
        }
      }))
    };
  }

  async extractMetadata(content) {
    const metadata = {};

    // Try to extract YAML frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const yaml = frontmatterMatch[1];

      // Extract key metadata fields
      const titleMatch = yaml.match(/title:\s*(.+)/);
      if (titleMatch) metadata.title = titleMatch[1];

      const descriptionMatch = yaml.match(/description:\s*(.+)/);
      if (descriptionMatch) metadata.description = descriptionMatch[1];

      const tagsMatch = yaml.match(/tags:\s*\[(.+)\]/);
      if (tagsMatch) metadata.tags = tagsMatch[1].split(',').map(t => t.trim());
    }

    return metadata;
  }
}