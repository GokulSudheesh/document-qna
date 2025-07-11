import React from "react";
import UploadModal from "./upload-modal";
import { useTranslations } from "next-intl";
import { CommonProps } from "./props";

const UpdateSession = (props: CommonProps) => {
  const t = useTranslations();
  return (
    <UploadModal
      title={t("updateSession.title")}
      subTitle={t("updateSession.subtitle")}
      {...props}
    />
  );
};

export default UpdateSession;
