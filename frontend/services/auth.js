export async function getCurrentUser(accessToken) {
  const baseUrl =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
  const response = await fetch(`${baseUrl}/auth/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
    cache: "no-store",
  });
  if (!response.ok) throw new Error("The API could not verify your session.");
  return response.json();
}
