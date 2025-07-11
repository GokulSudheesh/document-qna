import React from "react";
import { Reference } from "@/client";
import { motion, Variants } from "motion/react";
import FileIcon from "@/components/file-icon";

const fileItemVariant: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.3 } },
};

const FileItem = ({ file_name }: Reference) => {
  return (
    <motion.div
      variants={fileItemVariant}
      className="flex gap-2 items-center border border-fileitem-border text-fileitem-foreground p-2 rounded-md"
    >
      <FileIcon className="flex w-6 md:w-8 h-auto" fileName={file_name} />
      <span className="text-sm">{file_name}</span>
    </motion.div>
  );
};

export default FileItem;
