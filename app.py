import os
import joblib
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Safe model loader
MODEL_PATH = "adaboost_model.pkl"
model = None

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber-Tech Intelligence Portal | AdaBoost AI</title>
    <!-- Google Fonts, FontAwesome & Chart.js -->
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {
            --bg-dark: #05050d;
            --card-bg: rgba(13, 12, 29, 0.82);
            --card-border: rgba(186, 85, 211, 0.25);
            --neon-pink: #ff007f;
            --neon-purple: #a855f7;
            --neon-cyan: #00f0ff;
            --neon-emerald: #10b981;
            --text-main: #f3f4f6;
            --text-muted: #a1a1aa;
            --input-bg: rgba(255, 255, 255, 0.04);
            --input-border: rgba(168, 85, 247, 0.3);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Space Grotesk', sans-serif;
        }

        /* Animated Synthwave Gradient Background */
        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            position: relative;
            padding: 40px 20px;
            background: linear-gradient(-45deg, #05050d, #1a0b2e, #2b0938, #031329, #05050d);
            background-size: 400% 400%;
            animation: cyberGradient 12s ease infinite;
            color: var(--text-main);
        }

        @keyframes cyberGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Particle Overlay */
        #bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .container {
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 1100px;
            background: var(--card-bg);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 45px;
            box-shadow: 0 0 50px rgba(168, 85, 247, 0.15),
                        0 20px 40px rgba(0, 0, 0, 0.8);
        }

        .header {
            text-align: center;
            margin-bottom: 35px;
        }

        .header .badge {
            display: inline-block;
            padding: 6px 18px;
            background: rgba(255, 0, 127, 0.12);
            border: 1px solid rgba(255, 0, 127, 0.4);
            border-radius: 30px;
            color: var(--neon-pink);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.2);
        }

        .header h1 {
            font-size: 2.3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, var(--neon-cyan) 50%, var(--neon-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .header p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        .grid-form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .form-group label i {
            color: var(--neon-cyan);
        }

        .form-control {
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            padding: 12px 16px;
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .form-control:focus {
            border-color: var(--neon-cyan);
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        }

        select.form-control option {
            background-color: #0d0c1d;
            color: #ffffff;
        }

        .submit-btn {
            grid-column: 1 / -1;
            margin-top: 15px;
            background: linear-gradient(135deg, var(--neon-pink) 0%, var(--neon-purple) 50%, var(--neon-cyan) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 18px;
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            box-shadow: 0 10px 30px -5px rgba(255, 0, 127, 0.5);
            position: relative;
            overflow: hidden;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px -5px rgba(0, 240, 255, 0.6);
            filter: brightness(1.15);
        }

        .submit-btn:active {
            transform: translateY(0);
        }

        /* Analytics Output Card */
        .result-card {
            margin-top: 35px;
            padding: 30px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            display: none;
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        .result-header {
            text-align: center;
            margin-bottom: 25px;
        }

        .result-title {
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .result-value {
            font-size: 1.8rem;
            font-weight: 700;
            display: inline-block;
            padding: 12px 28px;
            border-radius: 14px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--card-border);
            transition: all 0.5s ease;
        }

        .result-positive {
            color: var(--neon-emerald);
            border-color: rgba(16, 185, 129, 0.5);
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.3);
            animation: pulseEmerald 2s infinite;
        }

        .result-negative {
            color: var(--neon-pink);
            border-color: rgba(255, 0, 127, 0.5);
            box-shadow: 0 0 25px rgba(255, 0, 127, 0.3);
            animation: pulseMagenta 2s infinite;
        }

        @keyframes pulseEmerald {
            0%, 100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
            50% { box-shadow: 0 0 35px rgba(16, 185, 129, 0.6); }
        }

        @keyframes pulseMagenta {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 127, 0.3); }
            50% { box-shadow: 0 0 35px rgba(255, 0, 127, 0.6); }
        }

        .analytics-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 25px;
            margin-top: 25px;
            align-items: center;
        }

        @media (min-width: 850px) {
            .analytics-grid {
                grid-template-columns: 1.1fr 0.9fr;
            }
        }

        .chart-box {
            position: relative;
            width: 100%;
            height: 300px;
            padding: 15px;
            background: rgba(5, 5, 13, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(168, 85, 247, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .metrics-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .metric-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px;
        }

        .metric-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            justify-content: space-between;
        }

        .metric-bar-bg {
            height: 10px;
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 5px;
            overflow: hidden;
            position: relative;
        }

        .metric-bar-fill {
            height: 100%;
            width: 0%;
            border-radius: 5px;
            transition: width 1.2s cubic-bezier(0.1, 1, 0.1, 1);
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 600px) {
            .container { padding: 25px 20px; }
            .header h1 { font-size: 1.6rem; }
        }
    </style>
</head>
<body>

    <canvas id="bg-canvas"></canvas>

    <div class="container">
        <div class="header">
            <span class="badge"><i class="fa-solid fa-atom"></i> Cyber-Tech Intelligence</span>
            <h1>AdaBoost Predictive Dashboard</h1>
            <p>Input target metrics to evaluate predictive customer intelligence models</p>
        </div>

        <form id="prediction-form" class="grid-form">
            <div class="form-group">
                <label><i class="fa-solid fa-user"></i> Age</label>
                <input type="number" name="Age" class="form-control" placeholder="e.g. 34" required min="18" max="100" value="34">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-venus-mars"></i> Gender</label>
                <select name="Gender" class="form-control" required>
                    <option value="0">Female</option>
                    <option value="1" selected>Male</option>
                </select>
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-calendar-check"></i> Tenure (Months)</label>
                <input type="number" name="Tenure" class="form-control" placeholder="e.g. 12" required min="0" value="12">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-bolt"></i> Usage Frequency</label>
                <input type="number" name="Usage Frequency" class="form-control" placeholder="e.g. 18" required min="0" value="18">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-headset"></i> Support Calls</label>
                <input type="number" name="Support Calls" class="form-control" placeholder="e.g. 2" required min="0" value="2">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-clock"></i> Payment Delay (Days)</label>
                <input type="number" name="Payment Delay" class="form-control" placeholder="e.g. 5" required min="0" value="5">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-tags"></i> Subscription Type</label>
                <select name="Subscription Type" class="form-control" required>
                    <option value="0">Basic</option>
                    <option value="1" selected>Standard</option>
                    <option value="2">Premium</option>
                </select>
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-file-contract"></i> Contract Length</label>
                <select name="Contract Length" class="form-control" required>
                    <option value="0">Monthly</option>
                    <option value="1" selected>Quarterly</option>
                    <option value="2">Annual</option>
                </select>
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-dollar-sign"></i> Total Spend ($)</label>
                <input type="number" step="0.01" name="Total Spend" class="form-control" placeholder="e.g. 850.50" required min="0" value="850">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-hand-pointer"></i> Last Interaction (Days)</label>
                <input type="number" name="Last Interaction" class="form-control" placeholder="e.g. 14" required min="0" value="14">
            </div>

            <button type="submit" class="submit-btn">
                <i class="fa-solid fa-bolt-lightning"></i> Run Model Analytics
            </button>
        </form>

        <div id="result-box" class="result-card">
            <div class="result-header">
                <div class="result-title">Model Decision Output</div>
                <div id="result-text" class="result-value">---</div>
            </div>

            <div class="analytics-grid">
                <!-- Interactive Radar Chart -->
                <div class="chart-box">
                    <canvas id="radarChart"></canvas>
                </div>

                <!-- Animated Meters Panel -->
                <div class="metrics-panel">
                    <div class="metric-item">
                        <div class="metric-label">
                            <span>Risk Score Index</span>
                            <span id="riskPctText">0%</span>
                        </div>
                        <div class="metric-bar-bg">
                            <div id="riskBar" class="metric-bar-fill" style="background: linear-gradient(90deg, #10b981, #ff007f);"></div>
                        </div>
                    </div>

                    <div class="metric-item">
                        <div class="metric-label">
                            <span>Platform Activity Level</span>
                            <span id="usagePctText">0%</span>
                        </div>
                        <div class="metric-bar-bg">
                            <div id="engagementBar" class="metric-bar-fill" style="background: linear-gradient(90deg, #a855f7, #00f0ff);"></div>
                        </div>
                    </div>

                    <div class="metric-item">
                        <div class="metric-label">
                            <span>Value Metric</span>
                            <span id="spendPctText">0%</span>
                        </div>
                        <div class="metric-bar-bg">
                            <div id="spendBar" class="metric-bar-fill" style="background: linear-gradient(90deg, #ff007f, #00f0ff);"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Particle Network Acceleration Effect
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        let speedMultiplier = 1;
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const particles = [];
        const particleCount = 50;

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2.5 + 1;
                this.baseSpeedX = (Math.random() - 0.5) * 0.7;
                this.baseSpeedY = (Math.random() - 0.5) * 0.7;
                this.color = Math.random() > 0.5 ? '#ff007f' : '#00f0ff';
                this.opacity = Math.random() * 0.6 + 0.2;
            }

            update() {
                this.x += this.baseSpeedX * speedMultiplier;
                this.y += this.baseSpeedY * speedMultiplier;

                if (this.x < 0 || this.x > canvas.width) this.baseSpeedX *= -1;
                if (this.y < 0 || this.y > canvas.height) this.baseSpeedY *= -1;
            }

            draw() {
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.opacity;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();

                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < 110) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(168, 85, 247, ${0.15 - distance / 900})`;
                        ctx.lineWidth = 0.7;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();

        // Chart.js Radar Instance
        let radarChartInstance = null;

        function renderRadarChart(data) {
            const ctxRadar = document.getElementById('radarChart').getContext('2d');
            
            const normalizedData = [
                Math.min(100, (data['Age'] / 80) * 100),
                Math.min(100, (data['Tenure'] / 60) * 100),
                Math.min(100, (data['Usage Frequency'] / 30) * 100),
                Math.min(100, (data['Support Calls'] / 10) * 100),
                Math.min(100, (data['Payment Delay'] / 30) * 100),
                Math.min(100, (data['Total Spend'] / 2000) * 100)
            ];

            if (radarChartInstance) {
                radarChartInstance.destroy();
            }

            radarChartInstance = new Chart(ctxRadar, {
                type: 'radar',
                data: {
                    labels: ['Age', 'Tenure', 'Usage', 'Calls', 'Delay', 'Spend'],
                    datasets: [{
                        label: 'Feature Intensity',
                        data: normalizedData,
                        backgroundColor: 'rgba(0, 240, 255, 0.25)',
                        borderColor: '#00f0ff',
                        borderWidth: 2,
                        pointBackgroundColor: '#ff007f',
                        pointBorderColor: '#ffffff',
                        pointHoverBackgroundColor: '#ffffff',
                        pointHoverBorderColor: '#ff007f'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(168, 85, 247, 0.3)' },
                            grid: { color: 'rgba(168, 85, 247, 0.2)' },
                            pointLabels: {
                                color: '#a1a1aa',
                                font: { size: 11, family: 'Space Grotesk' }
                            },
                            ticks: { display: false },
                            suggestedMin: 0,
                            suggestedMax: 100
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }

        // AJAX Prediction Logic
        document.getElementById('prediction-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Hyper-speed particles animation trigger
            speedMultiplier = 4;
            setTimeout(() => { speedMultiplier = 1; }, 1500);

            const formData = new FormData(this);
            const data = {};
            
            formData.forEach((value, key) => {
                data[key] = parseFloat(value);
            });

            const resultBox = document.getElementById('result-box');
            const resultText = document.getElementById('result-text');

            resultBox.style.display = 'block';
            resultText.style.color = '#ffffff';
            resultText.className = 'result-value';
            resultText.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing Model...';

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const res = await response.json();
                if (res.status === 'success') {
                    resultText.className = 'result-value ' + (res.prediction === 1 ? 'result-negative' : 'result-positive');
                    resultText.innerHTML = res.label;

                    // Render Animated Radar Chart
                    renderRadarChart(data);

                    // Compute Percentage Metrics
                    const riskPct = res.prediction === 1 ? 88 : 12;
                    const usagePct = Math.round(Math.min(100, (data['Usage Frequency'] / 30) * 100));
                    const spendPct = Math.round(Math.min(100, (data['Total Spend'] / 2000) * 100));

                    // Animate Bar Widths & Text Counters
                    setTimeout(() => {
                        document.getElementById('riskBar').style.width = riskPct + '%';
                        document.getElementById('engagementBar').style.width = usagePct + '%';
                        document.getElementById('spendBar').style.width = spendPct + '%';

                        document.getElementById('riskPctText').innerText = riskPct + '%';
                        document.getElementById('usagePctText').innerText = usagePct + '%';
                        document.getElementById('spendPctText').innerText = spendPct + '%';
                    }, 100);

                } else {
                    resultText.className = 'result-value';
                    resultText.style.color = '#ff007f';
                    resultText.innerText = 'Error: ' + res.message;
                }
            } catch (err) {
                resultText.className = 'result-value';
                resultText.style.color = '#ff007f';
                resultText.innerText = 'Execution Failed. Check server logs.';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({
            'status': 'error', 
            'message': 'Model file (adaboost_model.pkl) was not found or failed to load on the server.'
        }), 500

    try:
        data = request.get_json(force=True)
        
        feature_order = [
            'Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls',
            'Payment Delay', 'Subscription Type', 'Contract Length', 
            'Total Spend', 'Last Interaction'
        ]
        
        features = []
        for feat in feature_order:
            val = data.get(feat)
            if val is None:
                return jsonify({
                    'status': 'error', 
                    'message': f'Missing value for feature: "{feat}"'
                }), 400
            features.append(float(val))

        input_array = np.array([features])
        prediction = int(model.predict(input_array)[0])
        
        label = "High Risk / Churn Predicted" if prediction == 1 else "Low Risk / Active Customer"

        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'label': label
        })

    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': f'Prediction Error: {str(e)}'
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
