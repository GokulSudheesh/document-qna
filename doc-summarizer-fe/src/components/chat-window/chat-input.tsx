import React, { useCallback, useState } from "react";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";
import { useTranslations } from "next-intl";

const CHAT_INPUT_HEIGHT = "24px";

type Props = {
  handleSendMessage: (message: string) => void;
};

const ChatInput = ({ handleSendMessage }: Props) => {
  const t = useTranslations();
  const [message, setMessage] = useState("");
  const textAreaRef = React.useRef<HTMLTextAreaElement>(null);

  const handleOnChange: React.ChangeEventHandler<HTMLTextAreaElement> =
    useCallback((e) => {
      setMessage(e.target.value);
      if (textAreaRef.current) {
        if (!e.target.value) {
          textAreaRef.current.style.height = CHAT_INPUT_HEIGHT; // Reset to initial height
        } else {
          textAreaRef.current.style.height = `${e.target.scrollHeight}px`;
        }
      }
    }, []);

  const handleOnSend = useCallback(() => {
    if (!message.trim()) return;
    handleSendMessage(message.trim());
    setMessage("");
    if (textAreaRef.current)
      textAreaRef.current.style.height = CHAT_INPUT_HEIGHT; // Reset height after sending
  }, [message, handleSendMessage]);

  const handleKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> =
    useCallback(
      (e) => {
        if (e.key === "Enter" && e.shiftKey) return;
        if (e.key === "Enter") {
          handleOnSend();
          e.preventDefault();
        }
      },
      [handleOnSend]
    );

  const handleOnSendBtnClick = useCallback(
    (e: React.MouseEvent<HTMLButtonElement>) => {
      e.stopPropagation();
      handleOnSend();
    },
    [handleOnSend]
  );

  const handleTextAreaWrapperClick = () => {
    textAreaRef.current?.focus();
  };

  return (
    <div
      onClick={handleTextAreaWrapperClick}
      className="relative cursor-text flex flex-col gap-2 border-input focus-within:border-ring focus-visible:border-ring focus-within:ring-ring/50 
      focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive 
      dark:bg-input/30 field-sizing-content w-full rounded-md border bg-transparent px-3 py-2 text-base shadow-xs transition-[color,box-shadow] 
      outline-none focus-within:ring-[3px] focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50"
    >
      <textarea
        ref={textAreaRef}
        value={message}
        onChange={handleOnChange}
        onKeyDown={handleKeyDown}
        data-slot="textarea"
        style={{
          height: CHAT_INPUT_HEIGHT,
        }}
        placeholder={t("chatInputPlaceholder")}
        className="placeholder:text-muted-foreground m-0 w-full max-h-[48px] resize-none border-0 bg-transparent focus:outline-none focus-visible:outline-none 
        [&::-webkit-scrollbar]:w-1
        [&::-webkit-scrollbar-track]:rounded-full
        [&::-webkit-scrollbar-track]:bg-gray-100
        [&::-webkit-scrollbar-thumb]:rounded-full
        [&::-webkit-scrollbar-thumb]:bg-gray-300
        dark:[&::-webkit-scrollbar-track]:bg-neutral-700
        dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"
      />
      <div className="flex justify-end">
        <Button
          variant="default"
          size="icon"
          className="size-8"
          onClick={handleOnSendBtnClick}
        >
          <Send />
        </Button>
      </div>
    </div>
  );
};

export default ChatInput;
