"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { getSupabaseClient } from "@/lib/supabase/client";

export function AuthForm({ mode }) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [pending, setPending] = useState(false);
  const isRegister = mode === "register";
  const configured = Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  );

  async function handleSubmit(event) {
    event.preventDefault();
    setErrorMessage("");
    const supabase = getSupabaseClient();
    if (!supabase) {
      setErrorMessage("Supabase project settings are missing.");
      return;
    }
    setPending(true);
    try {
      const result = isRegister
        ? await supabase.auth.signUp({ email, password })
        : await supabase.auth.signInWithPassword({ email, password });
      if (result.error) throw result.error;
      if (result.data.session) {
        router.replace("/dashboard");
        router.refresh();
      } else if (isRegister) {
        setErrorMessage(
          "Account created, but a session is not available yet. Please sign in when your account is ready.",
        );
      } else {
        setErrorMessage("Sign in did not create a session. Please try again.");
      }
    } catch (error) {
      setErrorMessage(
        error.message || "Authentication failed. Please try again.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-12">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-xl">
            {isRegister ? "Create your account" : "Sign in to RAGForge"}
          </CardTitle>
          <CardDescription>
            {isRegister
              ? "Create a private workspace for your documents."
              : "Continue to your document workspace."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Password</FieldLabel>
                <Input
                  id="password"
                  type="password"
                  autoComplete={
                    isRegister ? "new-password" : "current-password"
                  }
                  minLength={6}
                  required
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                />
              </Field>
            </FieldGroup>
            {errorMessage && (
              <p role="alert" className="text-sm text-destructive">
                {errorMessage}
              </p>
            )}
            <Button type="submit" disabled={pending || !configured}>
              {pending
                ? "Please wait…"
                : isRegister
                  ? "Create account"
                  : "Sign in"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="text-sm text-muted-foreground">
          {isRegister ? (
            <p>
              Already registered?{" "}
              <Link className="text-foreground underline" href="/login">
                Sign in
              </Link>
            </p>
          ) : (
            <p>
              New to RAGForge?{" "}
              <Link className="text-foreground underline" href="/register">
                Create an account
              </Link>
            </p>
          )}
        </CardFooter>
      </Card>
    </main>
  );
}
