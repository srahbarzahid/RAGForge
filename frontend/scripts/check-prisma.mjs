import { config } from "dotenv";

config({ path: ".env.local" });

const { prisma } = await import("../lib/prisma.js");

try {
  const rows = await prisma.$queryRaw`SELECT 1 AS connection_ok`;
  if (rows[0]?.connection_ok !== 1) {
    throw new Error("Prisma database check returned an unexpected result");
  }
  for (const model of [
    "profile",
    "knowledgeBase",
    "document",
    "conversation",
    "message",
    "feedback",
    "usageRecord",
    "auditLog",
  ]) {
    await prisma[model].findFirst();
  }
  console.log("Prisma PostgreSQL connection OK");
  console.log("All eight application tables readable through Prisma");
} finally {
  await prisma.$disconnect();
}
