import "@/styles/globals.css";
import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme-provider";
import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";
import { MainContent } from "@/components/layout/main-content";

export const metadata: Metadata = {
  title: "Mimicus Admin UI",
  description: "Admin interface for managing Mimicus mock services",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="flex min-h-screen w-full bg-background text-foreground">
            <Sidebar />
            <div className="flex flex-1 flex-col">
              <Header />
              <MainContent>{children}</MainContent>
            </div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}