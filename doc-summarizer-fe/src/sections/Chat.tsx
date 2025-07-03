"use client";
import React from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { chatHistoryApiV1ChatHistorySessionIdGet, Session } from "@/client";
import { useQuery } from "@tanstack/react-query";
import { AppSidebar } from "@/components/app-sidebar";
import ThemeSwitcher from "@/components/ui/theme-switcher";

type Props = {
  initialDataSessions: Session[];
};

const Chat = ({ initialDataSessions }: Props) => {
  console.log("Initial Data Sessions:", initialDataSessions);
  const sessionId = "685f07d1caa7391dbd45c23c";
  const { data: chatHistory } = useQuery({
    queryKey: ["chat-history", sessionId],
    queryFn: () =>
      chatHistoryApiV1ChatHistorySessionIdGet({
        path: { session_id: sessionId },
      }),
  });
  console.log("Chat History:", chatHistory);
  return (
    <SidebarProvider>
      <AppSidebar sessions={initialDataSessions} />
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
