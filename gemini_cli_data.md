# 🟢 Node.js aur Gemini CLI Installation aur Setup

## Node.js Version
- **Required Version:** Node.js 20 or higher
- Gemini CLI Node.js ke environment me chalta hai.

## Installation Commands

### Install Gemini CLI Globally
```bash
npm install -g @google/gemini-cli
```
- Ye command Gemini CLI ko globally install karti hai
- `-g` ka matlab global installation hota hai

### Check Installation
```bash
gemini -v
```
- Ye check karta hai ke Gemini CLI install hui hai ya nahi
- Version info display karti hai

---

## 🧠 Gemini CLI Basic Commands

| Command | Purpose |
|---------|---------|
| `gemini` | Interactive mode start karta hai |
| `gemini --model gemini-2.5-flash` | Specific model select karta hai |
| `gemini -p "..."` | Non-interactive prompt run karta hai |
| `gemini --model gemini-2.5-flash --yolo` | Auto-approve mode (no confirmations) |

---

## ⚙️ Shell Mode aur Terminal Commands

| Command | Purpose |
|---------|---------|
| `! shell` | Shell mode activate karta hai (normal terminal commands) |
| `Esc` | Shell/edit mode se normal mode me wapas aata hai |

---

## 📁 File aur Folder Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `mkdir <name>` | Naya folder create karta hai | `mkdir myProject` |
| `cd <path>` | Directory change karta hai | `cd myProject` or `cd ..` |
| `ls` | Files/folders list karta hai (Linux/Mac) | `ls` |
| `dir` | Files/folders list karta hai (CMD) | `dir` |

---

## ✨ Built-in Features aur Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/tools` | Available tools list karta hai | `/tools` |
| `/stats` | Token aur model usage dikhata hai | `/stats` |
| `/memory show` | Current context memory dikhata hai | `/memory show` |
| `/memory refresh` | CLI ki memory reset karta hai | `/memory refresh` |
| `/mcp` | MCP servers manage karta hai | `/mcp list` |
| `/clear` | Screen aur context clear karta hai | `/clear` |
| `/chat save <tag>` | Chat ko save karta hai | `/chat save resumeBuilder` |
| `/chat resume <tag>` | Saved chat load karta hai | `/chat resume resumeBuilder` |
| `@<file_or_directory>` | File/folder context deta hai | `@./src/ or @./file.ts` |
| `!<command>` | Shell command run karta hai | `!ls or !git status` |

---

## ⚡ YOLO Option

```bash
gemini --model gemini-2.5-flash --yolo
```
- Experimental option (You Only Live Once 😄)
- Auto-confirmation deta hai bina manually "yes/no" likhe
- Har step pe Gemini bina rukke kaam karega

---

## 🔗 Useful Resources

- **MCP GitHub:** https://github.com/modelcontextprotocol/servers

---

## 🪟 WSL + Ubuntu Setup (Windows)

### Step 1: Install WSL + Ubuntu
```powershell
wsl --install -d Ubuntu
```

### Step 2: Start Ubuntu
```powershell
wsl -d Ubuntu
```

### Step 3: Install Node.js aur npm
```bash
sudo apt update && sudo apt install -y nodejs npm
```

### Step 4: Install Gemini CLI
```bash
sudo npm install -g @google/gemini-cli
```

---

## ⚙️ VS Code Settings Configuration

### Fixed & Valid settings.json

```json
{
  "ide": {
    "hasSeenNudge": true
  },
  "security": {
    "auth": {
      "selectedType": "oauth-personal"
    }
  },
  "ui": {
    "theme": "Default"
  },
  "mcpServers": {
    "github": {
      "httpUrl": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "github_pat_YOUR_PERSONAL_ACCESS_TOKEN"
      },
      "timeout": 5001
    }
  }
}
```

---

## 🔥 Firebase MCP Server Setup

### Step 1: Start Firebase MCP Server
```bash
cd C:\firebase-mcp
npx firebase-tools mcp
```

### Step 2: Start Gemini in Project Folder
```bash
cd D:\firebase-project
gemini --model gemini-2.5-flash
/mcp list
```

---
