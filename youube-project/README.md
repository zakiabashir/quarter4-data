# AI Script to Video Generator

This is a full-stack web application that allows users to generate voice-overs and videos from a script using AI.

## Features

- **Frontend (React)**:
  - Single page app with a textarea for script input.
  - Voice settings (male/female, speed).
  - Buttons: "Generate Voice", "Generate Video", "Preview", "Download".
  - Progress indicators for voice and video generation.
  - Video preview player and audio playback.
  - Optional cover image upload.
  - Styled with Tailwind CSS.
  - Input validation and error messages.
- **Backend (Node.js + Express)**:
  - `POST /api/generate-voice`: Generates audio from script using ElevenLabs API (or a stub if API key is missing).
  - `POST /api/generate-video`: Generates a 1080p MP4 video from audio and script.
    - Automatically selects relevant stock images/video clips using Unsplash/Pexels APIs (or local placeholders if keys are missing).
    - Uses FFmpeg to combine images/clips + audio with soft crossfades and simple text overlays.
    - Mixes main TTS voice with a low-volume background nasheed.
  - Static routes to serve generated audio/video files and local assets.
  - In-memory job queue to process video generation tasks and provide status updates via `GET /api/status/:id`.

## Quick Start (Urdu)

فوری آغاز: یہ سیکشن غیر تکنیکی صارفین کے لیے آواز اور ویڈیو بنانے کا فوری طریقہ بتاتا ہے۔

1. **آواز بنائیں (Generate Voice)**: اپنا اسکرپٹ لکھیں اور "Generate Voice" بٹن دبائیں۔ جب آواز تیار ہو جائے گی تو آپ اسے سن سکیں گے۔
2. **ویڈیو بنائیں (Generate Video)**: آواز بننے کے بعد، "Generate Video" بٹن دبائیں۔ جب ویڈیو تیار ہو جائے گی تو آپ اسے دیکھ اور ڈاؤن لوڈ کر سکیں گے۔

## Setup

### Prerequisites

- Node.js (v18 or higher) and npm
- Docker (optional, for containerized deployment)
- FFmpeg (must be installed and available in your system's PATH if running backend directly, or handled by Docker)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-script-to-video.git
cd ai-script-to-video
```

### 2. Environment Variables

Create a `.env` file in the root directory of the project (e.g., `ai-script-to-video/.env`) and add the following:

```
PORT=5000
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
PEXELS_API_KEY=your_pexels_api_key_here

# Optional: If FFmpeg is not in your system's PATH, specify the full path
# FFMPEG_PATH=/usr/local/bin/ffmpeg
# FFPROBE_PATH=/usr/local/bin/ffprobe
```

- `PORT`: The port on which the backend server will run. (Default: `5000`)
- `ELEVENLABS_API_KEY`: Required for actual voice generation. If not provided, a stub will be used. Get it from [ElevenLabs](https://elevenlabs.io/).
- `UNSPLASH_ACCESS_KEY`: Optional, for fetching stock images. If not provided, Pexels or local assets will be used. Get it from [Unsplash Developers](https://unsplash.com/developers).
- `PEXELS_API_KEY`: Optional, for fetching stock images. If not provided, local assets will be used. Get it from [Pexels API](https://www.pexels.com/api/).
- `FFMPEG_PATH`, `FFPROBE_PATH`: Only needed if FFmpeg executables are not in your system's PATH.

### 3. Install Dependencies

#### Backend

```bash
cd backend
npm install
cd ..
```

#### Frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Running the Application

#### Development Mode (Frontend & Backend Separately)

You will need two terminal windows for this.

**Terminal 1: Run Backend**

```bash
cd backend
npm start # or `node server.js`
```

**Terminal 2: Run Frontend**

```bash
cd frontend
npm start
```

The frontend will typically run on `http://localhost:3000` and proxy API requests to the backend on `http://localhost:5000`.

#### Production Build (using `concurrently`)

First, install `concurrently` in the root of your project:

```bash
npm install concurrently
```

Then, add a `dev` script in the root `package.json` to run both frontend and backend concurrently.

```json
// In your root package.json (create if it doesn't exist)
{
  "name": "ai-script-to-video",
  "version": "1.0.0",
  "description": "A full-stack web application to generate voice-overs and videos from a script using AI.",
  "main": "index.js",
  "scripts": {
    "start": "node backend/server.js",
    "dev": "concurrently \"npm start --prefix backend\" \"npm start --prefix frontend\""
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "concurrently": "^8.0.0"
  }
}
```

Now you can run both with:

```bash
npm run dev
```

#### Running with Docker

1. **Build the Docker Image**: Navigate to the project root directory and build the Docker image.

   ```bash
   docker build -t ai-script-to-video .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 5000:5000 --env-file ./.env ai-script-to-video
   ```
   
   The application will be accessible at `http://localhost:5000`.

### Placeholder Assets

- Placeholder images (`image1.jpg`, `image2.jpg`, `image3.jpg`) are located in `backend/assets/`.
- A placeholder background nasheed (`nasheed.mp3`) is located in `backend/assets/`.
- If API keys for Unsplash/Pexels are not provided, these local assets will be used.

### Replacing ElevenLabs TTS

To replace ElevenLabs TTS with another provider (e.g., OpenAI TTS or Gemini TTS), you would primarily modify the `backend/server.js` file:

1.  **Identify the new API**: Find the API documentation for your desired TTS provider.
2.  **Install necessary SDK/library**: If the new provider has an official Node.js SDK, install it (`npm install <sdk-name>`).
3.  **Update Environment Variables**: Add any new API keys or configuration settings to your `.env` file.
4.  **Modify `generateVoiceElevenLabs` function**:
    -   Rename `generateVoiceElevenLabs` to something more generic like `generateVoiceExternal` or create a new function.
    -   Adjust the `axios.post` call (or use the new SDK) to match the new API's endpoint, headers, and request body format.
    -   Ensure the audio output is saved as an MP3 file in the `storage/audio` directory.
    -   Update the error handling to reflect the new API's potential error responses.
5.  **Update the `app.post('/api/generate-voice')` handler**:
    -   Modify the conditional logic to use your new function based on the presence of its API key, or use it as the primary external provider.

---

## Project Structure

```
.
├── Dockerfile                  # Multi-stage Dockerfile for the entire application
├── backend/
│   ├── Dockerfile              # Dockerfile for backend only
│   ├── package.json            # Backend dependencies and scripts
│   ├── server.js               # Backend Express application
│   ├── assets/                 # Placeholder images, nasheed.mp3
│   └── storage/                # Generated audio and video files (runtime created)
├── frontend/
│   ├── package.json            # Frontend dependencies and scripts
│   ├── public/                 # Public assets for React app
│   ├── src/                    # React source code
│   │   ├── App.js              # Main React component
│   │   ├── index.css           # Tailwind CSS directives
│   │   ├── index.js            # React app entry point
│   │   └── reportWebVitals.js
│   ├── tailwind.config.js      # Tailwind CSS configuration
│   └── postcss.config.js       # PostCSS configuration
├── .env.example                # Example environment variables
└── README.md                   # Project documentation
```
