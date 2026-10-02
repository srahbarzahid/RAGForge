import { config } from "dotenv";

config({ path: ".env.local" });

const { prisma } = await import("../lib/prisma.js");

try {
  const rows = await prisma.$queryRaw`SELECT 1 AS connection_ok`;
  if (rows[0]?.connection_ok !== 1) {
    throw new Error("Prisma database check returned an unexpected result");
  }
  console.log("Prisma PostgreSQL connection OK");
} finally {
  await prisma.$disconnect();
}
