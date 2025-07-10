import React, { useCallback, useEffect, useRef, useState } from "react";
import { ChatHistoryItem } from "@/client/types.gen";
import ChatItem from "./chat-item";
import { scrollToBottom } from "./utils";
import { TChatState } from "@/types/chat";
import { Button } from "@/components/ui/button";
import { ArrowDown } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import Cursor from "./cursor";
import { Spinner } from "@/components/ui/spinner";

const SCROLL_BOTTOM_THRESHOLD = 75; // Threshold to determine if we are at the bottom

type Props = {
  chatHistory: ChatHistoryItem[];
  currentChatState: TChatState;
  isFetchingChatHistory?: boolean;
};

const ChatWindow = ({
  chatHistory,
  currentChatState,
  isFetchingChatHistory,
}: Props) => {
  const [showScrollBottomButton, setShowScrollBottomButton] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const chatLength = chatHistory.length;

  const handleScrollToBottom = () => {
    if (containerRef?.current) scrollToBottom(containerRef?.current);
  };

  const checkIfAtBottom = useCallback((element: HTMLDivElement): boolean => {
    const isAtBottom =
      Math.abs(
        element.scrollHeight - element.scrollTop - element.clientHeight
      ) <= SCROLL_BOTTOM_THRESHOLD;
    return isAtBottom;
  }, []);

  const handleScroll = useCallback(
    (e: React.UIEvent<HTMLDivElement>) => {
      const isAtBottom = checkIfAtBottom(e.currentTarget);
      setShowScrollBottomButton(!isAtBottom);
    },
    [checkIfAtBottom]
  );

  // Scroll to the bottom of the chat window when new messages are added
  const handleChatItemHeightChange = useCallback(
    (_height: number) => {
      if (currentChatState !== "stream" || !containerRef?.current) return;
      // console.log("[LOG] Height changed:", height);
      const isAtBottom = checkIfAtBottom(containerRef.current);
      if (!isAtBottom) return;
      scrollToBottom(containerRef.current);
    },
    [currentChatState, checkIfAtBottom]
  );

  // Scroll to the bottom of the chat window when new messages are added
  useEffect(() => {
    if (containerRef?.current) scrollToBottom(containerRef?.current);
  }, [chatLength]);

  if (isFetchingChatHistory)
    return (
      <div className="flex justify-center h-full w-full min-h-0">
        <Spinner className="m-auto text-sidebar-foreground/70" size="large" />
      </div>
    );
  return (
    <div className="relative flex h-full min-h-0">
      <div
        ref={containerRef}
        className="flex flex-col gap-2 w-full max-h-full overflow-y-auto
        [&::-webkit-scrollbar]:w-1
        [&::-webkit-scrollbar-track]:rounded-full
        [&::-webkit-scrollbar-track]:bg-gray-100
        [&::-webkit-scrollbar-thumb]:rounded-full
        [&::-webkit-scrollbar-thumb]:bg-gray-300
        dark:[&::-webkit-scrollbar-track]:bg-neutral-700
        dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"
        onScroll={handleScroll}
      >
        {chatHistory.map((item, index) => (
          <ChatItem
            key={item.id}
            className="last:mb-6"
            {...item}
            handleHeightChange={handleChatItemHeightChange}
            currentChatState={
              index === chatHistory.length - 1 && item.role === "assistant"
                ? currentChatState
                : undefined
            }
          />
        ))}
        {currentChatState === "loading" && (
          <div className="flex justify-center my-6">
            <Cursor />
          </div>
        )}
      </div>
      <AnimatePresence>
        {showScrollBottomButton && (
          <Button
            as={motion.button}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute bottom-2 translate-x-[-50%] left-1/2 size-8 shadow-lg"
            variant="outline"
            onClick={handleScrollToBottom}
          >
            <ArrowDown />
          </Button>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatWindow;
