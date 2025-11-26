require('dotenv').config(); // Load environment variables from .env file

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const axios = require('axios'); // Import axios
const ffmpeg = require('fluent-ffmpeg'); // Import fluent-ffmpeg
const sharp = require('sharp'); // Import sharp

// Set FFmpeg path (adjust if FFmpeg is not in your system's PATH)
ffmpeg.setFfmpegPath(process.env.FFMPEG_PATH || 'ffmpeg');
ffmpeg.setFfprobePath(process.env.FFPROBE_PATH || 'ffprobe');

const app = express();
const PORT = process.env.PORT || 5000;
const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
const UNSPLASH_ACCESS_KEY = process.env.UNSPLASH_ACCESS_KEY;
const PEXELS_API_KEY = process.env.PEXELS_API_KEY;

app.use(cors());
app.use(express.json());

// Create storage directories if they don't exist
const storageDir = path.join(__dirname, 'storage');
const audioDir = path.join(storageDir, 'audio');
const videosDir = path.join(storageDir, 'videos');
const assetsDir = path.join(__dirname, 'assets'); // For local placeholder clips

if (!fs.existsSync(storageDir)) fs.mkdirSync(storageDir);
if (!fs.existsSync(audioDir)) fs.mkdirSync(audioDir);
if (!fs.existsSync(videosDir)) fs.mkdirSync(videosDir);
if (!fs.existsSync(assetsDir)) fs.mkdirSync(assetsDir);

// Static routes to serve files from /storage and /assets
app.use('/storage', express.static(storageDir));
app.use('/assets', express.static(assetsDir));

// Serve static files from the React app build directory
// This should be placed after your API routes so API calls are not intercepted
const frontendBuildPath = path.join(__dirname, 'public_html');
app.use(express.static(frontendBuildPath));

// Enable CORS for all routes (including OPTIONS)
app.use(cors({
  origin: '*', // Allow all origins for development
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));
app.use(express.json());

// In-memory job queue for video generation (for simplicity)
const jobQueue = {}; // { jobId: { status: 'pending'|'in_progress'|'completed'|'failed', result: any, progress: number } }

// Helper function to simulate TTS
async function generateVoiceStub(script, voice, speed) {
  return new Promise(resolve => {
    setTimeout(() => {
      const id = uuidv4();
      const audioFileName = `${id}.mp3`;
      const audioFilePath = path.join(audioDir, audioFileName);
      fs.writeFileSync(audioFilePath, `Placeholder audio for: ${script} (${voice}, ${speed})`);
      console.log(`Generated voice stub: ${audioFilePath}`);
      resolve({ id, audioUrl: `/storage/audio/${audioFileName}` });
    }, 1500); // Simulate network delay
  });
}

// Helper function to generate voice using ElevenLabs API
async function generateVoiceElevenLabs(script, voice, speed) {
  if (!ELEVENLABS_API_KEY) {
    throw new Error('ElevenLabs API key is not configured.');
  }

  try {
    // This is a simplified example. You'd need to select a specific voice_id
    // and potentially adjust other parameters for ElevenLabs.
    // Refer to ElevenLabs API documentation for details:
    // https://elevenlabs.io/docs/api-reference/text-to-speech
    const voiceId = voice === 'male' ? 'pNInz6obpgDQGcFmaJgB' : 'EXAVITQu4vr4xnSDxMaL'; // Example voice IDs
    const response = await axios.post(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      {
        text: script,
        model_id: 'eleven_monolingual_v1', // Or another suitable model
        voice_settings: {
          stability: 0.5,
          similarity_boost: 0.75,
          style: 0.0,
          use_speaker_boost: true,
        },
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'xi-api-key': ELEVENLABS_API_KEY,
          'Accept': 'audio/mpeg',
        },
        responseType: 'arraybuffer',
      }
    );

    const id = uuidv4();
    const audioFileName = `${id}.mp3`;
    const audioFilePath = path.join(audioDir, audioFileName);
    fs.writeFileSync(audioFilePath, response.data);
    console.log(`Generated voice with ElevenLabs: ${audioFilePath}`);
    return { id, audioUrl: `/storage/audio/${audioFileName}` };
  } catch (error) {
    console.error('Error generating voice with ElevenLabs:', error.response ? error.response.data : error.message);
    throw new Error('ElevenLabs TTS failed.');
  }
}

// POST /api/generate-voice
app.post('/api/generate-voice', async (req, res) => {
  const { script, voice, speed } = req.body;

  if (!script) {
    return res.status(400).json({ error: 'Script is required.' });
  }

  try {
    let result;
    if (ELEVENLABS_API_KEY) {
      result = await generateVoiceElevenLabs(script, voice || 'male', speed || 1.0);
    } else {
      console.warn('ElevenLabs API key not found. Using stub for voice generation.');
      result = await generateVoiceStub(script, voice || 'male', speed || 1.0);
    }
    res.json(result);
  } catch (error) {
    console.error('Error generating voice:', error);
    res.status(500).json({ error: 'Failed to generate voice: ' + error.message });
  }
});

// Helper function to select image clips
async function selectImageClips(script, numberOfClips = 5) {
  let imageUrls = [];
  const query = script.split(' ').slice(0, 5).join(' '); // Use first few words of script as query

  // Try Unsplash
  if (UNSPLASH_ACCESS_KEY) {
    try {
      console.log(`Searching Unsplash for: ${query}`);
      const response = await axios.get(`https://api.unsplash.com/search/photos`, {
        params: { query, per_page: numberOfClips },
        headers: { Authorization: `Client-ID ${UNSPLASH_ACCESS_KEY}` },
      });
      imageUrls = response.data.results.map(img => img.urls.regular);
      console.log(`Found ${imageUrls.length} images from Unsplash.`);
    } catch (error) {
      console.error('Error fetching from Unsplash:', error.response ? error.response.data : error.message);
      imageUrls = []; // Fallback to Pexels or local
    }
  }

  // If Unsplash failed or no key, try Pexels
  if (imageUrls.length === 0 && PEXELS_API_KEY) {
    try {
      console.log(`Searching Pexels for: ${query}`);
      const response = await axios.get(`https://api.pexels.com/v1/search`, {
        params: { query, per_page: numberOfClips },
        headers: { Authorization: PEXELS_API_KEY },
      });
      imageUrls = response.data.photos.map(photo => photo.src.large);
      console.log(`Found ${imageUrls.length} images from Pexels.`);
    } catch (error) {
      console.error('Error fetching from Pexels:', error.response ? error.response.data : error.message);
      imageUrls = []; // Fallback to local
    }
  }

  // Fallback to local assets
  if (imageUrls.length === 0) {
    console.warn('No API keys for Unsplash/Pexels or API fetch failed. Using local placeholder images.');
    const localImages = fs.readdirSync(assetsDir).filter(f => f.match(/\.(jpg|jpeg|png)$/i));
    for (let i = 0; i < numberOfClips; i++) {
      if (localImages[i % localImages.length]) {
        imageUrls.push(path.join(assetsDir, localImages[i % localImages.length]));
      }
    }
    if (imageUrls.length === 0) {
      console.error('No local placeholder images found in assets directory.');
      throw new Error('No images available for video generation.');
    }
  }
  return imageUrls;
}

// Function to get audio duration using ffprobe
function getAudioDuration(audioFilePath) {
  return new Promise((resolve, reject) => {
    ffmpeg.ffprobe(audioFilePath, (err, metadata) => {
      if (err) {
        console.error('Error getting audio duration:', err);
        return reject(err);
      }
      resolve(metadata.format.duration);
    });
  });
}

// Helper to split script into caption segments (simple split by sentence)
function getCaptionSegments(script) {
    return script.match(/[^.!?]+[.!?]*/g) || [script];
}


// POST /api/generate-video
app.post('/api/generate-video', async (req, res) => {
  const { id: voiceId, script, coverImageUrl } = req.body;

  if (!voiceId || !script) {
    return res.status(400).json({ error: 'Voice ID and script are required.' });
  }

  const jobId = uuidv4();
  jobQueue[jobId] = { status: 'pending', progress: 0 };
  res.json({ jobId, statusUrl: `/api/status/${jobId}` });

  (async () => {
    try {
      jobQueue[jobId].status = 'in_progress';
      jobQueue[jobId].progress = 5;
      console.log(`Video generation job ${jobId} started.`);

      const audioFilePath = path.join(audioDir, `${voiceId}.mp3`);
      if (!fs.existsSync(audioFilePath)) {
        throw new Error(`Audio file not found for voice ID: ${voiceId}`);
      }
      const audioDuration = await getAudioDuration(audioFilePath);
      console.log(`Audio duration: ${audioDuration} seconds`);

      // 1. Select images/video clips
      jobQueue[jobId].progress = 15;
      const imageUrls = await selectImageClips(script);
      const clipDuration = audioDuration / imageUrls.length; // Distribute audio duration among clips
      console.log(`Selected ${imageUrls.length} image clips. Each clip duration: ${clipDuration}s`);

      // 2. Prepare images (download, resize, add text overlays)
      jobQueue[jobId].progress = 30;
      const processedImagePaths = [];
      const captionSegments = getCaptionSegments(script);
      const segmentsPerImage = Math.ceil(captionSegments.length / imageUrls.length);

      for (let i = 0; i < imageUrls.length; i++) {
        const imgUrl = imageUrls[i];
        const outputImagePath = path.join(storageDir, `processed_img_${jobId}_${i}.png`);
        const imageBuffer = imgUrl.startsWith('http') ? (await axios.get(imgUrl, { responseType: 'arraybuffer' })).data : fs.readFileSync(imgUrl);
        
        let image = sharp(imageBuffer);
        const metadata = await image.metadata();

        const width = 1920;
        const height = 1080;

        // Resize image to fit 1080p, maintaining aspect ratio
        image = image.resize({
            width: width,
            height: height,
            fit: sharp.fit.cover, // Cover will crop
            position: sharp.strategy.attention // Focus on interesting parts
        });

        // Add text overlay
        const segmentIndexStart = i * segmentsPerImage;
        const segmentIndexEnd = Math.min((i + 1) * segmentsPerImage, captionSegments.length);
        const caption = captionSegments.slice(segmentIndexStart, segmentIndexEnd).join(' ').trim();

        if (caption) {
            const svgText = `
                <svg width="${width}" height="${height}">
                <style>
                    .title { fill: #fff; font-size: 48px; font-family: 'Arial', sans-serif; text-align: center; }
                    .background { fill: rgba(0,0,0,0.5); }
                </style>
                <rect x="0" y="${height * 0.7}" width="${width}" height="${height * 0.2}" class="background"/>
                <text x="50%" y="${height * 0.8}" text-anchor="middle" class="title">${caption}</text>
                </svg>
            `;
            const svgBuffer = Buffer.from(svgText);
            image = image.composite([{ input: svgBuffer, gravity: 'northwest' }]);
        }

        await image.toFile(outputImagePath);
        processedImagePaths.push(outputImagePath);
        jobQueue[jobId].progress = 30 + Math.floor((i / imageUrls.length) * 30);
      }
      console.log(`Processed ${processedImagePaths.length} images with captions.`);

      // 3. FFmpeg: Combine images, audio, and add transitions
      jobQueue[jobId].progress = 70;
      const videoFileName = `${jobId}.mp4`;
      const videoFilePath = path.join(videosDir, videoFileName);
      const nasheedAudioPath = path.join(assetsDir, 'nasheed.mp3');

      let command = ffmpeg();

      // Add all processed images as inputs with their respective durations
      processedImagePaths.forEach((imgPath) => {
        command = command.input(imgPath).loop(clipDuration); // Loop each image for its calculated duration
      });

      // Prepare complex filter for video streams (crossfades)
      const videoFilters = [];
      if (processedImagePaths.length > 1) {
        let currentVideoInput = 0;
        for (let i = 0; i < processedImagePaths.length - 1; i++) {
          const prevInput = `[${currentVideoInput}:v]`;
          const nextInput = `[${currentVideoInput + 1}:v]`;
          const output = `[v${i}]`;
          videoFilters.push({
            filter: 'xfade',
            options: {
              transition: 'fade',
              duration: 0.8,
              offset: (i + 1) * clipDuration - 0.4,
            },
            inputs: `${prevInput}${nextInput}`,
            outputs: output,
          });
          currentVideoInput++;
        }
      }

      // Add main audio input
      command = command.input(audioFilePath);
      const mainAudioStreamIndex = processedImagePaths.length; // Index of main audio stream

      // Add background nasheed if exists
      let nasheedAudioStreamIndex = -1;
      if (fs.existsSync(nasheedAudioPath)) {
        command = command.input(nasheedAudioPath);
        nasheedAudioStreamIndex = processedImagePaths.length + 1; // Index of nasheed audio stream
      }

      // Prepare complex filter for audio streams (mixing main audio and nasheed)
      const audioFilters = [];
      let finalAudioOutput = `[aout]`;
      if (nasheedAudioStreamIndex !== -1) {
        audioFilters.push({
          filter: 'amix',
          options: {
            inputs: 2,
            duration: 'shortest',
          },
          inputs: `[${mainAudioStreamIndex}:a][${nasheedAudioStreamIndex}:a]`,
          outputs: finalAudioOutput,
        });
      } else {
        // If no nasheed, just pass through main audio
        finalAudioOutput = `[${mainAudioStreamIndex}:a]`;
      }

      command
        .videoCodec('libx264')
        .audioCodec('aac')
        .format('mp4')
        .outputOptions([
          '-pix_fmt yuv420p',
          '-map 0:a', // Map audio from the first audio input by default (main audio)
          '-shortest', // Finish encoding when the shortest input stream ends (i.e., main audio)
        ])
        .complexFilter([...videoFilters, ...audioFilters])
        .output(videoFilePath)
        .on('progress', (progress) => {
          jobQueue[jobId].progress = 70 + Math.floor(progress.percent / 3);
          console.log(`FFmpeg progress: ${progress.percent}%`);
        })
        .on('end', () => {
          jobQueue[jobId].status = 'completed';
          jobQueue[jobId].progress = 100;
          jobQueue[jobId].result = { id: jobId, videoUrl: `/storage/videos/${videoFileName}` };
          console.log(`Video generation job ${jobId} completed. Video saved to ${videoFilePath}`);
          // Clean up processed images
          processedImagePaths.forEach(imgPath => fs.unlinkSync(imgPath));
        })
        .on('error', (err, stdout, stderr) => {
          console.error(`FFmpeg error for job ${jobId}:`, err.message);
          console.error('FFmpeg stdout:\n', stdout);
          console.error('FFmpeg stderr:\n', stderr);
          jobQueue[jobId].status = 'failed';
          jobQueue[jobId].result = { error: 'Failed to generate video: ' + err.message, ffmpeg_stdout: stdout, ffmpeg_stderr: stderr };
          // Clean up processed images
          processedImagePaths.forEach(imgPath => fs.unlinkSync(imgPath));
        })
        .run();
    } catch (error) {
      console.error(`Error processing video generation job ${jobId}:`, error);
      jobQueue[jobId].status = 'failed';
      jobQueue[jobId].result = { error: 'Failed to generate video: ' + error.message };
    }
  })();
});

// GET /api/status/:id

// GET /api/status/:id
app.get('/api/status/:id', (req, res) => {
  const { id } = req.params;
  const job = jobQueue[id];

  if (!job) {
    return res.status(404).json({ error: 'Job not found.' });
  }

  res.json(job);
});

app.get('/test', (req, res) => {
  res.send('Backend is running! Hello World!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
