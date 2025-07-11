import { FileUploadResponse, GetFileResponse } from "@/client/types.gen";

export type CommonProps = {
  isOpen: boolean;
  sessionId?: string | null;
  uploadedFiles?: GetFileResponse[];
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  onFileUploadSuccessCallback?: (data: FileUploadResponse) => void;
};

export type FileUploadProps = CommonProps & {
  title: string;
  subTitle: string;
  onClose?: () => void;
};
