import React, { useState, useRef, useEffect } from "react";

export default function ChatWindow({ chat, setChats }) {
    const [message, setMessage] = useState("");
    const chatEndRef = useRef();

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chat]);

    if (!chat) {
        return (
            <div className="flex-1 flex items-center justify-center bg-zinc-800 text-gray-500">
                Wähle einen Chat oder starte einen neuen.
            </div>
        );
    }

    const handleSend = () => {
        if (!message.trim()) return;

        const userMessage = { role: "user", content: message };
        const newMessages = [...chat.messages, userMessage];
        setChats((prev) =>
            prev.map((c) =>
                c.id === chat.id ? { ...c, messages: newMessages } : c
            )
        );
        setMessage("");
    };

    return (
        <div className="flex-1 flex flex-col h-full bg-zinc-800" >
            <div className="flex-1 overflow-y-auto p-4 space-y-2"  style={{ width: "50%", margin: "0 auto"}}>
                {chat.messages.map((msg, i) => (
                    <div
                        key={i}
                        className={`p-2 rounded-lg max-w-lg ${msg.role === "user"
                                ? "bg-blue-100 self-end"
                                : "bg-gray-200 self-start"
                            }`}
                    >
                        {msg.content}
                    </div>
                ))}
                <div ref={chatEndRef} />
            </div>

            <div className="p-3 flex items-center bg-zinc-800" style={{ width: "50%", margin: "0 auto", marginBottom: "2%"}}>
                <input
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    className="flex-1 p-2 rounded-xl border bg-zinc-700 border-zinc-500 text-white focus:outline-none focus:ring"
                    placeholder="Nachricht eingeben..."
                >
                </input>
                <button
                    onClick={handleSend}
                    className="ml-2 bg-slate-500 text-white px-4 py-2 rounded-md hover:bg-slate-700"
                >
                    Senden
                </button>

            </div>
        </div>
    );
}
