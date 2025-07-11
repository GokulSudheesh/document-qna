import { uploadFile } from "@/apiHelpers/fileUpload";
import { useMutation } from "@tanstack/react-query";
import { useCallback, useState } from "react";

export interface IUseFileUpload {
  files: File[];
  isPending: boolean;
  handleFileChange: (files: File[]) => void;
  handleUpload: () => void;
}

export const useFileUpload = () => {
  const [files, setFiles] = useState<File[]>([]);
  const { mutate, isPending } = useMutation({
    mutationFn: uploadFile,
  });

  const handleFileChange = useCallback((files: File[]) => {
    setFiles(files);
  }, []);

  const handleUpload = useCallback(async () => {}, [files, mutate]);

  return {
    files,
    isPending,
    handleFileChange,
    handleUpload,
  };
};
