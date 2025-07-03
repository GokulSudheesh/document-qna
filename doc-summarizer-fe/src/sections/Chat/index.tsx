"use client";
import React from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Session } from "@/client";
import { AppSidebar } from "@/components/app-sidebar";
import ChatWindow from "@/components/chat-window";
import { useChat } from "./hooks";
import { NavigationBar } from "@/components/ui/navigation-bar";

type Props = {
  initialDataSessions: Session[];
};

const Chat = ({ initialDataSessions }: Props) => {
  const { currentSessionId, chatSessions, chatHistory, handleSessionChange } =
    useChat({
      initialDataSessions,
    });
  return (
    <SidebarProvider>
      <AppSidebar
        currentSessionId={currentSessionId}
        sessions={chatSessions}
        onSelectSession={handleSessionChange}
      />
      <div className="flex flex-col w-full h-full">
        <NavigationBar />
        <main className="flex w-full h-[calc(100dvh-68.8px)] relative">
          <ChatWindow chatHistory={chatHistory} />
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Chat;
