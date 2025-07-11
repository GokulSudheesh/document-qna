import React from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatWindow from "./chat-window";
import ChatInput from "./chat-input";
import { TChatState } from "@/types/chat";
import { Button } from "@/components/ui/button";

type Props = {
  currentSessionId: string | null;
  currentChatState: TChatState;
  chatHistory: ChatHistoryItem[];
  isFetchingChatHistory?: boolean;
  handleSendMessage: (message: string) => void;
  onCreateNewSession: () => void;
  handleUploadFile?: () => void;
};

const Chat = ({
  currentSessionId,
  chatHistory,
  currentChatState,
  isFetchingChatHistory,
  handleSendMessage,
  onCreateNewSession,
  handleUploadFile,
}: Props) => {
  const isChatInputDisabled =
    !currentSessionId ||
    currentChatState === "loading" ||
    currentChatState === "stream";

  return (
    <div className="flex flex-col w-full h-full text-base">
      {!currentSessionId && (
        <div className="flex items-center justify-center w-full h-full">
          <p className="text-muted-foreground text-base text-center">
            <span>No active session selected. Select a session or </span>
            <Button
              className="inline-flex p-0"
              variant="link"
              onClick={onCreateNewSession}
            >
              create a new session
            </Button>
            <span> to start chatting.</span>
          </p>
        </div>
      )}
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
