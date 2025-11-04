import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  const [activeChat, setActiveChat] = useState(null);
  const [chats, setChats] = useState([]);

  const handleNewChat = () => {
    const newChat = { id: Date.now(), title: "Neuer Chat", messages: [] };
    setChats([newChat, ...chats]);
    setActiveChat(newChat);
  };

  return (
    <div className="flex h-screen bg-gray-100 text-gray-900">
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        onNewChat={handleNewChat}
        onSelectChat={setActiveChat}
      />
      <ChatWindow chat={activeChat} setChats={setChats} />
    </div>
  );
}
