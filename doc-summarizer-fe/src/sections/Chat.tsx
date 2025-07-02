"use client";
import React from "react";
import { chatHistoryApiV1ChatHistorySessionIdGet } from "@/client";
import { useQuery } from "@tanstack/react-query";

type Props = {};

const Chat = (props: Props) => {
  const sessionId = "685f07d1caa7391dbd45c23c";
  const { data: chatHistory } = useQuery({
    queryKey: ["chat-history", sessionId],
    queryFn: () =>
      chatHistoryApiV1ChatHistorySessionIdGet({
        path: { session_id: sessionId },
      }),
  });
  console.log("Chat History:", chatHistory);
  return <div>Chat</div>;
};

export default Chat;
