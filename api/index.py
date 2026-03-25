<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NeuroVibe Admin | Inventory Control</title>
    <style>
        :root { --blue: #4facfe; --orange: #ff9933; --bg: #0d1117; --card: #161b22; }
        body { background: var(--bg); color: white; font-family: sans-serif; padding: 20px; }
        .card { background: var(--card); border: 1px solid #334155; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
        .btn { border:none; padding:10px 15px; border-radius:6px; cursor:pointer; font-weight:bold; color:white; }
        .btn-blue { background: var(--blue); }
        .btn-orange { background: var(--orange); }
        select, input { background:#0d1117; border:1px solid #334155; color:white; padding:10px; border-radius:6px; margin-bottom:10px; width: 100%; box-sizing: border-box; }
        h3 { font-size:14px; color:var(--orange); margin-top:0; border-bottom:1px solid #334155; padding-bottom:10px; }
    </style>
</head>
<body>

    <h2 style="color:var(--blue); font-size:18px;">NEUROVIBE AI TECHNOLOGIES PVT LTD</h2>

    <!-- 1. Separate Inventory Import -->
    <div class="card">
        <h3>1. GATEWAY & NODE INVENTORY (EXCEL IMPORT)</h3>
        <p style="font-size:10px; color:gray;">SR NO | MODEL | IMEI | RADIO MAC | BLE MAC</p>
        <select id="importType">
            <option value="gateway">IMPORT TO GATEWAY COLUMN</option>
            <option value="node">IMPORT TO NODE COLUMN</option>
        </select>
        <input type="file" id="excelFile">
        <div style="display:flex; gap:10px;">
            <button class="btn btn-blue" style="flex:1;">UPLOAD INVENTORY</button>
            <button class="btn btn-orange" style="flex:1;" onclick="window.location.href='/api/export'">EXPORT TO EXCEL (.xlsx)</button>
        </div>
    </div>

    <!-- 2. Provisioning with Discovery -->
    <div class="card">
        <h3>2. PROVISIONING (TOKEN GENERATION)</h3>
        <p style="font-size:10px; color:gray;">If MAC ID is unknown, select from discovered devices below:</p>
        <select id="discoveryDropdown">
            <option value="">-- MAC ID Nahi Pata? Select Discovered --</option>
            <option value="MAC1">NEW GATEWAY (Detected: F1:B2)</option>
            <option value="MAC2">NEW NODE (Detected: A5:C8)</option>
        </select>
        <div style="text-align:center; font-size:10px; margin-bottom:10px;">OR ENTER MANUALLY</div>
        <input type="text" id="manualMac" placeholder="Enter MAC ID (e.g. GW-NV-001)">
        <button class="btn btn-blue" style="width:100%;" onclick="alert('Token Generated: NV-7862')">ASK TOKEN NO</button>
    </div>

    <a href="dashboard.html" style="color:var(--blue); text-decoration:none; font-size:12px;">← Back to Live Dashboard</a>

</body>
</html>
