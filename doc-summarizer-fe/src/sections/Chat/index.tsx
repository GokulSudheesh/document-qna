"use client";
import React from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Session } from "@/client";
import { AppSidebar } from "@/components/app-sidebar";
import ThemeSwitcher from "@/components/ui/theme-switcher";
import { useChat } from "./hooks";

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
      <main>
        <div className="flex fixed top-2 right-2 z-50">
          <ThemeSwitcher />
        </div>
        <SidebarTrigger className="mt-2 ms-2 w-9 h-9" />
      </main>
    </SidebarProvider>
  );
};

export default Chat;
