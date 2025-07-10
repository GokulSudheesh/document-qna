import React from "react";
import ThemeProvider from "./ThemeProvider";
import QueryProvider from "./QueryProvider";
import { NextIntlClientProvider } from "next-intl";
import AlertDialogueProvider from "./AlertDialogueProvider";

const Providers = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <QueryProvider>
        <NextIntlClientProvider>
          <AlertDialogueProvider>{children}</AlertDialogueProvider>
        </NextIntlClientProvider>
      </QueryProvider>
    </ThemeProvider>
  );
};

export default Providers;
