"use client";
import React from "react";
import ThemeSwitcher from "./theme-switcher";

export function NavigationBar() {
  return (
    <nav className="bg-background p-4 flex items-center justify-between w-full">
      <div className="flex ms-auto">
        <ThemeSwitcher />
      </div>
    </nav>
  );
}
