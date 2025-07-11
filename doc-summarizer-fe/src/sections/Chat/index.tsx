"use client";
import React, { useCallback } from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Session } from "@/client";
import { AppSidebar } from "@/components/app-sidebar";
import ChatWindow from "@/components/chat-window";
import { useChat } from "./hooks";
import { NavigationBar } from "@/components/ui/navigation-bar";
import CreateSession from "@/components/file-upload/create-session";
import { useDisclosure } from "@/components/ui/dialog";
import UpdateSession from "@/components/file-upload/update-session";

type Props = {
  initialDataSessions: Session[];
};

const Chat = ({ initialDataSessions }: Props) => {
  const {
    currentSessionId,
    chatSessions,
    chatHistory,
    currentChatState,
    isFetchingChatHistory,
    fileList,
    handleSessionChange,
    handleSessionDelete,
    handleSendMessage,
    onFileUploadSuccessCallback,
  } = useChat({
    initialDataSessions,
  });

  const { isOpen: isCreateSessionOpen, setIsOpen: setIsCreateSessionOpen } =
    useDisclosure();

  const { isOpen: isUpdateSessionOpen, setIsOpen: setIsUpdateSessionOpen } =
    useDisclosure();

  const onCreateNewSession = useCallback(() => {
    setIsCreateSessionOpen(true);
  }, [setIsCreateSessionOpen]);

  const onFileUploadButtonClick = useCallback(() => {
    setIsUpdateSessionOpen(true);
  }, [setIsUpdateSessionOpen]);

  return (
    <>
      <SidebarProvider>
        <AppSidebar
          currentSessionId={currentSessionId}
          sessions={chatSessions}
          onSelectSession={handleSessionChange}
          onDeleteSession={handleSessionDelete}
          onCreateNewSession={onCreateNewSession}
        />
        <div className="flex flex-col w-full h-full">
          <NavigationBar />
          <main className="flex w-full h-[calc(100dvh-68.8px)] relative">
            <ChatWindow
              currentSessionId={currentSessionId}
              chatHistory={chatHistory}
              currentChatState={currentChatState}
              isFetchingChatHistory={isFetchingChatHistory}
              handleSendMessage={handleSendMessage}
              handleUploadFile={onFileUploadButtonClick}
            />
          </main>
        </div>
      </SidebarProvider>
      <CreateSession
        isOpen={isCreateSessionOpen}
        setIsOpen={setIsCreateSessionOpen}
        onFileUploadSuccessCallback={onFileUploadSuccessCallback}
      />
      <UpdateSession
        sessionId={currentSessionId}
        isOpen={isUpdateSessionOpen}
        setIsOpen={setIsUpdateSessionOpen}
        onFileUploadSuccessCallback={onFileUploadSuccessCallback}
        uploadedFiles={fileList}
      />
    </>
  );
};

export default Chat;
