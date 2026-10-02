"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getSupabaseClient } from "@/lib/supabase/client";

export default function ConfirmPage() {
  const [message, setMessage] = useState("Confirming your email…");
  const [confirmed, setConfirmed] = useState(false);

  useEffect(() => {
    let active = true;

    async function confirm() {
      const supabase = getSupabaseClient();
      if (!supabase) {
        setMessage("Supabase project settings are missing.");
        return;
      }

      const url = new URL(window.location.href);
      const tokenHash = url.searchParams.get("token_hash");
      const type = url.searchParams.get("type");
      const code = url.searchParams.get("code");
      if (!((tokenHash && type === "email") || code)) {
        setMessage("This confirmation link is invalid or incomplete.");
        return;
      }

      try {
        const { error } =
          tokenHash && type === "email"
            ? await supabase.auth.verifyOtp({
                token_hash: tokenHash,
                type: "email",
              })
            : await supabase.auth.exchangeCodeForSession(code);
        if (error) throw error;
        if (active) {
          window.history.replaceState(null, "", "/auth/confirm");
          setConfirmed(true);
          setMessage("Email confirmed. Your account is ready.");
        }
      } catch {
        if (active)
          setMessage(
            "Confirmation failed or the link expired. Please sign in or request a new link.",
          );
      }
    }

    void confirm();
    return () => {
      active = false;
    };
  }, []);

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center gap-4 px-6">
      <h1 className="text-2xl font-semibold">Confirm your account</h1>
      <p role="status">{message}</p>
      <Link className="underline" href={confirmed ? "/dashboard" : "/login"}>
        {confirmed ? "Continue to dashboard" : "Go to sign in"}
      </Link>
    </main>
  );
}
