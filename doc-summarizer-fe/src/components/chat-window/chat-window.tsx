import React from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatItem from "./chat-item";

type Props = {
  chatHistory: ChatHistoryItem[];
};

const ChatWindow = ({ chatHistory }: Props) => {
  return (
    <div
      className="flex flex-col gap-2 w-full max-h-full overflow-y-auto
        [&::-webkit-scrollbar]:w-1
        [&::-webkit-scrollbar-track]:rounded-full
        [&::-webkit-scrollbar-track]:bg-gray-100
        [&::-webkit-scrollbar-thumb]:rounded-full
        [&::-webkit-scrollbar-thumb]:bg-gray-300
        dark:[&::-webkit-scrollbar-track]:bg-neutral-700
        dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"
    >
      {chatHistory.map((item) => (
        <ChatItem key={item.id} {...item} />
      ))}
    </div>
  );
};

export default ChatWindow;
