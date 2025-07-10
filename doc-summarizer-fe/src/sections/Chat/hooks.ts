import { useCallback, useMemo, useState } from "react";
import {
  chatHistoryApiV1ChatHistorySessionIdGet,
  ChatHistoryItem,
  ChatHistoryResponse,
  listSessionsApiV1SessionListGet,
  Reference,
  Session,
} from "@/client";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { API_URL } from "@/config";
import { v4 as uuidv4 } from "uuid";
import { ChatState, TChatState } from "@/types/chat";

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
  currentChatState: TChatState;
  handleSessionChange: (sessionId: string) => void;
  handleSendMessage: (message: string) => void;
}

export const useChat = ({
  initialDataSessions,
}: IUseChatArgs): IUseChatReturn => {
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(
    initialDataSessions?.[0]?.id || null
  );
  const [chatSessionsState, setChatSessionsState] = useState<ChatState[]>([]);

  const currentChatState = useMemo(
    () =>
      chatSessionsState.find((state) => state.sessionId === currentSessionId)
        ?.status,
    [chatSessionsState, currentSessionId]
  );

  const queryClient = useQueryClient();

  const { data: chatHistory } = useQuery({
    enabled: !!currentSessionId,
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

  const appendToChatHistory = useCallback(
    (sessionid: string, newMessage: ChatHistoryItem) => {
      queryClient.setQueryData(
        ["chat-history", sessionid],
        (oldData: { data: ChatHistoryResponse; error: undefined }) => {
          return {
            ...oldData,
            data: {
              success: true,
              data: [...(oldData?.data?.data || []), newMessage],
            },
          };
        }
      );
    },
    [queryClient]
  );

  const updateAIChatItem = useCallback(
    (
      sessionId: string,
      {
        id,
        message,
        references,
      }: { id: string; message: string; references: Reference[] | null }
    ) => {
      queryClient.setQueryData(
        ["chat-history", sessionId],
        (oldData: { data: ChatHistoryResponse; error: undefined }) => {
          const chatExists = oldData?.data?.data.find(
            (item: ChatHistoryItem) => item.id === id
          );
          if (!chatExists) {
            return {
              ...oldData,
              data: {
                success: true,
                data: [
                  ...(oldData?.data?.data || []),
                  { id, message, role: "assistant", references },
                ],
              },
            };
          }
          return {
            ...oldData,
            data: {
              success: true,
              data: oldData?.data?.data.map((item: ChatHistoryItem) =>
                item.id === id
                  ? {
                      ...item,
                      message: item.message + message,
                      role: "assistant",
                      references,
                    }
                  : item
              ),
            },
          };
        }
      );
    },
    [queryClient]
  );

  const setChatState = useCallback(
    (sessionId: string, status: TChatState) =>
      setChatSessionsState((prev) => [
        ...prev.filter((state) => state.sessionId !== sessionId),
        { sessionId, status },
      ]),
    []
  );

  const handleSendMessage = useCallback(
    (message: string) => {
      // Send the message to the current chat session
      if (!currentSessionId) return;
      appendToChatHistory(currentSessionId, {
        session_id: currentSessionId,
        id: uuidv4(),
        message,
        role: "user",
        created: new Date().toISOString(),
        references: null,
      });
      console.log("[LOG]", "Sending message:", message);
      setChatState(currentSessionId, "loading");
      fetchEventSource(`${API_URL}/api/v1/chat/sse/${currentSessionId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: message,
        }),
        async onopen(response) {
          console.log("[SSE] Connection opened.");
        },
        onmessage(ev) {
          try {
            console.log("[SSE] Message received:", ev.data);
            setChatState(currentSessionId, "stream");
            const data = JSON.parse(ev.data);
            switch (ev.event) {
              case "message":
                updateAIChatItem(currentSessionId, {
                  id: data.id,
                  message: data.message,
                  references: null,
                });
                return;
              case "references":
                return;
            }
          } catch (error) {
            console.error("[SSE] Error parsing data:", error);
          }
        },
        onclose() {
          console.log("[SSE] Connection closed.");
          setChatState(currentSessionId, undefined);
        },
        onerror(err) {
          console.error("[SSE] Error:", err);
          setChatState(currentSessionId, undefined);
          throw err; // rethrow to stop the operation
        },
      });
    },
    [currentSessionId, appendToChatHistory, updateAIChatItem, setChatState]
  );

  return {
    currentSessionId,
    chatHistory: chatHistory?.data?.data || [],
    chatSessions,
    currentChatState,
    handleSessionChange,
    handleSendMessage,
  };
};
