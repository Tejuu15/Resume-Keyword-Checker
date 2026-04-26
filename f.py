import re

from flask import Flask, render_template_string, request


app = Flask(__name__)


def extract_keywords(text):
        words = re.findall(r"\b\w+\b", text.lower())
        common_words = {"the", "and", "is", "in", "to", "of", "for", "a", "on"}
        return [word for word in words if word not in common_words]


def keyword_check(resume, job_desc):
        resume_keywords = set(extract_keywords(resume))
        job_keywords = set(extract_keywords(job_desc))

        matched = resume_keywords.intersection(job_keywords)
        missing = job_keywords - resume_keywords
        match_percent = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0

        return {
                "match_percent": round(match_percent, 2),
                "matched": sorted(matched),
                "missing": sorted(missing),
        }


PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Resume Keyword Checker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 24px; background: #f7f7fb; color: #1f2937; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); }
        h1 { margin-top: 0; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        textarea { width: 100%; min-height: 180px; padding: 10px; border: 1px solid #d1d5db; border-radius: 8px; resize: vertical; box-sizing: border-box; }
        button { margin-top: 16px; padding: 10px 16px; border: 0; border-radius: 8px; background: #2563eb; color: white; cursor: pointer; }
        .result { margin-top: 20px; padding: 14px; border: 1px solid #e5e7eb; border-radius: 8px; background: #fafafa; }
        .tags { margin-top: 8px; }
        .tags span { display: inline-block; margin: 4px 6px 0 0; padding: 5px 8px; border-radius: 999px; font-size: 13px; }
        .ok { background: #dcfce7; color: #166534; }
        .miss { background: #fee2e2; color: #991b1b; }
        @media (max-width: 700px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>Resume Keyword Checker</h1>
        <form method="post">
            <div class="grid">
                <div>
                    <label for="resume"><strong>Resume Text</strong></label>
                    <textarea id="resume" name="resume" placeholder="Paste resume text here...">{{ resume }}</textarea>
                </div>
                <div>
                    <label for="job_desc"><strong>Job Description</strong></label>
                    <textarea id="job_desc" name="job_desc" placeholder="Paste job description here...">{{ job_desc }}</textarea>
                </div>
            </div>
            <button type="submit">Check Keywords</button>
        </form>

        {% if result %}
            <div class="result">
                <h3>Match Percentage: {{ result.match_percent }}%</h3>
                <p><strong>Matched Keywords</strong></p>
                <div class="tags">
                    {% for word in result.matched %}<span class="ok">{{ word }}</span>{% else %}<span>No matched keywords.</span>{% endfor %}
                </div>
                <p><strong>Missing Keywords</strong></p>
                <div class="tags">
                    {% for word in result.missing %}<span class="miss">{{ word }}</span>{% else %}<span>No missing keywords.</span>{% endfor %}
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
        result = None
        resume = ""
        job_desc = ""

        if request.method == "POST":
                resume = request.form.get("resume", "")
                job_desc = request.form.get("job_desc", "")
                result = keyword_check(resume, job_desc)

        return render_template_string(PAGE, result=result, resume=resume, job_desc=job_desc)


if __name__ == "__main__":
        app.run(debug=True)