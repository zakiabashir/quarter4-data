import React from 'react';
import { CallToActionProps } from '../types';

const CallToActionButton: React.FC<CallToActionProps> = ({ text, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition-colors duration-300 ease-in-out text-lg font-medium shadow-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-75"
    >
      {text}
    </button>
  );
};

export default CallToActionButton;