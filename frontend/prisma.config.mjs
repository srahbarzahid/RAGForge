import { config } from "dotenv";
import { defineConfig } from "prisma/config";

config({ path: ".env.local" });

export default defineConfig({
  schema: "prisma/schema.prisma",
  datasource: {
    // Client generation needs a valid URL shape but never connects to it.
    url:
      process.env.DATABASE_URL ??
      "postgresql://unused:unused@localhost:5432/unused",
  },
});
