import React from "react";
import Image from "next/image";
import PdfIIcon from "@/assets/icons/pdf-icn.svg";
import WordDocIcon from "@/assets/icons/worddoc-icn.svg";
import TextFileIcon from "@/assets/icons/textfile-icn.svg";
import { FileText } from "lucide-react";

const IconMap: Record<string, any> = {
  pdf: PdfIIcon,
  docx: WordDocIcon,
  txt: TextFileIcon,
};

type Props = {
  className?: string;
  fileName: string;
};

const FileIcon = ({ className, fileName }: Props) => {
  const fileType = fileName.split(".")?.[1];
  const img = IconMap[fileType];

  if (!fileType || !img)
    return (
      <div className={className}>
        <FileText
          className="w-full h-auto text-muted-foreground"
          aria-hidden="true"
        />
      </div>
    );
  return (
    <div className={className}>
      <Image
        src={img}
        width="0"
        height="0"
        sizes="100vw"
        className="w-full h-auto"
        alt={fileType}
        draggable={false}
      />
    </div>
  );
};

export default FileIcon;
