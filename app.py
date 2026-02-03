import os
from flask import Flask, request, render_template_string, jsonify, redirect, url_for

app = Flask(__name__)

CHALLENGE_1_ANSWER = os.getenv("CHALLENGE_1_ANSWER")
CHALLENGE_2_ANSWER = os.getenv("CHALLENGE_2_ANSWER")

if not CHALLENGE_1_ANSWER or not CHALLENGE_2_ANSWER:
    raise RuntimeError("CHALLENGE_1_ANSWER and CHALLENGE_2_ANSWER must be set")

FLAG_1 = os.getenv("FLAG_1")
FLAG_2 = os.getenv("FLAG_2")

if not FLAG_1 or not FLAG_2:
    raise RuntimeError("Both FLAG_1 and FLAG_2 must be set")

HTML_1 = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>The Silent Machine</title>

  <style>
    :root{
      --paper:#f6f1e4;
      --paper2:#efe6d2;
      --ink:#1f2937;
      --muted:#4b5563;
      --seal:#7a2e2e;
      --gold:#a07c2c;
      --shadow: rgba(0,0,0,0.18);
      --line: rgba(31,41,55,0.16);
    }

    *{box-sizing:border-box;}

    body{
      margin:0;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:28px;
      color:var(--ink);
      font-family: Georgia, "Times New Roman", serif;

      background:
        radial-gradient(900px 500px at 20% 10%, rgba(160,124,44,0.10), transparent 55%),
        radial-gradient(900px 500px at 90% 85%, rgba(122,46,46,0.10), transparent 55%),
        linear-gradient(180deg, #111827, #0b1020);
    }

    .page{
      width:min(980px, 100%);
      background: linear-gradient(180deg, var(--paper), var(--paper2));
      border-radius:22px;
      box-shadow: 0 24px 70px var(--shadow);
      border: 1px solid rgba(255,255,255,0.12);
      overflow:hidden;
      position:relative;
    }

    /* subtle "paper grain" */
    .page::before{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(circle at 15% 20%, rgba(0,0,0,0.03), transparent 55%),
        radial-gradient(circle at 85% 75%, rgba(0,0,0,0.02), transparent 60%);
      mix-blend-mode:multiply;
      pointer-events:none;
      opacity:0.7;
    }

    header{
      position:relative;
      padding:22px 24px 14px 24px;
      border-bottom: 1px solid var(--line);
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:14px;
    }

    .head-left{
      display:flex;
      flex-direction:column;
      gap:6px;
    }

    .kicker{
      font-size:12px;
      letter-spacing:0.18em;
      text-transform:uppercase;
      color:var(--muted);
    }

    h1{
      margin:0;
      font-size:26px;
      line-height:1.1;
      letter-spacing:-0.02em;
    }

    .stamp{
      display:flex;
      align-items:center;
      gap:10px;
      padding:10px 12px;
      border-radius:16px;
      border:1px solid rgba(122,46,46,0.25);
      background: rgba(122,46,46,0.06);
      color: var(--seal);
      font-weight:700;
      font-size:13px;
      white-space:nowrap;
    }

    .wax{
      width:14px;
      height:14px;
      border-radius:50%;
      background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.45), transparent 55%),
                  var(--seal);
      box-shadow: 0 8px 18px rgba(122,46,46,0.25);
    }

    main{
      position:relative;
      padding:22px 24px 26px 24px;
      display:grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap:22px;
    }

    @media (max-width: 900px){
      main{grid-template-columns:1fr;}
    }

    .story{
      padding:18px 18px;
      border-radius:18px;
      border:1px solid rgba(31,41,55,0.12);
      background: rgba(255,255,255,0.35);
    }

    .story p{
      margin:0 0 12px 0;
      font-size:15.5px;
      line-height:1.75;
      color: var(--ink);
    }

    .story p:last-child{ margin-bottom:0; }

    .dropcap::first-letter{
      float:left;
      font-size:42px;
      line-height:0.95;
      padding-right:10px;
      padding-top:4px;
      color: var(--gold);
      font-weight:700;
    }

    .quote{
      margin:14px 0;
      padding:14px 14px;
      border-left:4px solid rgba(160,124,44,0.75);
      background: rgba(160,124,44,0.06);
      border-radius:14px;
      color:#111827;
      font-style:italic;
    }

    .console{
      padding:18px 18px;
      border-radius:18px;
      border:1px solid rgba(31,41,55,0.12);
      background: rgba(255,255,255,0.55);
      position:relative;
    }

    .console h2{
      margin:0 0 10px 0;
      font-size:15px;
      letter-spacing:0.12em;
      text-transform:uppercase;
      color: var(--muted);
    }

    .console .panel-title{
      margin:0 0 16px 0;
      font-size:18px;
      font-weight:700;
      color:#111827;
    }

    label{
      display:block;
      font-size:13px;
      color: var(--muted);
      margin-bottom:8px;
    }

    input{
      width:100%;
      padding:12px 12px;
      border-radius:14px;
      border:1px solid rgba(31,41,55,0.18);
      background: rgba(246,241,228,0.7);
      color: #111827;
      outline:none;
      font-size:15px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      letter-spacing:0.08em;
      transition: box-shadow 0.15s ease, border-color 0.15s ease;
    }

    input:focus{
      border-color: rgba(160,124,44,0.55);
      box-shadow: 0 0 0 4px rgba(160,124,44,0.16);
    }

    .row{
      display:flex;
      gap:10px;
      margin-top:12px;
    }

    button{
      flex:1;
      border:none;
      padding:11px 12px;
      border-radius:14px;
      cursor:pointer;
      font-weight:700;
      font-size:14px;
      background: linear-gradient(180deg, rgba(160,124,44,0.95), rgba(122,46,46,0.92));
      color:#fff;
      transition: transform 0.05s ease, filter 0.15s ease;
    }

    button:hover{ filter: brightness(1.03); }
    button:active{ transform: translateY(1px); }

    .secondary{
      background: rgba(31,41,55,0.08);
      color: #111827;
      border: 1px solid rgba(31,41,55,0.14);
      font-weight:700;
    }

    .msg{
      margin-top:14px;
      padding:12px 12px;
      border-radius:14px;
      border:1px solid rgba(31,41,55,0.14);
      background: rgba(246,241,228,0.65);
      font-size:14px;
      line-height:1.55;
      color:#111827;
    }

    code{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 13.5px;
      padding: 2px 7px;
      border-radius: 10px;
      background: rgba(31,41,55,0.08);
      border: 1px solid rgba(31,41,55,0.14);
    }

    footer{
      padding:14px 24px;
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size:12.5px;
      display:flex;
      justify-content:space-between;
      gap:10px;
      flex-wrap:wrap;
    }

    .tiny{
      font-style:italic;
    }
  </style>
</head>

<body>
  <div class="page">
    <header>
      <div class="head-left">
        <div class="kicker">Baker Street • Confidential</div>
        <h1>The Silent Machine</h1>
      </div>

      <div class="stamp">
        <span class="wax"></span>
        Case File: 221B
      </div>
    </header>

    <main>
      <section class="story">
        <p class="dropcap">
          London wore its fog like a cloak that night. At 221B Baker Street, a brass console sat on Holmes’ desk
          with all the charm of a locked diary and none of the courtesy.
        </p>

        <p>
          Watson approached it with optimism. Holmes approached it with certainty.
        </p>

        <div class="quote">
          “Some secrets aren’t hidden in vaults, Watson… they’re hidden behind obedience.”
        </div>

        <p>
          The device demanded a single offering — not coins, not words, not apologies — only the correct input.
          It would remain perfectly silent until it was addressed properly.
        </p>

        <div class="quote">
          “It’s a machine, Watson.<br>
          Speak to it.”
        </div>
      </section>

      <section class="console">
        <h2>Device Console</h2>
        <div class="panel-title">Enter your reply</div>

        <form method="POST">
          <label for="bin">Input</label>
          <input id="bin" name="bin" placeholder="..." autocomplete="off" required />

          <div class="row">
            <button type="submit">Submit</button>
            <button class="secondary" type="button" onclick="document.getElementById('bin').value=''">
              Clear
            </button>
          </div>
        </form>

        {% if message %}
          <div class="msg">{{ message|safe }}</div>
        {% endif %}
      </section>
    </main>

    <footer>
      <div class="tiny">“When you have eliminated the impossible, whatever remains…”</div>
      <div>CTF Interface • Localhost</div>
    </footer>
  </div>
</body>
</html>
"""

HTML_2 = """
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
            <div class="subtle">⚠️ A good detective counts till the <b>fifth mark</b>.</div>
        </div>

        <form method="POST">
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

@app.route("/challenge/1", methods=["GET", "POST"])
def challenge_one():
    if request.method == "POST":
        user_bin = request.form.get("bin", "").strip()

        if not user_bin:
            return render_template_string(HTML_1, message="The machine hears nothing.")

        if any(c not in "01" for c in user_bin):
            return render_template_string(HTML_1, message="The machine refuses to understand that.")

        if user_bin == CHALLENGE_1_ANSWER:
            return render_template_string(
                HTML_1,
                message=f"The machine finally speaks: <code>{FLAG_1}</code>"
            )

        return render_template_string(HTML_1, message="Silence. Try again.")

    return render_template_string(HTML_1, message=None)

@app.route("/challenge/2", methods=["GET", "POST"])


def challenge_two():
    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()

        if user_answer == CHALLENGE_2_ANSWER:
            return f"""
            <div style="font-family: Georgia, serif; text-align:center; padding:50px; background:#0b0b0b; color:#f5f5f5; height:100vh;">
                <h2 style="color:#d4af37;">✅ Correct! The case is solved.</h2>
                <p>Your flag is:</p>
                <code style="font-size:18px;">{FLAG_2}</code>
                <br><br>
                <a href="/challenge/2" style="color:#d4af37; text-decoration:none;">🔙 Back</a>
            </div>
            """

        return f"""
        <div style="font-family: Georgia, serif; text-align:center; padding:50px; background:#0b0b0b; color:#f5f5f5; height:100vh;">
            <h2 style="color:#ff4d4d;">❌ Incorrect!</h2>
            <a href="/challenge/2" style="color:#d4af37; text-decoration:none;">🔙 Try Again</a>
        </div>
        """

    return render_template_string(HTML_2)


@app.route("/")
def index():
    return redirect(url_for("challenge_one"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


