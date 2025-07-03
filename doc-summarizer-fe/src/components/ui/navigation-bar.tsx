"use client";
import React from "react";
import ThemeSwitcher from "./theme-switcher";
import { SidebarTrigger } from "./sidebar";

export function NavigationBar() {
  return (
    <nav className="border-b border-sidebar-border bg-sidebar text-sidebar-foreground p-4 flex items-center justify-between w-full">
      <SidebarTrigger className="w-9 h-9" />
      <div className="flex ms-auto">
        <ThemeSwitcher />
      </div>
    </nav>
  );
}
