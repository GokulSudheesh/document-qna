import React, { useCallback } from "react";
import Markdown from "markdown-to-jsx";
import { ChatHistoryItem } from "@/client/types.gen";
import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { TChatState } from "@/types/chat";
import Cursor from "./cursor";
import styles from "./style.module.css";
import FileItem from "./file-item";
import { motion, Variants } from "motion/react";

const referencesContainerVariant: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3,
    },
  },
};

type Props = {
  className?: string;
  currentChatState: TChatState;
  isLastItem: boolean;
  handleHeightChange?: (height: number) => void;
} & ChatHistoryItem;

const ChatItem = ({
  className,
  id,
  message,
  role,
  references,
  currentChatState,
  isLastItem,
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
      <div className="flex flex-col gap-4 w-full">
        <div className="flex">
          <Markdown
            className={styles["chat-mkdwn-wrapper"]}
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
        {!!references?.length && (
          <motion.div
            className="flex flex-wrap gap-2"
            variants={referencesContainerVariant}
            initial={isLastItem ? "hidden" : "show"}
            animate="show"
          >
            {references?.map((ref) => (
              <FileItem key={ref.file_id} {...ref} />
            ))}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default ChatItem;
