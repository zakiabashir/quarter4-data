import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000';

function App() {
  const [script, setScript] = useState('');
  const [voice, setVoice] = useState('male');
  const [speed, setSpeed] = useState(1.0);
  const [coverImage, setCoverImage] = useState(null);
  const [audioUrl, setAudioUrl] = useState('');
  const [videoId, setVideoId] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [voiceJobId, setVoiceJobId] = useState('');
  const [videoJobId, setVideoJobId] = useState('');
  const [voiceStatus, setVoiceStatus] = useState('');
  const [videoStatus, setVideoStatus] = useState('');
  const [voiceProgress, setVoiceProgress] = useState(0);
  const [videoProgress, setVideoProgress] = useState(0);
  const [error, setError] = useState('');

  const audioRef = useRef(null);
  const videoRef = useRef(null);

  const handleGenerateVoice = async () => {
    setError('');
    setAudioUrl('');
    setVoiceJobId('');
    setVoiceStatus('in_progress');
    setVoiceProgress(0);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/generate-voice`, { script, voice, speed });
      setAudioUrl(response.data.audioUrl);
      setVoiceStatus('completed');
      setVoiceProgress(100);
    } catch (err) {
      console.error('Error generating voice:', err);
      setError(err.response?.data?.error || 'Failed to generate voice.');
      setVoiceStatus('failed');
      setVoiceProgress(0);
    }
  };

  const handleGenerateVideo = async () => {
    setError('');
    setVideoUrl('');
    setVideoJobId('');
    setVideoStatus('in_progress');
    setVideoProgress(0);

    if (!audioUrl) {
      setError('Please generate voice first.');
      setVideoStatus('');
      return;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/api/generate-video`, {
        id: audioUrl.split('/').pop().replace('.mp3', ''), // Extract voice ID from audioUrl
        script,
        coverImageUrl: coverImage ? URL.createObjectURL(coverImage) : null, // Not directly used by backend yet
      });
      setVideoJobId(response.data.jobId);
      setVideoStatus('pending');
    } catch (err) {
      console.error('Error generating video:', err);
      setError(err.response?.data?.error || 'Failed to generate video.');
      setVideoStatus('failed');
      setVideoProgress(0);
    }
  };

  const handleCoverImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setCoverImage(e.target.files[0]);
    }
  };

  useEffect(() => {
    let videoStatusInterval;
    if (videoJobId && videoStatus !== 'completed' && videoStatus !== 'failed') {
      videoStatusInterval = setInterval(async () => {
        try {
          const response = await axios.get(`${API_BASE_URL}/api/status/${videoJobId}`);
          setVideoStatus(response.data.status);
          setVideoProgress(response.data.progress);
          if (response.data.status === 'completed') {
            setVideoUrl(`${API_BASE_URL}${response.data.result.videoUrl}`);
            clearInterval(videoStatusInterval);
          } else if (response.data.status === 'failed') {
            setError(response.data.result.error || 'Video generation failed.');
            clearInterval(videoStatusInterval);
          }
        } catch (err) {
          console.error('Error fetching video status:', err);
          setError('Failed to get video status.');
          setVideoStatus('failed');
          clearInterval(videoStatusInterval);
        }
      }, 2000);
    }
    return () => clearInterval(videoStatusInterval);
  }, [videoJobId, videoStatus]);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-4xl">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">AI Script to Video</h1>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <strong className="font-bold">Error!</strong>
            <span className="block sm:inline"> {error}</span>
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="script" className="block text-gray-700 text-sm font-bold mb-2">
            Script:
          </label>
          <textarea
            id="script"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-32"
            placeholder="Enter your script here..."
            value={script}
            onChange={(e) => setScript(e.target.value)}
          ></textarea>
        </div>

        <div className="mb-4 flex space-x-4">
          <div className="w-1/2">
            <label htmlFor="voice" className="block text-gray-700 text-sm font-bold mb-2">
              Voice:
            </label>
            <select
              id="voice"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={voice}
              onChange={(e) => setVoice(e.target.value)}
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
          <div className="w-1/2">
            <label htmlFor="speed" className="block text-gray-700 text-sm font-bold mb-2">
              Speed:
            </label>
            <input
              type="number"
              id="speed"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={speed}
              onChange={(e) => setSpeed(parseFloat(e.target.value))}
              step="0.1"
              min="0.5"
              max="2.0"
            />
          </div>
        </div>

        <div className="mb-6">
          <label htmlFor="coverImage" className="block text-gray-700 text-sm font-bold mb-2">
            Cover Image (Optional):
          </label>
          <input
            type="file"
            id="coverImage"
            accept="image/*"
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
            onChange={handleCoverImageChange}
          />
          {coverImage && (
            <p className="text-gray-500 text-xs mt-1">Selected: {coverImage.name}</p>
          )}
        </div>

        <div className="flex space-x-4 mb-6">
          <button
            onClick={handleGenerateVoice}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex-1"
            disabled={voiceStatus === 'in_progress'}
          >
            {voiceStatus === 'in_progress' ? `Generating Voice (${voiceProgress}%)` : 'Generate Voice'}
          </button>
          <button
            onClick={handleGenerateVideo}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex-1"
            disabled={!audioUrl || videoStatus === 'in_progress'}
          >
            {videoStatus === 'in_progress' ? `Generating Video (${videoProgress}%)` : 'Generate Video'}
          </button>
        </div>

        {audioUrl && (
          <div className="mb-4">
            <h3 className="text-xl font-semibold mb-2 text-gray-800">Audio Preview:</h3>
            <audio controls src={audioUrl} ref={audioRef} className="w-full">
              Your browser does not support the audio element.
            </audio>
          </div>
        )}

        {videoUrl && (
          <div className="mb-4">
            <h3 className="text-xl font-semibold mb-2 text-gray-800">Video Preview:</h3>
            <video controls src={videoUrl} ref={videoRef} className="w-full h-96 bg-black">
              Your browser does not support the video tag.
            </video>
            <a
              href={videoUrl}
              download
              className="mt-2 inline-block bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Download Video
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;