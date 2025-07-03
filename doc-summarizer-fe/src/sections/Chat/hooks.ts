import {
  chatHistoryApiV1ChatHistorySessionIdGet,
  ChatHistoryItem,
  listSessionsApiV1SessionListGet,
  Session,
} from "@/client";
import { useQuery } from "@tanstack/react-query";
import { useCallback, useState } from "react";

const getSessions = async (): Promise<Session[]> => {
  const data = await listSessionsApiV1SessionListGet();
  return data?.data?.data || [];
};

interface IUseChatArgs {
  initialDataSessions: Session[];
}

interface IUseChatReturn {
  currentSessionId: string | null;
  chatHistory: ChatHistoryItem[];
  chatSessions: Session[];
  handleSessionChange: (sessionId: string) => void;
}

export const useChat = ({
  initialDataSessions,
}: IUseChatArgs): IUseChatReturn => {
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(
    initialDataSessions?.[0]?.id || null
  );

  const { data: chatHistory } = useQuery({
    queryKey: ["chat-history", currentSessionId],
    queryFn: () =>
      chatHistoryApiV1ChatHistorySessionIdGet({
        path: { session_id: currentSessionId },
      }),
  });

  const { data: chatSessions } = useQuery({
    queryKey: ["chat-sessions"],
    queryFn: () => getSessions(),
    initialData: initialDataSessions,
  });

  const handleSessionChange = useCallback((sessionId: string) => {
    setCurrentSessionId(sessionId);
  }, []);

  return {
    currentSessionId,
    chatHistory: chatHistory?.data?.data || [],
    chatSessions,
    handleSessionChange,
  };
};
