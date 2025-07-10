import React from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatWindow from "./chat-window";
import ChatInput from "./chat-input";
import { TChatState } from "@/types/chat";

type Props = {
  currentChatState: TChatState;
  chatHistory: ChatHistoryItem[];
  handleSendMessage: (message: string) => void;
};

const Chat = ({ chatHistory, currentChatState, handleSendMessage }: Props) => {
  return (
    <div className="flex flex-col w-full h-full text-base">
      <ChatWindow
        chatHistory={chatHistory}
        currentChatState={currentChatState}
      />
      <div className="flex mx-16 mt-auto py-4">
        <ChatInput
          isDisabled={
            currentChatState === "loading" || currentChatState === "stream"
          }
          handleSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
};

export default Chat;
