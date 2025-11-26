// Utility functions for audio encoding/decoding as specified in the @google/genai guidelines.

/**
 * Decodes a base64 string into a Uint8Array.
 * @param base64 The base64 string to decode.
 * @returns The decoded Uint8Array.
 */
export function decodeBase64(base64: string): Uint8Array {
  const binaryString = atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes;
}

/**
 * Decodes raw PCM audio data (Uint8Array) into an AudioBuffer.
 * This function is designed for raw PCM data from the Gemini API, not standard audio files.
 * @param data The Uint8Array containing raw PCM audio data.
 * @param ctx The AudioContext to create the AudioBuffer with.
 * @param sampleRate The sample rate of the audio data.
 * @param numChannels The number of channels in the audio data (e.g., 1 for mono).
 * @returns A Promise that resolves with the decoded AudioBuffer.
 */
export async function decodeAudioData(
  data: Uint8Array,
  ctx: AudioContext,
  sampleRate: number,
  numChannels: number,
): Promise<AudioBuffer> {
  const dataInt16 = new Int16Array(data.buffer);
  const frameCount = dataInt16.length / numChannels;
  const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);

  for (let channel = 0; channel < numChannels; channel++) {
    const channelData = buffer.getChannelData(channel);
    for (let i = 0; i < frameCount; i++) {
      channelData[i] = dataInt16[i * numChannels + channel] / 32768.0; // Convert 16-bit PCM to float32
    }
  }
  return buffer;
}

/**
 * Encodes a Uint8Array into a base64 string.
 * @param bytes The Uint8Array to encode.
 * @returns The base64 encoded string.
 */
export function encodeBase64(bytes: Uint8Array): string {
  let binary = '';
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}
