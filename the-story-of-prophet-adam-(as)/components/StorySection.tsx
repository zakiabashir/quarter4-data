import React from 'react';
import { StorySectionProps } from '../types';
import PlayAudioButton from './PlayAudioButton';

const StorySection: React.FC<StorySectionProps> = ({ id, title, content, onPlayRequest, isPlaying }) => {
  return (
    <section id={id} className="bg-white p-6 md:p-8 rounded-lg shadow-md mb-8 mx-auto max-w-2xl lg:max-w-3xl border border-gray-200">
      <div className="flex justify-between items-center mb-4 border-b pb-2">
        <h2 className="text-2xl md:text-3xl font-semibold text-blue-700">
          {title}
        </h2>
        <PlayAudioButton
          textToSpeak={content}
          sectionId={id}
          onPlayRequest={onPlayRequest}
          isPlaying={isPlaying}
        />
      </div>
      <p className="text-base md:text-lg leading-relaxed text-gray-700 whitespace-pre-line">
        {content}
      </p>
    </section>
  );
};

export default StorySection;