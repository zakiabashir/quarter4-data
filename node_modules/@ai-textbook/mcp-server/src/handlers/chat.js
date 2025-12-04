export class ChatHandler {
  constructor(ragService) {
    this.ragService = ragService;
    this.sessionContexts = new Map();
  }

  async handleMessage(message, context = {}) {
    const sessionId = context.sessionId || 'default';

    // Maintain conversation context
    if (!this.sessionContexts.has(sessionId)) {
      this.sessionContexts.set(sessionId, {
        messages: [],
        currentChapter: context.chapter || null,
        currentSection: context.section || null
      });
    }

    const sessionCtx = this.sessionContexts.get(sessionId);

    // Add user message to context
    sessionCtx.messages.push({ role: 'user', content: message });

    // Generate response using RAG
    const response = await this.ragService.generateResponse(
      message,
      context.chapter || sessionCtx.currentChapter
    );

    // Add assistant response to context
    sessionCtx.messages.push({ role: 'assistant', content: response.response });

    // Limit context size (keep last 10 messages)
    if (sessionCtx.messages.length > 10) {
      sessionCtx.messages = sessionCtx.messages.slice(-10);
    }

    return {
      id: Date.now().toString(),
      response: response.response,
      sources: response.sources,
      sessionId
    };
  }

  async explainCode(code, language = 'python') {
    const prompt = `
    Explain this ${language} code step by step:

    \`\`\`${language}
    ${code}
    \`\`\`

    Provide:
    1. What the code does
    2. How each part works
    3. Common use cases
    4. Possible modifications or improvements
    `;

    const response = await this.ragService.generateResponse(prompt);
    return response.response;
  }

  async getSessionContext(sessionId) {
    return this.sessionContexts.get(sessionId) || {
      messages: [],
      currentChapter: null,
      currentSection: null
    };
  }

  async clearSession(sessionId) {
    this.sessionContexts.delete(sessionId);
    return { success: true };
  }
}