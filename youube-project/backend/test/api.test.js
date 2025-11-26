const chai = require('chai');
const chaiHttp = require('chai-http');
const { expect } = chai;
const fs = require('fs');
const path = require('path');

chai.use(chaiHttp);

// Dynamically import the app to ensure it's loaded after env vars
let app;
before((done) => {
  // Set a dummy ElevenLabs API key for testing purposes if not already set
  // This ensures the ElevenLabs path is taken for integration tests, or stub is used
  if (!process.env.ELEVENLABS_API_KEY) {
    process.env.ELEVENLABS_API_KEY = 'dummy_elevenlabs_key';
  }
  // Set a dummy FFmpeg path to prevent errors if not installed globally
  if (!process.env.FFMPEG_PATH) {
    process.env.FFMPEG_PATH = '/usr/bin/ffmpeg'; // Assuming a common path in CI/Docker
    process.env.FFPROBE_PATH = '/usr/bin/ffprobe';
  }
  // Require the app after environment variables are set
  app = require('../server');
  done();
});

describe('Backend API Tests', () => {
  const testScript = 'This is a test script for voice generation.';
  let generatedAudioId;
  let generatedVideoJobId;

  it('should generate voice successfully with a dummy key', (done) => {
    chai.request(app)
      .post('/api/generate-voice')
      .send({ script: testScript, voice: 'male', speed: 1.0 })
      .end((err, res) => {
        expect(res).to.have.status(200);
        expect(res.body).to.be.an('object');
        expect(res.body).to.have.property('id');
        expect(res.body).to.have.property('audioUrl');
        generatedAudioId = res.body.id;

        // Verify audio file exists
        const audioFilePath = path.join(__dirname, '../storage/audio', `${generatedAudioId}.mp3`);
        expect(fs.existsSync(audioFilePath)).to.be.true;
        done();
      });
  }).timeout(5000); // Increased timeout for voice generation

  it('should return 400 if script is missing for generate-voice', (done) => {
    chai.request(app)
      .post('/api/generate-voice')
      .send({ voice: 'male', speed: 1.0 })
      .end((err, res) => {
        expect(res).to.have.status(400);
        expect(res.body).to.be.an('object');
        expect(res.body).to.have.property('error').eql('Script is required.');
        done();
      });
  });

  it('should initiate video generation successfully', (done) => {
    if (!generatedAudioId) {
      // Skip if previous test failed
      return done(new Error('Audio ID not generated. Skipping video generation test.'));
    }
    chai.request(app)
      .post('/api/generate-video')
      .send({ id: generatedAudioId, script: testScript })
      .end((err, res) => {
        expect(res).to.have.status(200);
        expect(res.body).to.be.an('object');
        expect(res.body).to.have.property('jobId');
        expect(res.body).to.have.property('statusUrl');
        generatedVideoJobId = res.body.jobId;
        done();
      });
  });

  it('should return video generation status', (done) => {
    if (!generatedVideoJobId) {
      return done(new Error('Video Job ID not generated. Skipping status test.'));
    }
    // Give some time for the job to start
    setTimeout(() => {
      chai.request(app)
        .get(`/api/status/${generatedVideoJobId}`)
        .end((err, res) => {
          expect(res).to.have.status(200);
          expect(res.body).to.be.an('object');
          expect(res.body).to.have.property('status');
          expect(res.body).to.have.property('progress');
          done();
        });
    }, 1000);
  });

  it('should eventually complete video generation job', (done) => {
    if (!generatedVideoJobId) {
      return done(new Error('Video Job ID not generated. Skipping completion test.'));
    }

    const checkStatus = () => {
      chai.request(app)
        .get(`/api/status/${generatedVideoJobId}`)
        .end((err, res) => {
          expect(res).to.have.status(200);
          expect(res.body).to.be.an('object');
          const { status, result } = res.body;

          if (status === 'completed') {
            expect(result).to.have.property('videoUrl');
            // Verify video file exists (stubbed)
            const videoFilePath = path.join(__dirname, '../storage/videos', `${generatedVideoJobId}.mp4`);
            expect(fs.existsSync(videoFilePath)).to.be.true;
            done();
          } else if (status === 'failed') {
            done(new Error(`Video generation failed with error: ${result.error}`));
          } else {
            // Still in progress, check again after a delay
            setTimeout(checkStatus, 2000);
          }
        });
    };
    checkStatus();
  }).timeout(30000); // Long timeout for video generation completion

  it('should return 404 for a non-existent job status', (done) => {
    chai.request(app)
      .get(`/api/status/non-existent-job-id`)
      .end((err, res) => {
        expect(res).to.have.status(404);
        expect(res.body).to.be.an('object');
        expect(res.body).to.have.property('error').eql('Job not found.');
        done();
      });
  });

  it('should serve static audio files', (done) => {
    if (!generatedAudioId) {
      return done(new Error('Audio ID not generated. Skipping static audio test.'));
    }
    chai.request(app)
      .get(`/storage/audio/${generatedAudioId}.mp3`)
      .end((err, res) => {
        expect(res).to.have.status(200);
        expect(res).to.have.header('Content-Type', 'application/octet-stream'); // Or audio/mpeg if it were a real MP3
        done();
      });
  });

  it('should serve static video files', (done) => {
    if (!generatedVideoJobId) {
      return done(new Error('Video Job ID not generated. Skipping static video test.'));
    }
    // Ensure the video file exists from the previous test
    const videoFilePath = path.join(__dirname, '../storage/videos', `${generatedVideoJobId}.mp4`);
    if (!fs.existsSync(videoFilePath)) {
      fs.writeFileSync(videoFilePath, 'dummy video content'); // Create dummy if not created by FFmpeg stub
    }

    chai.request(app)
      .get(`/storage/videos/${generatedVideoJobId}.mp4`)
      .end((err, res) => {
        expect(res).to.have.status(200);
        expect(res).to.have.header('Content-Type', 'application/octet-stream'); // Or video/mp4 if it were a real MP4
        done();
      });
  });
});
