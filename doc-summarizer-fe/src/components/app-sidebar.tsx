import { MessageSquare, PlusIcon } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Session } from "@/client";
import { Button } from "@/components/ui/button";

type SessionItemProps = {
  session: Session;
  onSelectSession?: (sessionId: string) => void;
};

const SessionItem = ({ session, onSelectSession }: SessionItemProps) => {
  const onSelectCallback = () => {
    if (!session.id) return;
    onSelectSession?.(session.id);
  };

  return (
    <SidebarMenuItem>
      <SidebarMenuButton asChild size="lg">
        <Button
          variant="ghost"
          className="w-full justify-start"
          onClick={onSelectCallback}
        >
          <MessageSquare />
          <span>{session.session_name}</span>
        </Button>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
};

type AppSidebarProps = {
  sessions: Session[];
  onCreateNewSession?: () => void;
  onSelectSession?: (sessionId: string) => void;
};

export function AppSidebar({
  sessions,
  onCreateNewSession,
  onSelectSession,
}: AppSidebarProps) {
  return (
    <Sidebar>
      <SidebarContent
        className="overflow-y-auto
  [&::-webkit-scrollbar]:w-1
  [&::-webkit-scrollbar-track]:rounded-full
  [&::-webkit-scrollbar-track]:bg-gray-100
  [&::-webkit-scrollbar-thumb]:rounded-full
  [&::-webkit-scrollbar-thumb]:bg-gray-300
  dark:[&::-webkit-scrollbar-track]:bg-neutral-700
  dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"
      >
        <SidebarGroup>
          <Button
            className="justify-start w-full text-md font-medium !px-2"
            size="lg"
            variant="ghost"
            onClick={onCreateNewSession}
          >
            <span>New Chat</span>
            <PlusIcon />
          </Button>
          <SidebarGroupLabel className="text-md">Sessions</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sessions.map((session) => (
                <SessionItem
                  key={session.id}
                  session={session}
                  onSelectSession={onSelectSession}
                />
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
