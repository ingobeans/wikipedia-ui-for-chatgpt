from flask import Flask, render_template, request, jsonify
import gpt, re, html

app = Flask(__name__)

def sanitize_and_format(text):
    #BEWARE: ChatGPT generated code, because apparently the bleach library and the MarkdownIT library don't behave well together
    sanitized_text = html.escape(text)
    formatted_text = sanitized_text.replace("\n\n","\n")
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_text)
    formatted_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_text)
    formatted_text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', formatted_text, flags=re.DOTALL)
    formatted_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', formatted_text)
    for i in range(6, 0, -1):
        pattern = '#' * i + ' (.*?)(?:$|\n)'
        replacement = f'<h{i}>\\1</h{i}>\n'
        formatted_text = re.sub(pattern, replacement, formatted_text)

    return formatted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_resp',methods=["POST"])
def get_resp():
    try:
        content = request.json
        print(content)
        success = True
        textRaw = gpt.get_resp(content["messages"])
    except Exception as e:
        textRaw = str(e)
        success = False
        
    #text = bleach.clean(textRaw)
    #text = md.render(src=text)
    
    text = sanitize_and_format(textRaw)
    return jsonify(contentRaw=textRaw,content=text,success=success)

if __name__ == '__main__':
    app.run(debug=True)
