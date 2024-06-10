from Libraries import *
from validation import validate_existing_data, update_existing_data


app = Flask(__name__)
app.secret_key = 'supersecretkeY88'  # Needed for flashing messages

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xlsx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                df = pd.read_excel(file)
                df_cleaned, num_records_uncleaned = validate_existing_data(df)
                update_existing_data(df_cleaned)
                num_records_updated = len(df_cleaned)
                return redirect(url_for('uploaded_file', filename=filename, records_updated=num_records_updated, records_uncleaned=num_records_uncleaned))
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Only .xlsx files are allowed.')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    records_updated = request.args.get('records_updated', default=0, type=int)
    records_uncleaned = request.args.get('records_uncleaned', default=0, type=int)
    return render_template('uploaded.html', filename=filename, records_updated=records_updated, records_uncleaned=records_uncleaned)

@app.route('/download_uncleaned/<filename>')
def download_uncleaned_file(filename):
    return send_file(f'df_final_uncleaned.xlsx', as_attachment=True)

@app.route('/download_sample_file')
def download_sample_file():
    sample_data = {
        'Id': [],
        'Productname': [],
        'Barcode': [],
        'Company': [],
        'Brand': [],
        'SuperCategory': [],
        'Category': [],
        'SubCategory': [],
        'Segment': [],
        'Color': [],
        'Varient': [],
        'Measurement': [],
        'MeasurementType': [],
        'Packaging': [],
        'CPOffer': [],
        'CaseSize': [],
        'Local': [],
        'Sourcing': [],
        'TradePrice': [],
        'MRP': [],
        'Price': [],
        'DiscountedPrice': [],
        'StandardName': []
    }
    df_sample = pd.DataFrame(sample_data)

    sample_file_path = 'sample_file.xlsx'
    df_sample.to_excel(sample_file_path, index=False)

    return send_file(sample_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
