import { pgTable, serial, text, timestamp, integer, real } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export const devicesTable = pgTable("devices", {
  id: serial("id").primaryKey(),
  model: text("model").notNull(),
  serialNumber: text("serial_number").notNull().unique(),
  type: text("type").notNull(),
  siteId: integer("site_id"),
  status: text("status").notNull().default("online"),
  installDate: text("install_date"),
  lastSeen: timestamp("last_seen"),
  firmwareVersion: text("firmware_version"),
  description: text("description"),
  healthScore: real("health_score"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertDeviceSchema = createInsertSchema(devicesTable).omit({ id: true, createdAt: true });
export type InsertDevice = z.infer<typeof insertDeviceSchema>;
export type Device = typeof devicesTable.$inferSelect;
