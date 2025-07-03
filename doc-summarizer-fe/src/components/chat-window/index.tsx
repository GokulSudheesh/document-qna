import React from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatWindow from "./chat-window";
import { Textarea } from "@/components/ui/textarea";

type Props = {
  chatHistory: ChatHistoryItem[];
};

const Chat = ({ chatHistory }: Props) => {
  return (
    <div className="flex flex-col w-full h-full text-base">
      <ChatWindow chatHistory={chatHistory} />
      <div className="flex mx-16 mt-auto py-4">
        <Textarea />
      </div>
    </div>
  );
};

export default Chat;
