import React, { useRef, useState, useEffect, useCallback } from 'react';
import StorySection from './components/StorySection';
import CallToActionButton from './components/CallToActionButton';
import PlayAudioButton from './components/PlayAudioButton';
import { STORY_SECTIONS } from './constants';
import { GoogleGenAI } from '@google/genai';
import { decodeBase64, decodeAudioData } from './utils';

// Helper function to create an AudioContext if one doesn't exist
const getAudioContext = () => {
  if (typeof window !== 'undefined' && (window as any)._audioContext) {
    return (window as any)._audioContext;
  }
  // Fix: Removed 'webkitAudioContext' as it's deprecated and 'AudioContext' is standard.
  const ctx = new window.AudioContext({ sampleRate: 24000 });
  if (typeof window !== 'undefined') {
    (window as any)._audioContext = ctx;
  }
  return ctx;
};

const App: React.FC = () => {
  const [currentPlayingSectionId, setCurrentPlayingSectionId] = useState<string | null>(null);
  const audioSourceRef = useRef<AudioBufferSourceNode | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  // Initialize Gemini API client
  const aiRef = useRef<GoogleGenAI | null>(null);
  useEffect(() => {
    aiRef.current = new GoogleGenAI({ apiKey: process.env.API_KEY });
  }, []);

  // Stop any currently playing audio
  const stopAudio = useCallback(() => {
    if (audioSourceRef.current) {
      audioSourceRef.current.stop();
      audioSourceRef.current.disconnect();
      audioSourceRef.current = null;
    }
    setCurrentPlayingSectionId(null);
  }, []);

  // Play audio for a given text and section ID
  const onPlayRequest = useCallback(async (sectionId: string, text: string) => {
    stopAudio(); // Stop any current playback

    if (!text || !aiRef.current) {
      // If no text or already paused, just stop
      return;
    }

    setCurrentPlayingSectionId(sectionId); // Set the new playing section

    try {
      if (!audioContextRef.current) {
        audioContextRef.current = getAudioContext();
      }
      const audioContext = audioContextRef.current;

      const response = await aiRef.current.models.generateContent({
        model: 'gemini-2.5-flash-preview-tts',
        contents: [{ parts: [{ text: text }] }],
        config: {
          responseModalities: ['AUDIO'],
          speechConfig: {
            voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Kore' } },
          },
        },
      });

      const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;

      if (base64Audio) {
        const decodedBytes = decodeBase64(base64Audio);
        const audioBuffer = await decodeAudioData(
          decodedBytes,
          audioContext,
          24000, // Sample rate from Gemini TTS is 24000
          1,     // Number of channels (mono)
        );

        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContext.destination);

        source.onended = () => {
          if (currentPlayingSectionId === sectionId) { // Only clear if this section is still the one playing
            stopAudio();
          }
        };

        source.start(0);
        audioSourceRef.current = source;
      } else {
        throw new Error('No audio data received from the API.');
      }
    } catch (error) {
      console.error('Error playing audio:', error);
      alert('Failed to play audio. Please try again. ' + (error instanceof Error ? error.message : ''));
      stopAudio(); // Ensure state is reset on error
    }
  }, [stopAudio, currentPlayingSectionId]);

  const handleFollowClick = () => {
    alert('Thank you for your interest! In a real app, this would lead to a channel or subscription page.');
    // In a real application, this would navigate to a channel, open a modal, or trigger an external link.
  };

  const introText = `In the name of Allah, the Most Merciful, the Most Compassionate.
    Aaj hum baat karne ja rahe hain insani tareekh ki sab se pehli kahani — Hazrat Adam (AS) ki kahani.
    Ek aisi kahani jo hamein batati hai ke hum kahan se aaye hain… aur Allah ne humein kis maqam par paida kiya.`;

  const outroText = `Agar aap ko yeh kahani pasand aayi to mazeed Prophets Stories ke liye channel ko zaroor follow karein.
    Allah hum sab ko hidayat de. Ameen.`;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-8 px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <header className="w-full bg-blue-700 text-white p-6 md:p-8 text-center shadow-lg mb-8 rounded-b-xl">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">
          The Story of Prophet Adam (AS)
        </h1>
        <p className="mt-2 text-xl md:text-2xl font-light opacity-90">
          The Beginning of Humanity
        </p>
      </header>

      <main className="container max-w-4xl mx-auto px-4">
        {/* Intro */}
        <section id="intro" className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-6 md:p-8 rounded-lg shadow-xl mb-12 text-center">
          <div className="flex justify-between items-center mb-4 border-b border-blue-400 pb-2">
            <p className="text-xl md:text-2xl leading-relaxed font-light text-left">
              In the name of Allah, the Most Merciful, the Most Compassionate.
              <br className="my-2" />
              Aaj hum baat karne ja rahe hain insani tareekh ki sab se pehli kahani — Hazrat Adam (AS) ki kahani.
              <br />
              Ek aisi kahani jo hamein batati hai ke hum kahan se aaye hain… aur Allah ne humein kis maqam par paida kiya.
            </p>
            <PlayAudioButton
              textToSpeak={introText}
              sectionId="intro"
              onPlayRequest={onPlayRequest}
              isPlaying={currentPlayingSectionId === 'intro'}
            />
          </div>
        </section>

        {/* Story Sections */}
        {STORY_SECTIONS.map((section) => (
          <StorySection
            key={section.id}
            id={section.id}
            title={section.title}
            content={section.content}
            onPlayRequest={onPlayRequest}
            isPlaying={currentPlayingSectionId === section.id}
          />
        ))}

        {/* Outro */}
        <section id="outro" className="bg-gradient-to-r from-green-500 to-teal-600 text-white p-6 md:p-8 rounded-lg shadow-xl mt-12 text-center max-w-2xl lg:max-w-3xl mx-auto">
          <div className="flex justify-between items-center mb-4 border-b border-green-400 pb-2">
            <h2 className="text-2xl md:text-3xl font-semibold text-left">Conclusion</h2>
            <PlayAudioButton
              textToSpeak={outroText}
              sectionId="outro"
              onPlayRequest={onPlayRequest}
              isPlaying={currentPlayingSectionId === 'outro'}
            />
          </div>
          <p className="text-lg md:text-xl leading-relaxed mb-6 text-left">
            Agar aap ko yeh kahani pasand aayi to mazeed Prophets Stories ke liye channel ko zaroor follow karein.
            <br />
            Allah hum sab ko hidayat de. Ameen.
          </p>
          <CallToActionButton text="Follow for More Stories" onClick={handleFollowClick} />
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full bg-gray-800 text-gray-300 p-6 md:p-8 text-center mt-12 rounded-t-xl shadow-inner">
        <p className="text-sm md:text-base">
          &copy; {new Date().getFullYear()} Prophets Stories. All rights reserved.
        </p>
        <p className="mt-2 text-xs opacity-75">
          Dedicated to spreading knowledge and wisdom.
        </p>
      </footer>
    </div>
  );
};

export default App;