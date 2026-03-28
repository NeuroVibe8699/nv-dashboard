import { db } from "@workspace/db";
import { usersTable, devicesTable, alertsTable } from "@workspace/db";
import bcrypt from "bcryptjs";

async function seed() {
  console.log("Seeding users...");

  const adminHash = await bcrypt.hash("admin123", 10);
  const userHash = await bcrypt.hash("user123", 10);

  await db.insert(usersTable).values([
    { username: "admin", email: "admin@neurovibe.ai", passwordHash: adminHash, role: "admin", fullName: "System Administrator", siteId: null },
    { username: "operator1", email: "operator1@neurovibe.ai", passwordHash: userHash, role: "user", fullName: "Rajesh Kumar", siteId: 1 },
    { username: "operator2", email: "operator2@neurovibe.ai", passwordHash: userHash, role: "user", fullName: "Priya Sharma", siteId: 2 },
  ]).onConflictDoNothing();

  console.log("Seeding nodes (NVS-1001 to NVS-1010)...");

  const nodeModels = Array.from({ length: 10 }, (_, i) => `NVS-${1001 + i}`);
  const gatewayModels = Array.from({ length: 10 }, (_, i) => `NV-${1001 + i}`);
  const statuses = ["online", "online", "online", "online", "online", "warning", "warning", "offline", "critical", "online"];
  const healthScores = [96, 88, 92, 79, 85, 63, 58, null, 41, 94];
  const sites = [1, 1, 2, 2, 3, 3, 1, 2, 3, 4];
  const firmwares = ["v2.4.1", "v2.4.1", "v2.3.8", "v2.4.1", "v2.3.5", "v2.2.9", "v2.4.1", "v2.1.0", "v2.3.8", "v2.4.1"];

  const nodeValues = nodeModels.map((model, i) => ({
    model,
    serialNumber: `SN-NVS${String(i + 1).padStart(4, "0")}`,
    type: "node" as const,
    siteId: sites[i],
    status: statuses[i],
    installDate: `2024-0${(i % 9) + 1}-${String((i * 3 + 10) % 28 + 1).padStart(2, "0")}`,
    lastSeen: statuses[i] !== "offline" ? new Date() : new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    firmwareVersion: firmwares[i],
    healthScore: healthScores[i],
    description: `Vibration monitoring node at Site ${sites[i]}`,
  }));

  const gatewayValues = gatewayModels.map((model, i) => ({
    model,
    serialNumber: `SN-NVG${String(i + 1).padStart(4, "0")}`,
    type: "gateway" as const,
    siteId: sites[i],
    status: i < 8 ? "online" : "warning",
    installDate: `2023-${String((i % 11) + 1).padStart(2, "0")}-15`,
    lastSeen: new Date(),
    firmwareVersion: `v3.${i % 3}.${i % 5}`,
    healthScore: 80 + i,
    description: `Data aggregation gateway for ${model}`,
  }));

  await db.insert(devicesTable).values([...nodeValues, ...gatewayValues]).onConflictDoNothing();

  console.log("Seeding alerts...");
  await db.insert(alertsTable).values([
    { deviceId: 6, type: "vibration", severity: "warning", message: "NVS-1006: Vibration level 8.3 mm/s exceeds threshold 7.1 mm/s", status: "active" },
    { deviceId: 7, type: "temperature", severity: "warning", message: "NVS-1007: Temperature 87°C approaching critical limit", status: "active" },
    { deviceId: 9, type: "health", severity: "critical", message: "NVS-1009: Device health score critical (41%). Immediate maintenance required!", status: "active" },
    { deviceId: 9, type: "vibration", severity: "critical", message: "NVS-1009: Extreme vibration 12.5 mm/s detected - possible bearing failure", status: "active" },
    { deviceId: 8, type: "connectivity", severity: "info", message: "NVS-1008: Device offline for 3+ days. Check network connection.", status: "acknowledged" },
    { deviceId: 7, type: "magnetic_flux", severity: "warning", message: "NVS-1007: Magnetic flux anomaly detected. Motor inspection recommended.", status: "active" },
  ]).onConflictDoNothing();

  console.log("Seed complete!");
  process.exit(0);
}

seed().catch((err) => {
  console.error("Seed failed:", err);
  process.exit(1);
});
