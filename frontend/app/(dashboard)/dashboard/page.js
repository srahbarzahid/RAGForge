"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { getSupabaseClient } from "@/lib/supabase/client";
import { getCurrentUser } from "@/services/auth";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("Checking your session…");
  const configured = Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  );

  useEffect(() => {
    const supabase = getSupabaseClient();
    if (!supabase) return;
    let active = true;
    let request = 0;

    async function verify(session) {
      const current = ++request;
      if (!session) {
        if (active) router.replace("/login");
        return;
      }
      try {
        const identity = await getCurrentUser(session.access_token);
        if (active && current === request) {
          setUser(identity);
          setMessage("");
        }
      } catch {
        if (active && current === request) {
          setUser(null);
          setMessage("Your session could not be verified by the API.");
        }
      }
    }

    supabase.auth.getSession().then(({ data }) => verify(data.session));
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setTimeout(() => {
        void verify(session);
      }, 0);
    });
    return () => {
      active = false;
      subscription.unsubscribe();
    };
  }, [router]);

  async function signOut() {
    const supabase = getSupabaseClient();
    if (!supabase) return;
    await supabase.auth.signOut({ scope: "local" });
    router.replace("/login");
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl items-center px-6 py-12">
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-xl">RAGForge dashboard</CardTitle>
          <CardDescription>Authentication foundation</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-5">
          {!configured && (
            <p role="alert">Supabase project settings are missing.</p>
          )}
          {configured && message && <p role="status">{message}</p>}
          {user && (
            <>
              <p>Signed in as {user.email || user.user_id}</p>
              <p className="text-sm text-muted-foreground">
                Knowledge bases and documents arrive in later modules.
              </p>
              <Button
                className="self-start"
                variant="outline"
                onClick={signOut}
              >
                Sign out
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
