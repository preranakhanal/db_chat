"use client";
import { useEffect, useState } from "react";
import { Mic, Square } from "lucide-react";

export default function VoiceInput() {
  const [volume, setVolume] = useState(0);
  const [listening, setListening] = useState(false);

  useEffect(() => {
    let audioCtx: AudioContext | null = null;
    let analyser: AnalyserNode | null = null;
    let source: MediaStreamAudioSourceNode | null = null;
    let rafId: number;

    if (listening) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          analyser = audioCtx.createAnalyser();
          source = audioCtx.createMediaStreamSource(stream);
          source.connect(analyser);
          analyser.fftSize = 64;
          const dataArray = new Uint8Array(analyser.frequencyBinCount);

          const update = () => {
            analyser!.getByteFrequencyData(dataArray);
            // Use max value for a more dynamic bar
            const max = Math.max(...dataArray);
            setVolume(max);
            rafId = requestAnimationFrame(update);
          };
          update();
        })
        .catch((err) => {
          // Gracefully handle error (permission denied, unsupported, etc.)
          setListening(false);
          setVolume(0);
          // Optionally log error or show feedback
          console.error("getUserMedia error:", err);
        });
    }
    return () => {
      cancelAnimationFrame(rafId);
      if (audioCtx) audioCtx.close();
    };
  }, [listening]);

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => setListening((prev) => !prev)}
        aria-label={listening ? "Stop voice input" : "Start voice input"}
        className={`flex items-center justify-center w-12 h-[60px] rounded-xl border border-gray-200 bg-white transition-colors ${listening ? 'text-primary' : 'text-gray-500'} hover:text-primary focus:outline-none`}
        type="button"
      >
        <Mic size={24} />
      </button>
      {listening && (
        <>
          {/* Animated horizontal volume bar */}
          <div
            aria-label="Recording"
            className="flex items-center h-[60px]"
            style={{ width: '32px', marginRight: '4px' }}
          >
            <div
              style={{
                width: '100%',
                // Minimum height 8px, maximum 40px, scale volume between 0-40
                height: `${Math.max(8, Math.min(40, volume / 2))}px`,
                background: '#3b82f6',
                borderRadius: '4px',
                transition: 'height 0.1s',
                alignSelf: 'center',
              }}
            />
          </div>
          <button
            onClick={() => setListening(false)}
            aria-label="Pause voice input"
            className="flex items-center justify-center w-12 h-[60px] rounded-xl border border-gray-200 bg-white text-red-500 hover:text-red-700 transition-colors focus:outline-none"
            type="button"
          >
            <Square size={24} />
          </button>
        </>
      )}
    </div>
  );
}
