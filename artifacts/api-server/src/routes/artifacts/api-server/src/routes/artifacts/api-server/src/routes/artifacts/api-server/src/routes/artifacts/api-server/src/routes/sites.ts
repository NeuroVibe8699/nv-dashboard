import { Router, type IRouter } from "express";
import { db } from "@workspace/db";
import { sitesTable, devicesTable } from "@workspace/db";
import { eq, count } from "drizzle-orm";

const router: IRouter = Router();

async function formatSite(site: typeof sitesTable.$inferSelect) {
  const [{ value }] = await db.select({ value: count() }).from(devicesTable).where(eq(devicesTable.siteId, site.id));
  return {
    id: site.id,
    name: site.name,
    location: site.location,
    description: site.description,
    status: site.status,
    deviceCount: Number(value),
    createdAt: site.createdAt.toISOString(),
  };
}

router.get("/", async (req, res) => {
  try {
    const sites = await db.select().from(sitesTable).orderBy(sitesTable.createdAt);
    const result = await Promise.all(sites.map(formatSite));
    res.json(result);
  } catch (err) {
    req.log.error({ err }, "List sites error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.post("/", async (req, res) => {
  try {
    const { name, location, description, status } = req.body;
    if (!name || !location || !status) {
      res.status(400).json({ error: "bad_request", message: "Missing required fields" });
      return;
    }
    const [site] = await db.insert(sitesTable).values({ name, location, description, status }).returning();
    res.status(201).json(await formatSite(site));
  } catch (err) {
    req.log.error({ err }, "Create site error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const [site] = await db.select().from(sitesTable).where(eq(sitesTable.id, parseInt(req.params.id))).limit(1);
    if (!site) { res.status(404).json({ error: "not_found", message: "Site not found" }); return; }
    res.json(await formatSite(site));
  } catch (err) {
    req.log.error({ err }, "Get site error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.put("/:id", async (req, res) => {
  try {
    const { name, location, description, status } = req.body;
    const updates: Partial<typeof sitesTable.$inferInsert> = {};
    if (name !== undefined) updates.name = name;
    if (location !== undefined) updates.location = location;
    if (description !== undefined) updates.description = description;
    if (status !== undefined) updates.status = status;

    const [site] = await db.update(sitesTable).set(updates).where(eq(sitesTable.id, parseInt(req.params.id))).returning();
    if (!site) { res.status(404).json({ error: "not_found", message: "Site not found" }); return; }
    res.json(await formatSite(site));
  } catch (err) {
    req.log.error({ err }, "Update site error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.delete("/:id", async (req, res) => {
  try {
    await db.delete(sitesTable).where(eq(sitesTable.id, parseInt(req.params.id)));
    res.json({ success: true, message: "Site deleted" });
  } catch (err) {
    req.log.error({ err }, "Delete site error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

export default router;
