import "./globals.css";

export const metadata = {
  title: "RAGForge",
  description: "Private document intelligence portal",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
