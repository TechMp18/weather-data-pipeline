// ============================================================================
// app.js — Dashboard JavaScript (Dashboard ka Logic)
// ============================================================================
//
// 🎯 YEH FILE KYA HAI?
// Yeh file dashboard ko "alive" banati hai:
// - Server se data fetch karti hai (API calls)
// - Tables mein data dikhati hai
// - Charts banati hai
// - Run Pipeline button kaam karata hai
//
// 📚 CONCEPTS used here:
// 1. fetch() — API se data laana (HTTP request from browser)
// 2. async/await — asynchronous code (wait karo jab tak data aaye)
// 3. DOM Manipulation — HTML elements ko JavaScript se change karna
// 4. Template Literals — backtick strings (` `) mein variables daal sakte ho
// ============================================================================

// API ka base URL
// Empty string = relative URL (same server pe request jayegi)
// Ye localhost pe bhi kaam karega aur deployed URL pe bhi!
const API_URL = "";

// ---------------------------------------------------------------------------
// 🚀 Page Load Hone Pe — Sab data fetch karo
// ---------------------------------------------------------------------------
// window.addEventListener("load", ...) — jab page fully load ho jaaye tab chalao
// DOMContentLoaded se ye different hai:
// - DOMContentLoaded: HTML ready hone pe (images loading hogi abhi)
// - load: SABB ready hone pe (images bhi load ho gayi)
// ---------------------------------------------------------------------------

window.addEventListener("load", () => {
    addLog("🚀 Dashboard initialized", "info");
    fetchAllData();
});

// Har 60 seconds mein auto-refresh (fresh data dikhane ke liye)
setInterval(fetchAllData, 60000);
// ☝️ setInterval(function, milliseconds) — har X milliseconds mein function chalao
// 60000ms = 60 seconds = 1 minute


async function fetchAllData() {
    // ☝️ async function — ye function "await" use kar sakta hai
    // await matlab: "is line pe ruko jab tak result na aa jaaye"
    
    addLog("📡 Fetching latest data...", "info");
    
    // Teeno API calls parallel mein chalao (faster!)
    await Promise.all([
        fetchStats(),
        fetchSummary(),
        fetchRecords(),
    ]);
    // ☝️ Promise.all() — saare promises ek saath chalao aur sab ke complete
    // hone ka wait karo. Agar ek bhi fail ho toh error aayega.
    // Ye ek-ek karke call karne se TEZZ hai!
    
    addLog("✅ Data refreshed successfully", "success");
}


// ============================================================================
// 📊 Pipeline Stats Fetch Karna
// ============================================================================

async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/api/stats`);
        // ☝️ fetch() — browser se HTTP request bhejta hai (GET by default)
        // await — ruko jab tak response na aaye
        // Template literal: `${API_URL}/api/stats` → "http://localhost:5050/api/stats"
        
        const data = await response.json();
        // ☝️ response.json() — JSON text ko JavaScript object mein convert karo
        
        // HTML elements update karo
        document.getElementById("total-records").textContent = data.total_records || 0;
        document.getElementById("total-cities").textContent = data.total_cities || 0;
        document.getElementById("avg-temp").textContent = data.overall_avg_temp 
            ? `${data.overall_avg_temp}°C` : "—";
        
        // Last run time format karo
        if (data.last_run) {
            const date = new Date(data.last_run);
            document.getElementById("last-run").textContent = formatTime(date);
        }
        // ☝️ document.getElementById("id") — HTML element dhundho uske ID se
        // .textContent — element ka text change karo
        
    } catch (error) {
        console.error("Stats fetch error:", error);
        addLog("❌ Failed to fetch stats", "error");
    }
}


// ============================================================================
// 📈 City Summary Fetch Karna + Chart Banana
// ============================================================================

async function fetchSummary() {
    try {
        const response = await fetch(`${API_URL}/api/summary`);
        const data = await response.json();
        
        // Summary count badge update karo
        document.getElementById("summary-count").textContent = `${data.length} cities`;
        
        // Table fill karo
        renderSummaryTable(data);
        
        // Chart banao
        renderChart(data);
        
    } catch (error) {
        console.error("Summary fetch error:", error);
        addLog("❌ Failed to fetch city summary", "error");
    }
}


function renderSummaryTable(data) {
    // ☝️ Yeh function HTML table ko data se fill karta hai
    
    const tbody = document.getElementById("summary-body");
    tbody.innerHTML = ""; // Pehle purana data clear karo
    
    // Har city ke liye ek row banao
    data.forEach(city => {
        // ☝️ forEach — array ke har element pe function chalao
        // city = { city: "Delhi", avg_temp: 35, min_temp: 20, ... }
        
        const row = document.createElement("tr");
        // ☝️ createElement("tr") — ek naya <tr> element banao
        
        // Temperature bar ka width calculate karo (0°C = 0%, 50°C = 100%)
        const barWidth = Math.min((city.avg_temp / 50) * 100, 100);
        const barColor = getTemperatureColor(city.avg_temp);
        
        row.innerHTML = `
            <td style="font-weight: 600; color: var(--text-primary);">${city.city}</td>
            <td style="color: ${barColor}; font-weight: 600;">${city.avg_temp}°C</td>
            <td>${city.min_temp}°C</td>
            <td>${city.max_temp}°C</td>
            <td>${city.avg_humidity}%</td>
            <td><span class="badge">${city.record_count}</span></td>
            <td>
                <div class="temp-bar-container">
                    <div class="temp-bar" style="width: ${barWidth}%; background: ${barColor};"></div>
                </div>
            </td>
        `;
        // ☝️ Template Literal (backtick string) — ${variable} se variable ki
        // value string mein daal sakte ho. Bahut powerful!
        // row.innerHTML — element ke andar ka HTML set karo
        
        tbody.appendChild(row);
        // ☝️ appendChild() — parent element mein child add karo
        // tbody ke andar <tr> row add ho jayega
    });
}


function renderChart(data) {
    // ☝️ Yeh function ek simple bar chart banata hai (bina kisi library ke!)
    
    const container = document.getElementById("temp-chart");
    container.innerHTML = "";
    
    if (data.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); text-align: center; width: 100%; padding: 2rem;">No data yet. Run the pipeline first!</p>';
        return;
    }
    
    // Sabse zyada temperature dhundho (chart scaling ke liye)
    const maxTemp = Math.max(...data.map(d => d.avg_temp));
    // ☝️ Math.max(...array) — array mein se sabse badi value
    // data.map(d => d.avg_temp) — sirf temperatures ka array banao
    // Spread operator (...) — array ko individual arguments mein spread karta hai
    
    data.forEach((city, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "chart-bar-wrapper";
        
        // Bar ki height calculate karo (relative to max temp)
        const height = Math.max((city.avg_temp / maxTemp) * 200, 10);
        const color = getTemperatureColor(city.avg_temp);
        
        wrapper.innerHTML = `
            <div class="chart-bar-value">${city.avg_temp}°C</div>
            <div class="chart-bar" style="height: ${height}px; background: linear-gradient(180deg, ${color}, ${color}88);"></div>
            <div class="chart-bar-label">${city.city}</div>
        `;
        
        // Animation delay — bars ek ke baad ek aayenge (cool effect!)
        wrapper.style.animationDelay = `${index * 0.1}s`;
        
        container.appendChild(wrapper);
    });
}


// ============================================================================
// 📋 Latest Records Fetch Karna
// ============================================================================

async function fetchRecords() {
    try {
        const response = await fetch(`${API_URL}/api/records`);
        const data = await response.json();
        
        document.getElementById("records-count").textContent = `${data.length} records`;
        
        const tbody = document.getElementById("records-body");
        tbody.innerHTML = "";
        
        // Sirf pehle 30 records dikhao (performance ke liye)
        data.slice(0, 30).forEach(record => {
            // ☝️ .slice(0, 30) — array ke pehle 30 elements lo
            
            const row = document.createElement("tr");
            
            // Category badge ka class
            const catClass = `category-${(record.temp_category || "unknown").toLowerCase().replace(" ", "-")}`;
            const comfortClass = `comfort-${(record.comfort_index || "unknown").toLowerCase()}`;
            
            row.innerHTML = `
                <td style="font-weight: 500; color: var(--text-primary);">${record.city}</td>
                <td style="color: ${getTemperatureColor(record.temperature)}; font-weight: 600;">
                    ${record.temperature}°C
                </td>
                <td>${record.feels_like ? record.feels_like + "°C" : "—"}</td>
                <td>${record.humidity ? record.humidity + "%" : "—"}</td>
                <td>${getWeatherEmoji(record.weather_condition)} ${record.weather_condition || "—"}</td>
                <td><span class="category-badge ${catClass}">${record.temp_category || "—"}</span></td>
                <td class="${comfortClass}">${record.comfort_index || "—"}</td>
                <td style="color: var(--text-muted); font-size: 0.75rem;">
                    ${formatTimestamp(record.timestamp)}
                </td>
            `;
            
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error("Records fetch error:", error);
        addLog("❌ Failed to fetch records", "error");
    }
}


// ============================================================================
// 🚀 Run Pipeline Button
// ============================================================================

async function runPipeline() {
    const btn = document.getElementById("run-pipeline-btn");
    btn.classList.add("loading");
    btn.innerHTML = '<span class="btn-icon">⏳</span> Running...';
    
    addLog("🚀 Pipeline triggered from dashboard...", "info");
    
    try {
        const response = await fetch(`${API_URL}/api/run`, {
            method: "POST",
            // ☝️ POST method — server pe kuch "action" karna hai (pipeline chalana)
            // GET sirf data MAANGNE ke liye, POST kuch KARNE ke liye
        });
        
        const result = await response.json();
        
        if (result.status === "success") {
            addLog("✅ Pipeline completed successfully!", "success");
            addLog(`📊 Extracted: ${result.result.extracted}, Loaded: ${result.result.loaded}`, "success");
            
            // Data refresh karo (naye records dikhane ke liye)
            await fetchAllData();
        } else {
            addLog(`❌ Pipeline failed: ${result.message}`, "error");
        }
        
    } catch (error) {
        addLog(`❌ Error running pipeline: ${error.message}`, "error");
    }
    
    // Button wapas normal karo
    btn.classList.remove("loading");
    btn.innerHTML = '<span class="btn-icon">🚀</span> Run Pipeline';
}


// ============================================================================
// 🛠️ Helper Functions (Chhote helper tools)
// ============================================================================

function getTemperatureColor(temp) {
    // Temperature ke hisaab se color do
    if (temp < 10) return "#3b82f6";      // Blue = Cold
    if (temp < 20) return "#06b6d4";      // Cyan = Cool
    if (temp < 30) return "#10b981";      // Green = Pleasant
    if (temp < 38) return "#f59e0b";      // Orange = Hot
    return "#ef4444";                      // Red = Very Hot
}


function getWeatherEmoji(condition) {
    // Weather condition ke liye emoji
    const emojiMap = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "🌨️",
        "Mist": "🌫️",
        "Haze": "🌫️",
        "Fog": "🌫️",
    };
    return emojiMap[condition] || "🌡️";
}


function formatTimestamp(timestamp) {
    // Timestamp ko readable format mein convert karo
    if (!timestamp) return "—";
    try {
        const date = new Date(timestamp);
        return date.toLocaleString("en-IN", { 
            day: "2-digit", 
            month: "short", 
            hour: "2-digit", 
            minute: "2-digit" 
        });
    } catch {
        return timestamp;
    }
}


function formatTime(date) {
    // Time ko "Just now", "5 min ago" format mein
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds mein difference
    
    if (diff < 60) return "Just now";
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return date.toLocaleDateString("en-IN");
}


// ============================================================================
// 📝 Pipeline Activity Log
// ============================================================================

function addLog(message, type = "info") {
    // Dashboard pe log messages dikhao
    const logContainer = document.getElementById("pipeline-log");
    
    const entry = document.createElement("div");
    entry.className = `log-entry log-${type}`;
    
    const time = new Date().toLocaleTimeString("en-IN");
    entry.textContent = `[${time}] ${message}`;
    
    // Naya log sabse upar add karo
    logContainer.insertBefore(entry, logContainer.firstChild);
    // ☝️ insertBefore(newChild, refChild) — refChild ke PEHLE newChild add karo
    // Isse newest log sabse upar dikhega!
    
    // Zyada purane logs hata do (max 50)
    while (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}


function clearLog() {
    // Log clear karo
    const logContainer = document.getElementById("pipeline-log");
    logContainer.innerHTML = "";
    addLog("🧹 Log cleared", "info");
}
