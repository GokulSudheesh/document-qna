import { deleteFile, uploadFile } from "@/apiHelpers/fileUpload";
import {
  ExtractedFile,
  FileUploadResponse,
  GetFileResponse,
  GetFilesResponse,
} from "@/client/types.gen";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { toast } from "sonner";

export interface IUseFileUpload {
  files: File[];
  isPending: boolean;
  handleFileChange: (files: File[]) => void;
  handleUpload: (args: {
    sessionId?: string | null;
    onSuccessCallback?: (data: FileUploadResponse) => void;
  }) => void;
  handleFileDeleteCallback: (args: {
    sessionId: string;
    fileId: string;
  }) => void;
  onModalCloseCallback: () => void;
}

export const useFileUpload = (): IUseFileUpload => {
  const queryClient = useQueryClient();
  const t = useTranslations();
  const [files, setFiles] = useState<File[]>([]);

  const { mutate: uploadFileMutate, isPending } = useMutation({
    mutationFn: uploadFile,
  });

  const handleFileChange = useCallback((files: File[]) => {
    setFiles(files);
  }, []);

  const updateQueryFileList = useCallback(
    ({
      sessionId,
      uploadedFiles,
    }: {
      sessionId: string;
      uploadedFiles: FileUploadResponse;
    }) => {
      queryClient.setQueryData(
        ["chat-files", sessionId],
        (oldData: { data: GetFilesResponse; error: undefined }) => {
          const timeStamp = new Date().toISOString();
          const newFiles: GetFileResponse[] =
            uploadedFiles?.data?.files?.map((file: ExtractedFile) => ({
              id: file.id,
              file_name: file.file_name,
              file_size: file.file_size,
              file_type: file.file_type,
              created: timeStamp,
              updated: timeStamp,
              session_id: sessionId,
            })) || [];
          return {
            ...oldData,
            data: {
              success: true,
              data: [...(oldData?.data?.data || []), ...newFiles],
            },
          };
        }
      );
    },
    []
  );

  const handleUpload: IUseFileUpload["handleUpload"] = useCallback(
    async ({ sessionId, onSuccessCallback }) => {
      uploadFileMutate(
        { sessionId, files },
        {
          onSuccess: (data) => {
            if (!data?.data) return;
            const sessionId = data?.data?.session_id;
            toast.success(t("uploadFileSuccessMessage"));
            setFiles([]);
            onSuccessCallback?.(data);
            if (sessionId) {
              updateQueryFileList({
                sessionId,
                uploadedFiles: data,
              });
              queryClient.invalidateQueries({
                queryKey: ["chat-files", sessionId],
              });
            }
          },
          onError: () => {
            toast.error(t("uploadFileErrorMessage"));
          },
        }
      );
    },
    [files, t, uploadFileMutate, updateQueryFileList]
  );

  const onModalCloseCallback = useCallback(() => {
    setFiles([]);
  }, []);

  const { mutate: deleteFileMutate } = useMutation({
    mutationFn: deleteFile,
    onError: () => {
      toast.error(t("deleteFileErrorMessage"));
    },
  });

  const handleFileDeleteCallback = useCallback(
    ({ sessionId, fileId }: { sessionId: string; fileId: string }) => {
      queryClient.setQueryData(
        ["chat-files", sessionId],
        (oldData: { data: GetFilesResponse; error: undefined }) => {
          return {
            ...oldData,
            data: {
              success: true,
              data: oldData.data?.data.filter((f) => f.id !== fileId),
            },
          };
        }
      );
      deleteFileMutate(fileId, {
        onSettled: () => {
          queryClient.invalidateQueries({
            queryKey: ["chat-files"],
          });
        },
      });
    },
    [queryClient]
  );

  return {
    files,
    isPending,
    handleFileChange,
    handleUpload,
    onModalCloseCallback,
    handleFileDeleteCallback,
  };
};
