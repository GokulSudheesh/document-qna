import {
  deleteFileApiV1FileFileIdDelete,
  fileUploadApiV1FileUploadPost,
} from "@/client";

export const uploadFile = async ({
  sessionId,
  files,
}: {
  sessionId?: string | null;
  files: File[];
}) => {
  const { data, response } = await fileUploadApiV1FileUploadPost({
    query: { session_id: sessionId },
    body: { files },
  });

  if (!response.ok || !data?.success) {
    throw new Error(`Error uploading files: ${response.status}`);
  }

  return data;
};

export const deleteFile = async (fileId: string) => {
  const { data, response } = await deleteFileApiV1FileFileIdDelete({
    path: { file_id: fileId },
  });

  if (!(response.ok && data?.success))
    throw new Error(`Error deleting file: ${response.status}`);

  return data;
};
