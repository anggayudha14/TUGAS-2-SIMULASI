from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Sistem Antrian M/M/2</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(120deg, #4facfe, #00f2fe);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .card {
            background: white;
            width: 420px;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        h2 {
            text-align: center;
            color: #333;
        }

        label {
            font-weight: 600;
            color: #444;
        }

        input {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #4facfe;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #00c6ff;
        }

        .hasil {
            background: #f4f9ff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }

        ul {
            padding-left: 20px;
        }

        li {
            margin-bottom: 6px;
        }

        .error {
            color: red;
            text-align: center;
            margin-bottom: 10px;
        }

        .ulang {
            display: block;
            margin-top: 15px;
            text-align: center;
            text-decoration: none;
            color: #4facfe;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>Sistem Antrian M/M/2</h2>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    {% if not hasil %}
    <form method="post">
        <label>Waktu Antar Kedatangan (menit)</label>
        <input type="number" step="any" name="kedatangan" required>

        <label>Waktu Pelayanan per Pelayan (menit)</label>
        <input type="number" step="any" name="pelayanan" required>

        <button type="submit">Hitung</button>
    </form>
    {% endif %}

    {% if hasil %}
    <div class="hasil">
        <b>Input:</b>
        <ul>
            <li>Waktu antar kedatangan = {{ wk }} menit</li>
            <li>Waktu pelayanan = {{ wp }} menit</li>
        </ul>

        <b>Hasil Perhitungan:</b>
        <ul>
            <li>λ = {{ lamda }}</li>
            <li>μ = {{ mu }}</li>
            <li>ρ = {{ rho }}</li>
            <li>W = {{ W }} menit</li>
            <li>Wq = {{ Wq }} menit</li>
        </ul>
    </div>

    <a href="/" class="ulang">Hitung Ulang</a>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            wk = float(request.form["kedatangan"])
            wp = float(request.form["pelayanan"])

            if wk <= 0 or wp <= 0:
                return render_template_string(HTML, error="Input harus bernilai positif", hasil=False)

            lamda = 1 / wk
            mu = 1 / wp
            rho = lamda / (2 * mu)
            W = 1 / (mu - lamda / 2)
            Wq = (lamda ** 2) / (2 * mu * (mu - lamda / 2))

            return render_template_string(
                HTML,
                hasil=True,
                wk=wk,
                wp=wp,
                lamda=round(lamda, 4),
                mu=round(mu, 4),
                rho=round(rho, 4),
                W=round(W, 4),
                Wq=round(Wq, 4)
            )

        except:
            return render_template_string(HTML, error="Input tidak valid", hasil=False)

    return render_template_string(HTML, hasil=False)

if __name__ == "__main__":
    app.run(debug=True)
