import React, { useCallback } from "react";
import { Upload } from "lucide-react";
import { Accept } from "react-dropzone";
import { useTranslations } from "next-intl";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { FileUploader } from "@/components/file-uploader";
import { FileUploadProps } from "./props";
import { useFileUpload } from "./hooks";

const ACCEPTED_FILE_TYPES: Accept = {
  "application/pdf": [".pdf"],
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
    ".docx",
  ],
  "application/msword": [".doc"],
  "text/plain": [".txt"],
};
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const MAX_FILE_COUNT = 10;

const UploadModal = ({
  sessionId,
  isOpen,
  title,
  subTitle,
  uploadedFiles,
  setIsOpen,
  onFileUploadSuccessCallback,
  onClose,
}: FileUploadProps) => {
  const t = useTranslations();
  const {
    files,
    isPending,
    handleFileChange,
    onModalCloseCallback,
    handleFileDeleteCallback,
    handleUpload,
  } = useFileUpload();

  const handleUploadCallback = useCallback(() => {
    handleUpload({ sessionId, onSuccessCallback: onFileUploadSuccessCallback });
  }, [sessionId, handleUpload, onFileUploadSuccessCallback]);

  const handleFileDelete = useCallback(
    (fileId: string) => {
      if (sessionId) handleFileDeleteCallback({ sessionId, fileId });
    },
    [sessionId, handleFileDeleteCallback]
  );

  const handleOpenChange = useCallback(
    (isOpen: boolean) => {
      if (!isOpen) {
        onModalCloseCallback();
        onClose?.();
      }
      setIsOpen(isOpen);
    },
    [onClose, onModalCloseCallback]
  );

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[425px] md:max-w-[60dvw]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{subTitle}</DialogDescription>
        </DialogHeader>
        <div className="grid gap-4">
          <div className="flex flex-col gap-4">
            <FileUploader
              value={files}
              maxSize={MAX_FILE_SIZE} // 5 MB
              maxFileCount={MAX_FILE_COUNT}
              accept={ACCEPTED_FILE_TYPES}
              disabled={isPending}
              uploadedFiles={uploadedFiles}
              onValueChange={handleFileChange}
              onRemoveUploadedFile={handleFileDelete}
              multiple
            />
          </div>
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">{t("cancel")}</Button>
          </DialogClose>
          <Button
            isLoading={isPending}
            disabled={!files.length || isPending}
            onClick={handleUploadCallback}
          >
            <Upload />
            {t("upload")}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default UploadModal;
