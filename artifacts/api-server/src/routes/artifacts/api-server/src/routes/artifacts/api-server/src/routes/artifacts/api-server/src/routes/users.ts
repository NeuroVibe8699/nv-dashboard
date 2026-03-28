import { Router, type IRouter } from "express";
import { db } from "@workspace/db";
import { usersTable } from "@workspace/db";
import { eq } from "drizzle-orm";
import bcrypt from "bcryptjs";

const router: IRouter = Router();

function formatUser(user: typeof usersTable.$inferSelect) {
  return {
    id: user.id,
    username: user.username,
    email: user.email,
    role: user.role,
    fullName: user.fullName,
    siteId: user.siteId,
    createdAt: user.createdAt.toISOString(),
  };
}

router.get("/", async (req, res) => {
  try {
    const users = await db.select().from(usersTable).orderBy(usersTable.createdAt);
    res.json(users.map(formatUser));
  } catch (err) {
    req.log.error({ err }, "List users error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.post("/", async (req, res) => {
  try {
    const { username, email, password, role, fullName, siteId } = req.body;
    if (!username || !email || !password || !role || !fullName) {
      res.status(400).json({ error: "bad_request", message: "Missing required fields" });
      return;
    }
    const passwordHash = await bcrypt.hash(password, 10);
    const [user] = await db.insert(usersTable).values({ username, email, passwordHash, role, fullName, siteId }).returning();
    res.status(201).json(formatUser(user));
  } catch (err) {
    req.log.error({ err }, "Create user error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const [user] = await db.select().from(usersTable).where(eq(usersTable.id, parseInt(req.params.id))).limit(1);
    if (!user) { res.status(404).json({ error: "not_found", message: "User not found" }); return; }
    res.json(formatUser(user));
  } catch (err) {
    req.log.error({ err }, "Get user error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.put("/:id", async (req, res) => {
  try {
    const { email, role, fullName, siteId, password } = req.body;
    const updates: Partial<typeof usersTable.$inferInsert> = {};
    if (email !== undefined) updates.email = email;
    if (role !== undefined) updates.role = role;
    if (fullName !== undefined) updates.fullName = fullName;
    if (siteId !== undefined) updates.siteId = siteId;
    if (password) updates.passwordHash = await bcrypt.hash(password, 10);

    const [user] = await db.update(usersTable).set(updates).where(eq(usersTable.id, parseInt(req.params.id))).returning();
    if (!user) { res.status(404).json({ error: "not_found", message: "User not found" }); return; }
    res.json(formatUser(user));
  } catch (err) {
    req.log.error({ err }, "Update user error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.delete("/:id", async (req, res) => {
  try {
    await db.delete(usersTable).where(eq(usersTable.id, parseInt(req.params.id)));
    res.json({ success: true, message: "User deleted" });
  } catch (err) {
    req.log.error({ err }, "Delete user error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

export default router;
