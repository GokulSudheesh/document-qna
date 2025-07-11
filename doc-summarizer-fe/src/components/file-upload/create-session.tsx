import React, { useCallback } from "react";
import UploadModal from "./upload-modal";
import { useTranslations } from "next-intl";
import { CommonProps } from "./props";
import { FileUploadResponse } from "@/client/types.gen";

const CreateSession = ({
  setIsOpen,
  onFileUploadSuccessCallback,
  ...props
}: CommonProps) => {
  const t = useTranslations();
  const onFileUploadSuccess = useCallback(
    (data: FileUploadResponse) => {
      // Close the modal after successful upload
      setIsOpen(false);
      onFileUploadSuccessCallback?.(data);
    },
    [onFileUploadSuccessCallback, setIsOpen]
  );
  return (
    <UploadModal
      title={t("createSession.title")}
      subTitle={t("createSession.subtitle")}
      setIsOpen={setIsOpen}
      onFileUploadSuccessCallback={onFileUploadSuccess}
      {...props}
    />
  );
};

export default CreateSession;
