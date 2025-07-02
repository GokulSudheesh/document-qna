export const uploadFile = async (files: File[]) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("file", file);
  });

  const response = await fetch("/api/file-upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Error uploading files: ${response.status}`);
  }

  return await response.json();
};
