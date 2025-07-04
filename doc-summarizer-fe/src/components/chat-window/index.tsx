import React from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatWindow from "./chat-window";
import ChatInput from "./chat-input";

type Props = {
  chatHistory: ChatHistoryItem[];
  handleSendMessage: (message: string) => void;
};

const Chat = ({ chatHistory, handleSendMessage }: Props) => {
  return (
    <div className="flex flex-col w-full h-full text-base">
      <ChatWindow chatHistory={chatHistory} />
      <div className="flex mx-16 mt-auto py-4">
        <ChatInput handleSendMessage={handleSendMessage} />
      </div>
    </div>
  );
};

export default Chat;
