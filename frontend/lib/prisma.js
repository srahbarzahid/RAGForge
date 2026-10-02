import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";

if (typeof window !== "undefined") {
  throw new Error("Prisma is server-only");
}

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error("DATABASE_URL is not configured for Prisma");
}

const connectionUrl = new URL(databaseUrl);
if (
  connectionUrl.protocol !== "postgresql:" &&
  connectionUrl.protocol !== "postgres:"
) {
  throw new Error("DATABASE_URL must be a PostgreSQL URL");
}

const globalForPrisma = globalThis;
const sslRootCert = process.env.DATABASE_SSL_ROOT_CERT;
connectionUrl.searchParams.set(
  "sslmode",
  sslRootCert ? "verify-full" : "require",
);
if (sslRootCert) connectionUrl.searchParams.set("sslrootcert", sslRootCert);
connectionUrl.searchParams.set("uselibpqcompat", "true");

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    adapter: new PrismaPg({ connectionString: connectionUrl.toString() }),
  });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
