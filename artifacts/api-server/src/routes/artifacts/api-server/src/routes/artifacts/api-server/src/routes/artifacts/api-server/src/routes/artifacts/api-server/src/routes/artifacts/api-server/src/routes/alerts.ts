import { Router, type IRouter } from "express";
import { db } from "@workspace/db";
import { alertsTable, devicesTable } from "@workspace/db";
import { eq, and } from "drizzle-orm";

const router: IRouter = Router();

async function formatAlert(alert: typeof alertsTable.$inferSelect) {
  const [device] = await db.select({ model: devicesTable.model }).from(devicesTable).where(eq(devicesTable.id, alert.deviceId)).limit(1);
  return {
    id: alert.id,
    deviceId: alert.deviceId,
    deviceModel: device?.model ?? "Unknown",
    type: alert.type,
    severity: alert.severity,
    message: alert.message,
    status: alert.status,
    createdAt: alert.createdAt.toISOString(),
    acknowledgedAt: alert.acknowledgedAt?.toISOString() ?? null,
  };
}

router.get("/", async (req, res) => {
  try {
    const { deviceId, status } = req.query;
    const conditions = [];
    if (deviceId) conditions.push(eq(alertsTable.deviceId, parseInt(deviceId as string)));
    if (status) conditions.push(eq(alertsTable.status, status as string));

    const alerts = conditions.length > 0
      ? await db.select().from(alertsTable).where(and(...conditions)).orderBy(alertsTable.createdAt)
      : await db.select().from(alertsTable).orderBy(alertsTable.createdAt);

    const result = await Promise.all(alerts.map(formatAlert));
    res.json(result);
  } catch (err) {
    req.log.error({ err }, "List alerts error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.post("/:id/acknowledge", async (req, res) => {
  try {
    const [alert] = await db.update(alertsTable)
      .set({ status: "acknowledged", acknowledgedAt: new Date() })
      .where(eq(alertsTable.id, parseInt(req.params.id)))
      .returning();
    if (!alert) { res.status(404).json({ error: "not_found", message: "Alert not found" }); return; }
    res.json(await formatAlert(alert));
  } catch (err) {
    req.log.error({ err }, "Acknowledge alert error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

export default router;
