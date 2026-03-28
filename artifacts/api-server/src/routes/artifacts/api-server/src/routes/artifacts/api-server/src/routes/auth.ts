import { Router, type IRouter } from "express";
import { db } from "@workspace/db";
import { usersTable } from "@workspace/db";
import { eq } from "drizzle-orm";
import bcrypt from "bcryptjs";

const router: IRouter = Router();

router.post("/login", async (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      res.status(400).json({ error: "bad_request", message: "Username and password required" });
      return;
    }

    const [user] = await db.select().from(usersTable).where(eq(usersTable.username, username)).limit(1);

    if (!user) {
      res.status(401).json({ error: "unauthorized", message: "Invalid credentials" });
      return;
    }

    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
      res.status(401).json({ error: "unauthorized", message: "Invalid credentials" });
      return;
    }

    (req as any).session = { userId: user.id, role: user.role };
    res.cookie("session", JSON.stringify({ userId: user.id, role: user.role }), {
      httpOnly: true,
      maxAge: 7 * 24 * 60 * 60 * 1000,
      sameSite: "lax",
    });

    res.json({
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        fullName: user.fullName,
        siteId: user.siteId,
        createdAt: user.createdAt.toISOString(),
      },
    });
  } catch (err) {
    req.log.error({ err }, "Login error");
    res.status(500).json({ error: "server_error", message: "Internal server error" });
  }
});

router.post("/logout", (_req, res) => {
  res.clearCookie("session");
  res.json({ success: true, message: "Logged out" });
});

router.get("/me", async (req, res) => {
  try {
    const cookieStr = req.cookies?.session;
    if (!cookieStr) {
      res.status(401).json({ error: "unauthorized", message: "Not authenticated" });
      return;
    }

    const session = JSON.parse(cookieStr);
    const [user] = await db.select().from(usersTable).where(eq(usersTable.id, session.userId)).limit(1);

    if (!user) {
      res.status(401).json({ error: "unauthorized", message: "Not authenticated" });
      return;
    }

    res.json({
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      fullName: user.fullName,
      siteId: user.siteId,
      createdAt: user.createdAt.toISOString(),
    });
  } catch {
    res.status(401).json({ error: "unauthorized", message: "Not authenticated" });
  }
});

export default router;
