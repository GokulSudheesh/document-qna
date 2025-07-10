import React, { useCallback } from "react";
import Markdown from "markdown-to-jsx";
import { ChatHistoryItem } from "@/client/types.gen";
import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { TChatState } from "@/types/chat";
import Cursor from "./cursor";

type Props = {
  className?: string;
  currentChatState: TChatState;
  handleHeightChange?: (height: number) => void;
} & ChatHistoryItem;

const ChatItem = ({
  className,
  id,
  message,
  role,
  references,
  currentChatState,
  handleHeightChange,
}: Props) => {
  const elementRef = useCallback(
    (node: HTMLDivElement) => {
      if (!node) return;
      const resizeObserver = new ResizeObserver(() => {
        handleHeightChange?.(node.clientHeight);
      });
      resizeObserver.observe(node);
    },
    [id]
  );

  return (
    <div
      ref={elementRef}
      className={cn("w-full flex gap-4 p-4", className, {
        "bg-accent text-accent-foreground": role === "assistant",
      })}
    >
      {role === "user" ? (
        <div className="flex flex-shrink-0 items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground">
          <User />
        </div>
      ) : (
        <div className="flex flex-shrink-0 items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground">
          <Bot />
        </div>
      )}
      <div className="flex">
        <Markdown
          options={{
            overrides: {
              script: {
                component: () => <></>, // Disable script tags
              },
              Cursor: {
                component: Cursor,
              },
            },
            // disableParsingRawHTML: true,
          }}
        >
          {currentChatState === "stream" ? message + "<Cursor />" : message}
        </Markdown>
      </div>
    </div>
  );
};

export default ChatItem;
