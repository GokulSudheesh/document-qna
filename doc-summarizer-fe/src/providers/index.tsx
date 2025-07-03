import React from "react";
import ThemeProvider from "./ThemeProvider";
import QueryProvider from "./QueryProvider";
import { NextIntlClientProvider } from "next-intl";

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
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </QueryProvider>
    </ThemeProvider>
  );
};

export default Providers;
