import React from "react";
import { Mic } from "lucide-react";

export default function VoiceButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: "none",
        border: "1px solid #ccc",
        borderRadius: 8,
        cursor: "pointer",
        padding: 0,
        marginLeft: 8,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: 60,
        width: 48,
      }}
      aria-label="Voice Input"
    >
  <Mic size={24} color="#222" />
    </button>
  );
}
