import React from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatWindow from "./chat-window";
import ChatInput from "./chat-input";
import { TChatState } from "@/types/chat";

type Props = {
  currentSessionId: string | null;
  currentChatState: TChatState;
  chatHistory: ChatHistoryItem[];
  isFetchingChatHistory?: boolean;
  handleUploadFile?: () => void;
  handleSendMessage: (message: string) => void;
};

const Chat = ({
  currentSessionId,
  chatHistory,
  currentChatState,
  isFetchingChatHistory,
  handleUploadFile,
  handleSendMessage,
}: Props) => {
  const isChatInputDisabled =
    !currentSessionId ||
    currentChatState === "loading" ||
    currentChatState === "stream";

  return (
    <div className="flex flex-col w-full h-full text-base">
      <ChatWindow
        chatHistory={chatHistory}
        currentChatState={currentChatState}
        isFetchingChatHistory={isFetchingChatHistory}
      />
      <div className="flex mx-4 md:mx-16 mt-auto py-4">
        <ChatInput
          isDisabled={isChatInputDisabled}
          handleSendMessage={handleSendMessage}
          handleUploadFile={handleUploadFile}
        />
      </div>
    </div>
  );
};

export default Chat;
