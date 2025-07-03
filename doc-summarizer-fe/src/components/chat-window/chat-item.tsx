import React from "react";
import Markdown from "markdown-to-jsx";
import { ChatHistoryItem } from "@/client/types.gen";
import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

type Props = {} & ChatHistoryItem;

const ChatItem = ({ id, message, role, references }: Props) => {
  return (
    <div
      className={cn("w-full flex gap-4 p-4 last:mb-4", {
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
        <Markdown options={{ disableParsingRawHTML: true }}>{message}</Markdown>
      </div>
    </div>
  );
};

export default ChatItem;
