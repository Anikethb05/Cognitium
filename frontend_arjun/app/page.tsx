"use client";

import { useState, useEffect, useRef } from "react";
import TextareaAutosize from "react-textarea-autosize";

interface Message {
  mode: string;
  content: string;
}

export default function Home() {
  const [mode, setMode] = useState("Whiteboard");
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const modes = ["Whiteboard", "Manim", "Code", "Chat"];

  const handleSend = () => {
    if (prompt.trim() === "") return;
    const newMessage = { mode, content: prompt };
    setMessages((prev) => [...prev, newMessage]);
    setPrompt("");
  };

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="min-h-screen flex flex-col bg-[#1f1f1f] text-white">
      {/* Messages Container */}
      <div className="flex-1 overflow-auto p-4">
        {messages.map((msg, index) => (
          <div key={index} className="mb-4">
            <div className="text-lg text-gray-400 mb-1">{msg.mode}:</div>
            <div className="p-3 bg-[#2c2c2c] rounded-lg">
              {msg.content}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Prompt Bar Container with 30px bottom margin */}
      <div className="w-full max-w-3xl mx-auto bg-[#2c2c2c] rounded-xl p-4 mb-[30px]">
        {/* Row 1: Mode Buttons */}
        <div className="flex flex-wrap items-center gap-2 mb-2">
          {modes.map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`px-3 py-1 text-sm rounded-full transition-colors ${
                mode === m
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-300 hover:bg-[#3a3a3a]"
              }`}
            >
              {m}
            </button>
          ))}
        </div>

        {/* Row 2: Dynamic Textarea + Send Button */}
        <div className="flex items-end gap-2">
          <TextareaAutosize
            minRows={1}
            placeholder={`Enter prompt for ${mode}...`}
            className="flex-grow bg-transparent text-white placeholder-gray-400 focus:outline-none"
            style={{ resize: "none" }}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button
            onClick={handleSend}
            className="p-2 text-gray-300 hover:text-white rounded-full hover:bg-[#3a3a3a] transition-colors"
          >
            {/* Send Icon (Paper-Plane) */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path d="M15.864.5a.5.5 0 0 1 .11.73l-7.5 10a.5.5 0 0 1-.58.16l-3.48-1.32-1.32-3.48a.5.5 0 0 1 .16-.58l10-7.5a.5.5 0 0 1 .73.11zm-6.85 7.3l-2.55.96.96 2.55 1.59-.59 2.25-2.92-2.25-2.92-1.59-.59-.96 2.55 2.55.96z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

