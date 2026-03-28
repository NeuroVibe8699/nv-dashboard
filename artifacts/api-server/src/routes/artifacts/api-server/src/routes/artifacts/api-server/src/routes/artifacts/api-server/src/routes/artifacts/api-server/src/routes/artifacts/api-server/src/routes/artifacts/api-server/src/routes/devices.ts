import { Router, type IRouter } from "express";
import { db } from "@workspace/db";
import { devicesTable, sitesTable, sensorDataTable, alertsTable } from "@workspace/db";
import { eq, and, desc } from "drizzle-orm";

const router: IRouter = Router();

async function formatDevice(device: typeof devicesTable.$inferSelect) {
  let siteName: string | null = null;
  if (device.siteId) {
    const [site] = await db.select({ name: sitesTable.name }).from(sitesTable).where(eq(sitesTable.id, device.siteId)).limit(1);
    siteName = site?.name ?? null;
  }
  return {
    id: device.id, model: device.model, serialNumber: device.serialNumber,
    type: device.type, siteId: device.siteId, siteName, status: device.status,
    installDate: device.installDate, lastSeen: device.lastSeen?.toISOString() ?? null,
    firmwareVersion: device.firmwareVersion, description: device.description,
    healthScore: device.healthScore, createdAt: device.createdAt.toISOString(),
  };
}

function generateSensorReading(deviceId: number, hoursAgo: number) {
  const base = deviceId * 1000 + hoursAgo;
  const noise = () => (Math.sin(base * 0.3) * 0.5 + Math.random() * 0.5 - 0.25);
  return {
    vibration: Math.max(0.1, 2.5 + noise() * 2),
    temperature: Math.max(20, 55 + noise() * 15),
    ultrasound: Math.max(10, 38 + noise() * 12),
    magneticFlux: Math.max(1, 22 + noise() * 8),
    velocity: Math.max(0.1, 15 + noise() * 6),
  };
}

router.get("/", async (req, res) => {
  try {
    const { type, siteId } = req.query;
    const conditions = [];
    if (type) conditions.push(eq(devicesTable.type, type as string));
    if (siteId) conditions.push(eq(devicesTable.siteId, parseInt(siteId as string)));
    const devices = conditions.length > 0
      ? await db.select().from(devicesTable).where(and(...conditions)).orderBy(devicesTable.model)
      : await db.select().from(devicesTable).orderBy(devicesTable.model);
    res.json(await Promise.all(devices.map(formatDevice)));
  } catch (err) {
    req.log.error({ err }); res.status(500).json({ error: "server_error" });
  }
});

router.post("/import", async (req, res) => {
  try {
    const { devices } = req.body;
    if (!Array.isArray(devices)) { res.status(400).json({ error: "bad_request", message: "devices must be an array" }); return; }
    let imported = 0; const errors: string[] = [];
    for (const d of devices) {
      try {
        await db.insert(devicesTable).values({ model: d.model, serialNumber: d.serialNumber, type: d.type, siteId: d.siteId, status: d.status || "online", installDate: d.installDate, firmwareVersion: d.firmwareVersion, description: d.description, healthScore: 85 });
        imported++;
      } catch (e: any) { errors.push(`Failed to import ${d.serialNumber}: ${e.message}`); }
    }
    res.json({ imported, failed: errors.length, errors });
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.get("/export", async (req, res) => {
  try {
    const devices = await db.select().from(devicesTable).orderBy(devicesTable.model);
    res.json(await Promise.all(devices.map(formatDevice)));
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.post("/", async (req, res) => {
  try {
    const { model, serialNumber, type, siteId, status, installDate, firmwareVersion, description } = req.body;
    if (!model || !serialNumber || !type || !status) { res.status(400).json({ error: "bad_request", message: "Missing required fields" }); return; }
    const [device] = await db.insert(devicesTable).values({ model, serialNumber, type, siteId, status, installDate, firmwareVersion, description, healthScore: 90, lastSeen: new Date() }).returning();
    res.status(201).json(await formatDevice(device));
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.get("/:id", async (req, res) => {
  try {
    const [device] = await db.select().from(devicesTable).where(eq(devicesTable.id, parseInt(req.params.id))).limit(1);
    if (!device) { res.status(404).json({ error: "not_found", message: "Device not found" }); return; }
    res.json(await formatDevice(device));
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.put("/:id", async (req, res) => {
  try {
    const { model, serialNumber, siteId, status, installDate, firmwareVersion, description } = req.body;
    const updates: Partial<typeof devicesTable.$inferInsert> = {};
    if (model !== undefined) updates.model = model;
    if (serialNumber !== undefined) updates.serialNumber = serialNumber;
    if (siteId !== undefined) updates.siteId = siteId;
    if (status !== undefined) updates.status = status;
    if (installDate !== undefined) updates.installDate = installDate;
    if (firmwareVersion !== undefined) updates.firmwareVersion = firmwareVersion;
    if (description !== undefined) updates.description = description;
    const [device] = await db.update(devicesTable).set(updates).where(eq(devicesTable.id, parseInt(req.params.id))).returning();
    if (!device) { res.status(404).json({ error: "not_found", message: "Device not found" }); return; }
    res.json(await formatDevice(device));
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.delete("/:id", async (req, res) => {
  try {
    await db.delete(devicesTable).where(eq(devicesTable.id, parseInt(req.params.id)));
    res.json({ success: true, message: "Device deleted" });
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.get("/:id/sensor-data", async (req, res) => {
  try {
    const deviceId = parseInt(req.params.id);
    const limit = parseInt(req.query.limit as string) || 100;
    const realData = await db.select().from(sensorDataTable).where(eq(sensorDataTable.deviceId, deviceId)).orderBy(desc(sensorDataTable.timestamp)).limit(limit);
    if (realData.length > 0) {
      res.json(realData.map(d => ({ id: d.id, deviceId: d.deviceId, timestamp: d.timestamp.toISOString(), vibration: d.vibration, temperature: d.temperature, ultrasound: d.ultrasound, magneticFlux: d.magneticFlux, velocity: d.velocity })));
      return;
    }
    const data = [];
    const now = new Date();
    for (let i = limit - 1; i >= 0; i--) {
      const ts = new Date(now.getTime() - i * (24 * 60 * 60 * 1000 / limit));
      data.push({ id: i + 1, deviceId, timestamp: ts.toISOString(), ...generateSensorReading(deviceId, i) });
    }
    res.json(data);
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.get("/:id/spectrum", async (req, res) => {
  try {
    const deviceId = parseInt(req.params.id);
    const frequencies: number[] = [], amplitudes: number[] = [];
    for (let f = 10; f <= 1000; f += 10) {
      frequencies.push(f);
      amplitudes.push(parseFloat(Math.max(0, 5 * Math.sin(f * 0.01 * deviceId) * Math.exp(-f * 0.001) + Math.random() * 2).toFixed(3)));
    }
    const peakIdx = amplitudes.indexOf(Math.max(...amplitudes));
    res.json({ deviceId, frequencies, amplitudes, dominantFrequency: frequencies[peakIdx], peakAmplitude: amplitudes[peakIdx], rmsVelocity: parseFloat((2.5 + Math.random() * 2).toFixed(3)), overallLevel: parseFloat((35 + Math.random() * 15).toFixed(2)), timestamp: new Date().toISOString() });
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

router.get("/:id/prediction", async (req, res) => {
  try {
    const deviceId = parseInt(req.params.id);
    const [device] = await db.select().from(devicesTable).where(eq(devicesTable.id, deviceId)).limit(1);
    const healthScore = device?.healthScore ?? (70 + Math.random() * 25);
    const failureProbability = parseFloat(((100 - healthScore) / 100 * 0.8).toFixed(3));
    const anomalies = [];
    if (healthScore < 80) anomalies.push({ type: "vibration", severity: healthScore < 60 ? "critical" : "high", description: "Abnormal vibration detected above threshold", value: 8.2, threshold: 7.1 });
    if (healthScore < 75) anomalies.push({ type: "temperature", severity: "medium", description: "Elevated temperature trending upward", value: 78.5, threshold: 85 });
    if (healthScore < 85) anomalies.push({ type: "ultrasound", severity: "low", description: "Minor ultrasound signature change", value: 42.3, threshold: 60 });
    let recommendedAction = "none";
    if (failureProbability > 0.6) recommendedAction = "immediate_action";
    else if (failureProbability > 0.35) recommendedAction = "schedule_maintenance";
    else if (failureProbability > 0.15) recommendedAction = "monitor";
    let predictedFailureDate: string | null = null;
    if (failureProbability > 0.15) {
      const failDate = new Date();
      failDate.setDate(failDate.getDate() + Math.round((1 - failureProbability) * 90));
      predictedFailureDate = failDate.toISOString();
    }
    res.json({ deviceId, healthScore: parseFloat(healthScore.toFixed(1)), failureProbability, predictedFailureDate, recommendedAction, anomalies, confidence: parseFloat((0.75 + Math.random() * 0.2).toFixed(3)), generatedAt: new Date().toISOString() });
  } catch (err) { req.log.error({ err }); res.status(500).json({ error: "server_error" }); }
});

export default router;
