import React from "react";
import { Reference } from "@/client";
import PdfIIcon from "@/assets/icons/pdf-icn.svg";
import WordDocIcon from "@/assets/icons/worddoc-icn.svg";
import TextFileIcon from "@/assets/icons/textfile-icn.svg";
import { motion, Variants } from "motion/react";
import Image from "next/image";

const fileItemVariant: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.3 } },
};

const IconMap: Record<string, any> = {
  pdf: PdfIIcon,
  docx: WordDocIcon,
  txt: TextFileIcon,
};

type Props = {} & Reference;

const FileItem = ({ file_name }: Props) => {
  const fileType = file_name.split(".")?.[1] || "txt";
  return (
    <motion.div
      variants={fileItemVariant}
      className="flex gap-2 items-center border border-fileitem-border text-fileitem-foreground p-2 rounded-md"
    >
      <Image src={IconMap[fileType]} width={32} alt={fileType} />
      <span className="text-sm">{file_name}</span>
    </motion.div>
  );
};

export default FileItem;
