"use client";
import React from "react";
import { Button } from "@/components/ui/button";
import { FileUploader } from "@/components/file-uploader";
import { useFileUpload } from "@/hooks/use-file-upload";
import { Upload } from "lucide-react";

const FileUpload = () => {
  const { files, isPending, handleFileChange, handleUpload } = useFileUpload();
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center h-full p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <FileUploader value={files} onValueChange={handleFileChange} />
        <Button
          className="ms-auto"
          isLoading={isPending}
          disabled={!files.length || isPending}
          onClick={handleUpload}
        >
          <Upload />
          Upload
        </Button>
      </main>
    </div>
  );
};

export default FileUpload;
