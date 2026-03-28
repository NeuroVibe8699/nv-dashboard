import { Router } from "express";
import healthRouter from "./health";
import authRouter from "./auth";
import usersRouter from "./users";
import sitesRouter from "./sites";
import devicesRouter from "./devices";
import alertsRouter from "./alerts";

const router = Router();

router.use(healthRouter);
router.use("/auth", authRouter);
router.use("/users", usersRouter);
router.use("/sites", sitesRouter);
router.use("/devices", devicesRouter);
router.use("/alerts", alertsRouter);

export default router;
