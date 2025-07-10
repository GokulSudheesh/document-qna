import React from "react";
import { cn } from "@/lib/utils";
import styles from "./style.module.css";

const Cursor = () => {
  return <span className={cn(styles.cursor, styles["cursor-blink"])} />;
};

export default Cursor;
