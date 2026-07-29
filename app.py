import os
import joblib
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Load the trained AdaBoost model
MODEL_PATH = "adaboost_model.pkl"
model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# HTML/CSS/JS Template with Dynamic Canvas Background & Premium UI Design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Prediction Portal | ML Analytics</title>
    <!-- Google Fonts & FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-dark: #0a0e17;
            --card-bg: rgba(16, 24, 40, 0.75);
            --card-border: rgba(255, 255, 255, 0.08);
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-purple: #7f00ff;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --input-bg: rgba(255, 255, 255, 0.03);
            --input-border: rgba(255, 255, 255, 0.12);
            --success-color: #10b981;
            --danger-color: #f43f5e;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            position: relative;
            padding: 40px 20px;
        }

        /* Animated Interactive Canvas Background */
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
            max-width: 1000px;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 45px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6),
                        0 0 40px rgba(0, 242, 254, 0.05);
        }

        .header {
            text-align: center;
            margin-bottom: 35px;
        }

        .header .badge {
            display: inline-block;
            padding: 6px 16px;
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid rgba(0, 242, 254, 0.25);
            border-radius: 30px;
            color: var(--accent-cyan);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, var(--accent-cyan) 100%);
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
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
            color: var(--accent-cyan);
        }

        .form-control {
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            padding: 12px 16px;
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            border-color: var(--accent-cyan);
            background: rgba(255, 255, 255, 0.06);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        }

        select.form-control option {
            background-color: #101828;
            color: #ffffff;
        }

        .submit-btn {
            grid-column: 1 / -1;
            margin-top: 15px;
            background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            box-shadow: 0 10px 25px -5px rgba(79, 172, 254, 0.4);
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(79, 172, 254, 0.6);
            filter: brightness(1.1);
        }

        .submit-btn:active {
            transform: translateY(0);
        }

        /* Result Section Styling */
        .result-card {
            margin-top: 30px;
            padding: 24px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            text-align: center;
            display: none;
            animation: fadeIn 0.5s ease-in-out forwards;
        }

        .result-title {
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .result-value {
            font-size: 1.8rem;
            font-weight: 700;
        }

        .result-positive {
            color: var(--success-color);
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }

        .result-negative {
            color: var(--danger-color);
            text-shadow: 0 0 20px rgba(244, 63, 94, 0.3);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 600px) {
            .container { padding: 25px 20px; }
            .header h1 { font-size: 1.6rem; }
        }
    </style>
</head>
<body>

    <!-- Particle Canvas Background -->
    <canvas id="bg-canvas"></canvas>

    <div class="container">
        <div class="header">
            <span class="badge"><i class="fa-solid fa-chart-line"></i> Enterprise Analytics</span>
            <h1>AdaBoost Intelligence Portal</h1>
            <p>Input dynamic metrics to evaluate predictive customer intelligence models</p>
        </div>

        <form id="prediction-form" class="grid-form">
            <div class="form-group">
                <label><i class="fa-solid fa-user"></i> Age</label>
                <input type="number" name="Age" class="form-control" placeholder="e.g. 34" required min="18" max="100">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-venus-mars"></i> Gender</label>
                <select name="Gender" class="form-control" required>
                    <option value="" disabled selected>Select Gender</option>
                    <option value="0">Female</option>
                    <option value="1">Male</option>
                </select>
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-calendar-check"></i> Tenure (Months)</label>
                <input type="number" name="Tenure" class="form-control" placeholder="e.g. 12" required min="0">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-bolt"></i> Usage Frequency</label>
                <input type="number" name="Usage Frequency" class="form-control" placeholder="e.g. 18" required min="0">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-headset"></i> Support Calls</label>
                <input type="number" name="Support Calls" class="form-control" placeholder="e.g. 2" required min="0">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-clock"></i> Payment Delay (Days)</label>
                <input type="number" name="Payment Delay" class="form-control" placeholder="e.g. 5" required min="0">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-tags"></i> Subscription Type</label>
                <select name="Subscription Type" class="form-control" required>
                    <option value="" disabled selected>Select Type</option>
                    <option value="0">Basic</option>
                    <option value="1">Standard</option>
                    <option value="2">Premium</option>
                </select>
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-file-contract"></i> Contract Length</label>
                <select name="Contract Length" class="form-control" required>
                    <option value="" disabled selected>Select Length</option>
                    <option value="0">Monthly</option>
                    <option value="1">Quarterly</option>
                    <option value="2">Annual</option>
                </select>
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-dollar-sign"></i> Total Spend ($)</label>
                <input type="number" step="0.01" name="Total Spend" class="form-control" placeholder="e.g. 850.50" required min="0">
            </div>

            <div class="form-group">
                <label><i class="fa-solid fa-hand-pointer"></i> Last Interaction (Days ago)</label>
                <input type="number" name="Last Interaction" class="form-control" placeholder="e.g. 14" required min="0">
            </div>

            <button type="submit" class="submit-btn">
                <i class="fa-solid fa-microchip"></i> Execute Model Prediction
            </button>
        </form>

        <div id="result-box" class="result-card">
            <div class="result-title">Model Evaluation Output</div>
            <div id="result-text" class="result-value">---</div>
        </div>
    </div>

    <!-- Canvas Animation & Ajax Interaction -->
    <script>
        // Interactive Canvas Animation Setup
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const particles = [];
        const particleCount = 45;

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 1;
                this.speedX = (Math.random() - 0.5) * 0.8;
                this.speedY = (Math.random() - 0.5) * 0.8;
                this.opacity = Math.random() * 0.5 + 0.2;
            }

            update() {
                this.x += this.speedX;
                this.y += this.speedY;

                if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
                if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
            }

            draw() {
                ctx.fillStyle = `rgba(0, 242, 254, ${this.opacity})`;
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

                    if (distance < 120) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(79, 172, 254, ${0.15 - distance / 800})`;
                        ctx.lineWidth = 0.8;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();

        // AJAX Form Submission Handling
        document.getElementById('prediction-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => data[key] = parseFloat(value));

            const resultBox = document.getElementById('result-box');
            const resultText = document.getElementById('result-text');

            resultBox.style.display = 'block';
            resultText.style.color = '#ffffff';
            resultText.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing Model...';

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
                } else {
                    resultText.className = 'result-value';
                    resultText.style.color = '#f43f5e';
                    resultText.innerText = 'Error: ' + res.message;
                }
            } catch (err) {
                resultText.className = 'result-value';
                resultText.style.color = '#f43f5e';
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
        return jsonify({'status': 'error', 'message': 'Model file not found or loaded.'}), 500

    try:
        data = request.get_json()
        
        # Extract features in exact feature order expected by the AdaBoost model
        feature_order = [
            'Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls',
            'Payment Delay', 'Subscription Type', 'Contract Length', 
            'Total Spend', 'Last Interaction'
        ]
        
        features = [data[feat] for feat in feature_order]
        input_array = np.array([features])

        prediction = int(model.predict(input_array)[0])
        
        # Customizable result dynamic labels
        label = "High Risk / Churn Predicted" if prediction == 1 else "Low Risk / Active Customer"

        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'label': label
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
