import React, { useState, useEffect } from 'react';
import { PlayAudioButtonProps } from '../types';

const PlayAudioButton: React.FC<PlayAudioButtonProps> = ({ textToSpeak, sectionId, onPlayRequest, isPlaying }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handlePlayClick = async () => {
    if (isPlaying) {
      // If currently playing, this is a pause request for the current section
      onPlayRequest(sectionId, ''); // Signal to stop current playback
    } else {
      // If not playing, this is a request to play this section
      setIsLoading(true);
      await onPlayRequest(sectionId, textToSpeak);
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handlePlayClick}
      className={`flex items-center justify-center px-4 py-2 rounded-full text-sm font-medium transition-colors duration-300 ease-in-out shadow-md
        ${isPlaying ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-blue-600 hover:bg-blue-700 text-white'}
        ${isLoading ? 'opacity-70 cursor-not-allowed' : ''} `}
      disabled={isLoading}
      aria-label={isPlaying ? `Pause audio for ${sectionId}` : `Play audio for ${sectionId}`}
    >
      {isLoading ? (
        <>
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </>
      ) : isPlaying ? (
        <>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.5 7.5a.5.5 0 00-.5.5v4a.5.5 0 001 0V8a.5.5 0 00-.5-.5z" clipRule="evenodd" />
          </svg>
          Pause
        </>
      ) : (
        <>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.5 7.5a.5.5 0 00-.5.5v4a.5.5 0 001 0V8a.5.5 0 00-.5-.5z" clipRule="evenodd" />
            <path d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.5 7.5a.5.5 0 00-.5.5v4a.5.5 0 001 0V8a.5.5 0 00-.5-.5z" />
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.5 7.5a.5.5 0 00-.5.5v4a.5.5 0 001 0V8a.5.5 0 00-.5-.5z" clipRule="evenodd" />
            <path d="M9.707 8.293a1 1 0 010 1.414l-2 2a1 1 0 01-1.414-1.414L7.586 10H5a1 1 0 110-2h2.586l-1.293-1.293a1 1 0 011.414-1.414l2 2zM12 11a1 1 0 100-2 1 1 0 000 2z" />
          </svg>
          Play Audio
        </>
      )}
    </button>
  );
};

export default PlayAudioButton;
