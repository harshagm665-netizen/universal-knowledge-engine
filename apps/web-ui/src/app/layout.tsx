import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Savage Sentinel v1.0',
  description: 'AI Education Companion for Novatech Robo',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-[#050a0f]">{children}</body>
    </html>
  );
}