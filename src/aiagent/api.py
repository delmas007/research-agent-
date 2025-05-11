from flask import Flask, request, jsonify, send_file
from aiagent.crew import Aiagent
from datetime import datetime
import os
from aiagent.tools.custom_tool import ExportMarkdownPDF

app = Flask(__name__)

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
        topic = data.get('topic')
        if not topic:
            return jsonify({'error': 'Le champ "topic" est requis.'}), 400

        result = Aiagent().crew().kickoff(inputs={"topic": topic})

        safe_topic = "".join(c for c in topic if c.isalnum() or c in ('_', '-')).replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_topic}_{timestamp}.pdf"

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)

        ExportMarkdownPDF().run(result.raw, output_path=output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
