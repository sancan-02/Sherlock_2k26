import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ---- OFFICIAL ANSWER ----
CORRECT_ANSWER = "0.567"

# ---- FLAG FROM ENVIRONMENT VARIABLE ----
FLAG = os.getenv("FLAG")
if not FLAG:
    raise RuntimeError(
        "FLAG environment variable is not set!\n"
        "Set it before running the server.\n"
        "Example (PowerShell): $env:FLAG='IET{...}'"
    )

# ---- Sherlock Themed Page ----
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sherlock's Answer Vault</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: "Georgia", serif;
            background: radial-gradient(circle at top, #1b1b1b, #0b0b0b);
            color: #f5f5f5;
        }

        .card {
            width: min(600px, 92vw);
            padding: 34px;
            border-radius: 18px;
            background: rgba(25, 25, 25, 0.92);
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.75);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        h2 {
            margin: 0;
            font-size: 26px;
            letter-spacing: 1px;
        }

        p {
            margin-top: 12px;
            font-size: 15px;
            color: #cfcfcf;
            line-height: 1.75;
            white-space: pre-line;
        }

        .hint {
            margin: 18px 0;
            font-size: 13px;
            color: #9e9e9e;
            font-style: italic;
        }

        .subtle {
            margin-top: 8px;
            font-size: 12px;
            color: rgba(212, 175, 55, 0.75);
        }

        input {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 10px;
            border: none;
            outline: none;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.08);
            color: white;
            text-align: center;
            letter-spacing: 1px;
        }

        input::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }

        button {
            width: 100%;
            margin-top: 18px;
            padding: 12px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            background: linear-gradient(135deg, #d4af37, #8a6f1d);
            color: #111;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 6px 18px rgba(212, 175, 55, 0.4);
        }

        .footer {
            margin-top: 18px;
            font-size: 12px;
            color: rgba(255, 255, 255, 0.35);
        }

        code {
            background: rgba(255, 255, 255, 0.08);
            padding: 4px 8px;
            border-radius: 6px;
            color: #d4af37;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>🕵️ Sherlock's Answer Vault</h2>
        <p>
When the mind grows restless, Holmes seeks a remedy—not in noise, but in chemistry.
A quiet vial, precisely measured… not pure, but diluted to a careful fraction.
Let x be the dose, let the curve confess its rise and fall—
        </p>

        <div class="hint">
            The vault opens only to a value that is neither whole nor careless.
            A single slip, and the case collapses.
            <div class="subtle">⚠️ A good detective counts till the <b>third mark</b>.</div>
        </div>

        <form method="POST" action="/submit">
            <input type="text" name="answer" placeholder="Enter the exact value..." required />
            <button type="submit">🔍 Verify Answer</button>
        </form>

        <div class="footer">
            Precision is proof • Baker Street Archives
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/submit", methods=["POST"])
def submit():
    participant_answer = request.form.get("answer", "").strip()

    if participant_answer == CORRECT_ANSWER:
        return f"""
        <div style="font-family: Georgia, serif; text-align:center; padding:50px; background:#0b0b0b; color:#f5f5f5; height:100vh;">
            <h2 style="color:#d4af37;">✅ Correct! The case is solved.</h2>
            <p>Your flag is:</p>
            <code style="font-size:18px;">{FLAG}</code>
            <br><br>
            <a href="/" style="color:#d4af37; text-decoration:none;">🔙 Back to Vault</a>
        </div>
        """
    else:
        return """
        <div style="font-family: Georgia, serif; text-align:center; padding:50px; background:#0b0b0b; color:#f5f5f5; height:100vh;">
            <h2 style="color:#ff4d4d;">❌ Incorrect! The trail has gone cold.</h2>
            <p>Re-check your deductions and try again.</p>
            <a href="/" style="color:#d4af37; text-decoration:none;">🔙 Try Again</a>
        </div>
        """


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json(force=True)
    participant_answer = str(data.get("answer", "")).strip()

    if participant_answer == CORRECT_ANSWER:
        return jsonify({"correct": True, "flag": FLAG})
    else:
        return jsonify({"correct": False})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
