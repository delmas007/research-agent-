from flask import Flask, request, jsonify, send_file, make_response
from aiagent.crew import Aiagent
from datetime import datetime
from flask_cors import CORS
from aiagent.tools.custom_tool import ExportMarkdownPDF
from urllib.parse import quote

app = Flask(__name__)
CORS(app, origins=['http://localhost:4200'])

@app.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()

    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Le champ "topic" est requis.'}), 400

    try:
        result = Aiagent().crew().kickoff(inputs={"topic": topic})
        return jsonify({'result': result.raw}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500\

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        topic = data.get('prompt')
        if not topic:
            return jsonify({'error': 'Le champ "prompt" est requis.'}), 400

        result = Aiagent().crew().kickoff(inputs={"topic": topic})

        pdf_io = ExportMarkdownPDF().run(result.raw)

        safe_topic = "".join(c for c in topic if c.isalnum() or c in ('_', '-')).replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_topic}.pdf"
        ascii_filename = quote(filename)

        response = make_response(send_file(
            pdf_io,
            as_attachment=True,
            mimetype='application/pdf',
            download_name=filename  # Flask ≥2.0
        ))
        response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{ascii_filename}"
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
