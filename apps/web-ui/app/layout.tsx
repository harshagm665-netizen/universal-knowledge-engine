import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SAVAGE V-RAG",
  description: "Edge Precision Intelligence",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-black">{children}</body>
    </html>
  );
}