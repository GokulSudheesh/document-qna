import { MessageSquare, PlusIcon, Trash } from "lucide-react";
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
import { useTranslations } from "next-intl";
import { cn } from "@/lib/utils";
import { motion } from "motion/react";

type SessionItemProps = {
  session: Session;
  isSelected: boolean;
  onSelectSession?: (sessionId: string) => void;
  onDeleteSession?: (sessionId: string) => void;
};

const SessionItem = ({
  session,
  isSelected,
  onSelectSession,
  onDeleteSession,
}: SessionItemProps) => {
  const t = useTranslations();
  const onSelectCallback = () => {
    if (!session.id) return;
    onSelectSession?.(session.id);
  };
  const onDeleteCallback = () => {
    if (!session.id) return;
    onDeleteSession?.(session.id);
  };

  const sessionName = session.session_name || t("newChat");

  return (
    <SidebarMenuItem>
      <SidebarMenuButton asChild size="lg" className="p-0">
        <div className="relative flex w-full h-full group/item">
          <Button
            variant="ghost"
            className={cn("w-full py-6 justify-start", {
              "bg-accent text-accent-foreground": isSelected,
            })}
            onClick={onSelectCallback}
          >
            <MessageSquare />
            <span title={sessionName}>{sessionName}</span>
          </Button>
          <Button
            as={motion.button}
            whileTap={{ scale: 0.9 }}
            size="icon"
            className="hidden group-hover/item:flex absolute right-1 bottom-1/2 translate-y-1/2"
            variant="outline"
            onClick={onDeleteCallback}
          >
            <Trash />
          </Button>
        </div>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
};

type AppSidebarProps = {
  currentSessionId?: string | null;
  sessions: Session[];
  onCreateNewSession?: () => void;
  onSelectSession?: (sessionId: string) => void;
  onDeleteSession?: (sessionId: string) => void;
};

export function AppSidebar({
  currentSessionId,
  sessions,
  onCreateNewSession,
  onSelectSession,
  onDeleteSession,
}: AppSidebarProps) {
  const t = useTranslations();
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
            <span>{t("newChat")}</span>
            <PlusIcon />
          </Button>
          <SidebarGroupLabel className="text-md">
            {t("sessions")}
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sessions.map((session) => (
                <SessionItem
                  key={session.id}
                  isSelected={session.id === currentSessionId}
                  session={session}
                  onSelectSession={onSelectSession}
                  onDeleteSession={onDeleteSession}
                />
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
