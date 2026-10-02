import Link from "next/link";

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-6 px-6 py-16">
      <h1 className="text-4xl font-semibold tracking-tight">RAGForge</h1>
      <p className="max-w-xl text-lg text-muted-foreground">
        The document intelligence portal is being built module by module. Sign
        in to build a private knowledge base, then ask questions grounded in
        your own documents.
      </p>
      <div className="flex gap-5 text-sm">
        <Link className="font-medium underline" href="/login">
          Sign in
        </Link>
        <Link className="font-medium underline" href="/register">
          Create account
        </Link>
      </div>
    </main>
  );
}
