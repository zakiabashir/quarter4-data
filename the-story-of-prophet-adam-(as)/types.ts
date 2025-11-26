export interface StorySectionType {
  id: string;
  title: string;
  content: string;
}

export interface StorySectionProps {
  id: string;
  title: string;
  content: string;
  onPlayRequest: (sectionId: string, text: string) => void;
  isPlaying: boolean;
}

export interface CallToActionProps {
  text: string;
  onClick: () => void;
}

export interface PlayAudioButtonProps {
  textToSpeak: string;
  sectionId: string;
  onPlayRequest: (sectionId: string, text: string) => void;
  isPlaying: boolean;
}