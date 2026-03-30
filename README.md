# NeuroVibe AI — Predictive Maintenance Dashboard

**NeuroVibe AI Technologies Pvt Ltd**  
Industrial Intelligence Ecosystem for Predictive Maintenance

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | Node.js, Express, TypeScript |
| Database | PostgreSQL (Drizzle ORM) |
| API Client | Auto-generated via Orval + OpenAPI 3.1 |
| Auth | JWT (HS256), bcryptjs |

## Features

- **Intelligence Overview** — Fleet Health KPIs, Asset Risk Profile, Implementation Workflow
- **Asset Risk Profile** — Machine status monitoring with 6 sensor types
- **Machine Detail** — Temperature, Vibration, Ultrasound, Magnetic Flux, Pressure, RPM trend charts
- **Predictive ML Logic** — Alert management and anomaly tracking
- **Spectrum Analysis** — Edge Gateway + Sensor Node inventory with CSV Import/Export
  - Gateway: Model (NV1001-NV1010), Serial No, IMEI, Radio MAC, LAN MAC, WAN MAC, BLE MAC
  - Node: Model (NVS1001-NVS1010), Serial No, Radio MAC, BLE MAC
  - Per-node configuration page with Motor Recipe + Installation Matrix
- **Maintenance Reports** — Maintenance scheduling and records
- **User Management** — Role-based access (admin / operator / viewer)
- **Site Map** — Interactive SVG plant floor map

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| rajesh.kumar | operator123 | Operator |
| suresh.patel | viewer123 | Viewer |

## Project Structure

```
.
├── artifacts/
│   ├── api-server/          # Express API (port 8080)
│   └── neurovibe-dashboard/ # React + Vite frontend
├── lib/
│   ├── api-spec/            # OpenAPI 3.1 spec + orval codegen
│   ├── api-client-react/    # Auto-generated React Query hooks
│   ├── api-zod/             # Auto-generated Zod validators
│   └── db/                  # Drizzle ORM schema + migrations
└── scripts/                 # Seed scripts
```

## Sensor Node CSV Format

**Gateway CSV:** `Model, Serial No, IMEI, Radio MAC, LAN MAC, WAN MAC, BLE MAC`

**Node CSV:** `Model, Serial No, Radio MAC, BLE MAC`

### Gateway Models
NV1001 868MHz · NV1002 915MHz · NV1003–NV1010

### Node Models
NVS1001 868MHz · NVS1002 915MHz · NVS1003 868MHz AI MODEL · NVS1004 915MHz AI MODEL · NVS1005–NVS1010

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET=your-secret-key
PORT=8080       # API server port
```

## Development Setup

```bash
pnpm install
pnpm --filter @workspace/db run push        # Apply DB schema
pnpm --filter @workspace/api-spec run codegen  # Generate API client
pnpm --filter @workspace/api-server run dev    # Start API (port 8080)
pnpm --filter @workspace/neurovibe-dashboard run dev  # Start frontend
```
