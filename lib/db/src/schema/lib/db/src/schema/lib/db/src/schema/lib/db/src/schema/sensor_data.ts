import { pgTable, serial, integer, real, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export const sensorDataTable = pgTable("sensor_data", {
  id: serial("id").primaryKey(),
  deviceId: integer("device_id").notNull(),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
  vibration: real("vibration").notNull(),
  temperature: real("temperature").notNull(),
  ultrasound: real("ultrasound").notNull(),
  magneticFlux: real("magnetic_flux").notNull(),
  velocity: real("velocity").notNull(),
});

export const insertSensorDataSchema = createInsertSchema(sensorDataTable).omit({ id: true });
export type InsertSensorData = z.infer<typeof insertSensorDataSchema>;
export type SensorData = typeof sensorDataTable.$inferSelect;
