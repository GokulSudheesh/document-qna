import React, { useCallback, useContext } from "react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { AlertDialogueContext } from "@/providers/AlertDialogueProvider";

const AlertDialogComponent = () => {
  const { dialogue, resetDialogue, setDialogue } =
    useContext(AlertDialogueContext);
  const {
    isOpen,
    type,
    primaryCtaHandler,
    secondaryCtaHandler,
    primaryCtaLabel,
    secondaryCtaLabel,
    showSecondaryCta = true,
    showPrimaryCta = true,
    title,
    content,
  } = dialogue;

  const handlePrimaryClick = useCallback(() => {
    primaryCtaHandler?.();
    resetDialogue?.();
  }, [primaryCtaHandler, resetDialogue]);

  const handleSecondaryClick = useCallback(() => {
    secondaryCtaHandler?.();
    resetDialogue?.();
  }, [secondaryCtaHandler, resetDialogue]);

  const handleClose = useCallback(() => {
    resetDialogue?.();
  }, [resetDialogue]);

  const handleOpenChange = useCallback(
    (isOpen: boolean) => {
      if (!isOpen) handleClose();
      else setDialogue?.({ ...dialogue, isOpen });
    },
    [handleClose, setDialogue, dialogue]
  );

  return (
    <AlertDialog open={isOpen} onOpenChange={handleOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          {title && <AlertDialogTitle>{title}</AlertDialogTitle>}
          <AlertDialogDescription>{content}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          {showSecondaryCta && secondaryCtaLabel && (
            <AlertDialogCancel onClick={handleSecondaryClick}>
              {secondaryCtaLabel}
            </AlertDialogCancel>
          )}
          {showPrimaryCta && primaryCtaLabel && (
            <AlertDialogAction onClick={handlePrimaryClick}>
              {primaryCtaLabel}
            </AlertDialogAction>
          )}
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};

export default AlertDialogComponent;
