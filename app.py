from flask import Flask, render_template, send_file
import pandas as pd
from gpon_engine import parse_olt_output, get_summary
import io

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Load sample data
    with open('sample_olt_output.txt', 'r') as f:
        cli_data = f.read()
    
    # Parse + analyze
    df = parse_olt_output(cli_data)
    total, bad, online, health = get_summary(df)
    
    return render_template('dashboard.html', 
                           table=df.to_html(classes='table table-striped'),
                           total=total, 
                           bad=bad, 
                           online=online,
                           health=health)

@app.route('/download')
def download():
    with open('sample_olt_output.txt', 'r') as f:
        cli_data = f.read()
    
    df = parse_olt_output(cli_data)
    
    # Export to Excel in memory
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='ONU_Report')
    output.seek(0)
    
    return send_file(output, 
                     download_name='GPON_Report.xlsx',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
