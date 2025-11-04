import React from "react";
import { Plus, Search, BookOpen, MessageSquare } from "lucide-react";

export default function Sidebar({ chats, activeChat, onNewChat, onSelectChat }) {
  return (
    <div className="w-64 bg-zinc-900 text-white flex flex-col">
      <div className="p-4 border-b border-gray-900 flex justify-between items-center">
        <h2 className="text-lg font-semibold">OpenChat</h2>
        <button onClick={onNewChat}>
          <Plus className="w-5 h-5" />
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto">
        <div className="p-3 text-gray-400 uppercase text-xs">Navigation</div>
        <button className="w-full text-left px-4 py-2 hover:bg-zinc-800 flex items-center gap-2">
          <Search className="w-4 h-4" /> Chat Suche
        </button>
        <button className="w-full text-left px-4 py-2 hover:bg-zinc-800 flex items-center gap-2">
          <BookOpen className="w-4 h-4" /> Library
        </button>

        <div className="p-3 text-gray-400 uppercase text-xs">Chats</div>
        {chats.length === 0 ? (
          <div className="px-4 text-sm text-gray-500">Keine Chats</div>
        ) : (
          chats.map((chat) => (
            <button
              key={chat.id}
              className={`w-full text-left px-4 py-2 text-sm flex items-center gap-2 ${
                activeChat?.id === chat.id ? "bg-gray-800" : "hover:bg-gray-800"
              }`}
              onClick={() => onSelectChat(chat)}
            >
              <MessageSquare className="w-4 h-4" />
              {chat.title}
            </button>
          ))
        )}
      </nav>
    </div>
  );
}
