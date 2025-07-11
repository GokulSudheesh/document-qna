import { useCallback, useContext, useMemo, useState } from "react";
import {
  chatHistoryApiV1ChatHistorySessionIdGet,
  ChatHistoryItem,
  ChatHistoryResponse,
  FileUploadResponse,
  GetFileResponse,
  listFilesApiV1FileListGet,
  listSessionsApiV1SessionListGet,
  Reference,
  Session,
} from "@/client";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { API_URL } from "@/config";
import { v4 as uuidv4 } from "uuid";
import { ChatSSEEvent, ChatState, TChatState } from "@/types/chat";
import { toast } from "sonner";
import { useTranslations } from "next-intl";
import { deleteSession } from "@/apiHelpers/session";
import { AlertDialogueContext } from "@/providers/AlertDialogueProvider";

// Refetch sessions list for every 10 chat history items
const SESSIONS_LIST_REFETCH_COUNT = 10;

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
  fileList: GetFileResponse[];
  chatSessions: Session[];
  currentChatState: TChatState;
  isFetchingChatHistory?: boolean;
  handleSessionChange: (sessionId: string) => void;
  handleSessionDelete: (sessionId: string) => void;
  handleSendMessage: (message: string) => void;
  onFileUploadSuccessCallback: (data: FileUploadResponse) => void;
}

export const useChat = ({
  initialDataSessions,
}: IUseChatArgs): IUseChatReturn => {
  const { setDialogue } = useContext(AlertDialogueContext);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(
    initialDataSessions?.[0]?.id || null
  );
  const [chatSessionsState, setChatSessionsState] = useState<ChatState[]>([]);

  const t = useTranslations();
  const currentChatState = useMemo(
    () =>
      chatSessionsState.find((state) => state.sessionId === currentSessionId)
        ?.status,
    [chatSessionsState, currentSessionId]
  );

  const queryClient = useQueryClient();

  const { data: chatHistory, isFetching: isFetchingChatHistory } = useQuery({
    enabled: !!currentSessionId,
    refetchOnWindowFocus: false,
    queryKey: ["chat-history", currentSessionId],
    select: (data) => data?.data?.data || [],
    queryFn: () =>
      chatHistoryApiV1ChatHistorySessionIdGet({
        path: { session_id: currentSessionId },
      }),
  });

  const { data: fileList, isFetching: isFetchingFileList } = useQuery({
    enabled: !!currentSessionId,
    queryKey: ["chat-files", currentSessionId],
    select: (data) => data?.data?.data || [],
    queryFn: () =>
      listFilesApiV1FileListGet({
        query: { session_id: currentSessionId },
      }),
  });

  const { data: chatSessions } = useQuery({
    queryKey: ["chat-sessions"],
    queryFn: () => getSessions(),
    placeholderData: initialDataSessions,
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

  const updateAIChatReferences = useCallback(
    (
      sessionId: string,
      { id, references }: { id: string; references: Reference[] | null }
    ) => {
      queryClient.setQueryData(
        ["chat-history", sessionId],
        (oldData: { data: ChatHistoryResponse; error: undefined }) => ({
          ...oldData,
          data: {
            success: true,
            data: oldData?.data?.data.map((item: ChatHistoryItem) =>
              item.id === id
                ? {
                    ...item,
                    references,
                  }
                : item
            ),
          },
        })
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

  const updateSessionsUpdatedAtTime = useCallback(
    (sessionId: string) => {
      queryClient.setQueryData(["chat-sessions"], (oldSessions: Session[]) => {
        const session = oldSessions.find((s) => s.id === sessionId);
        if (!session) return oldSessions;
        return [
          { ...session, updated: new Date().toISOString() },
          ...oldSessions.filter((s) => s.id !== sessionId),
        ];
      });
    },
    [queryClient]
  );

  const handleMessageEvent = useCallback(
    (sessionId: string, ev: ChatSSEEvent) => {
      try {
        console.log("[SSE] Message received:", ev.data);
        setChatState(sessionId, "stream");
        ev.data = JSON.parse(ev.data);
        switch (ev.event) {
          case "message":
            updateAIChatItem(sessionId, {
              id: ev.data.id,
              message: ev.data.message,
              references: null,
            });
            return;
          case "references":
            updateAIChatReferences(sessionId, {
              id: ev.data.id,
              references: ev.data.references,
            });
            return;
        }
      } catch (error) {
        console.error("[SSE] Error parsing data:", error);
      }
    },
    [setChatState, updateAIChatItem, updateAIChatReferences]
  );

  const handleConnectionClose = useCallback(
    (sessionId: string) => {
      console.log("[SSE] Connection closed.");
      setChatState(sessionId, undefined);
      if ((chatHistory?.length ?? 0) % SESSIONS_LIST_REFETCH_COUNT === 0)
        queryClient.invalidateQueries({
          queryKey: ["chat-sessions"],
        });
    },
    [queryClient, chatHistory, setChatState]
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
      // Update the current session's last updated time
      updateSessionsUpdatedAtTime(currentSessionId);
      // Set the chat state to loading
      console.log("[LOG]", "Sending message:", message);
      setChatState(currentSessionId, "loading");
      fetchEventSource(`${API_URL}/api/v1/chat/sse/${currentSessionId}`, {
        method: "POST",
        openWhenHidden: true,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: message,
        }),
        async onopen(_response) {
          console.log("[SSE] Connection opened.");
        },
        onmessage(ev) {
          handleMessageEvent(currentSessionId, ev as ChatSSEEvent);
        },
        onclose() {
          handleConnectionClose(currentSessionId);
        },
        onerror(err) {
          console.error("[SSE] Error:", err);
          toast.error(t("chatSSEError"));
          setChatState(currentSessionId, undefined);
          throw err; // rethrow to stop the operation
        },
      });
    },
    [
      currentSessionId,
      handleConnectionClose,
      appendToChatHistory,
      setChatState,
      handleMessageEvent,
    ]
  );

  const { mutate: deleteSessionMutate } = useMutation({
    mutationFn: deleteSession,
    onError: () => {
      toast.error(t("deleteSessionErrorMessage"));
    },
  });

  const handleSessionDeleteCallback = useCallback(
    (sessionId: string) => {
      queryClient.setQueryData(["chat-sessions"], (oldSessions: Session[]) => {
        return oldSessions.filter((s) => s.id !== sessionId);
      });
      deleteSessionMutate(sessionId, {
        onSettled: () => {
          queryClient.invalidateQueries({
            queryKey: ["chat-sessions"],
          });
        },
      });
    },
    [queryClient]
  );

  const handleSessionDelete = useCallback(
    (sessionId: string) => {
      setDialogue?.({
        isOpen: true,
        type: "warning",
        title: t("deleteSession.title"),
        content: t("deleteSession.content"),
        primaryCtaLabel: t("yes"),
        secondaryCtaLabel: t("no"),
        primaryCtaHandler: () => handleSessionDeleteCallback(sessionId),
      });
    },
    [t, setDialogue, handleSessionDeleteCallback]
  );

  const upsertSessionList = useCallback(
    (sessionId: string, files: string[]) => {
      queryClient.setQueryData(["chat-sessions"], (oldSessions: Session[]) => {
        const session = oldSessions.find((s) => s.id === sessionId);
        if (session) {
          // Update existing session
          return [
            {
              ...session,
              files: [...(session.files || []), ...files],
              updated: new Date().toISOString(),
            },
            ...oldSessions.filter((s) => s.id !== sessionId),
          ];
        } else {
          // Add new session
          const timeStamp = new Date().toISOString();
          return [
            {
              created: timeStamp,
              updated: timeStamp,
              session_name: "",
              files,
              id: sessionId,
            },
            ...oldSessions,
          ];
        }
      });
    },
    [queryClient]
  );

  const onFileUploadSuccessCallback = useCallback(
    (data: FileUploadResponse) => {
      if (!data?.data || !data?.data?.session_id) return;
      setCurrentSessionId(data.data.session_id);
      upsertSessionList(
        data.data.session_id,
        data.data.files?.map((file) => file.id) || []
      );
    },
    [upsertSessionList]
  );

  return {
    currentSessionId,
    chatHistory: chatHistory || [],
    fileList: fileList || [],
    chatSessions: chatSessions || [],
    currentChatState,
    isFetchingChatHistory,
    handleSessionChange,
    handleSessionDelete,
    handleSendMessage,
    onFileUploadSuccessCallback,
  };
};
