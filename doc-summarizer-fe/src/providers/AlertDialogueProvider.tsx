"use client";
import AlertDialogComponent from "@/components/alert-dialogue";
import { Dispatch, SetStateAction, createContext, useState } from "react";

export interface IDialogue {
  isOpen: boolean;
  type?: "error" | "warning" | "information" | null;
  title?: string | null;
  content: string | null;
  primaryCtaHandler?: Function | null;
  secondaryCtaHandler?: Function | null;
  primaryCtaLabel?: string;
  secondaryCtaLabel?: string;
  showPrimaryCta?: boolean;
  showSecondaryCta?: boolean;
}

interface IDialogueContextValue {
  dialogue: IDialogue;
  setDialogue: Dispatch<SetStateAction<IDialogue>> | null;
  resetDialogue: Function | null;
}

const defaultValue: IDialogueContextValue = {
  dialogue: {
    isOpen: false,
    type: null,
    title: null,
    content: null,
    primaryCtaHandler: null,
    secondaryCtaHandler: null,
  },
  setDialogue: null,
  resetDialogue: null,
};

export const AlertDialogueContext =
  createContext<IDialogueContextValue>(defaultValue);

const AlertDialogueProvider = ({ children }: { children: React.ReactNode }) => {
  const [dialogue, setDialogue] = useState<IDialogue>(defaultValue.dialogue);

  const resetDialogue = () => {
    setDialogue(defaultValue.dialogue);
  };

  return (
    <AlertDialogueContext.Provider
      value={{
        dialogue,
        setDialogue,
        resetDialogue,
      }}
    >
      {children}
      <AlertDialogComponent />
    </AlertDialogueContext.Provider>
  );
};

export default AlertDialogueProvider;
