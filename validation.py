from connection import *
from Libraries import *

# logging.basicConfig(
#         # filename=os.getenv('LOG_FILE'),
#         filename='app.log',
#         filemode='a',
#         format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#         level=logging.INFO)

def get_connection_uat():
    return create_engine(uat_connection())

engine = get_connection_uat()

# Load master files
logging.info("Loading Master Files...")
df_master_categories = pd.read_excel('MASTER FILES\CAT_MD.xlsx')
df_master_companies = pd.read_excel('MASTER FILES\CB_MD.xlsx')
df_master_packaging = pd.read_excel('MASTER FILES\P_MD.xlsx')
df_master_measurement_types = pd.read_excel('MASTER FILES\MT_MD.xlsx')

# Validate SuperCategory, Category, SubCategory, Company, Brand, Packaging
def validate_cat_CB_Packaging(row):
    super_category = row['SuperCategory']
    category = row['Category']
    sub_category = row['SubCategory']
    company = row['Company']
    brand = row['Brand']
    packaging = row['Packaging']

    valid_category = df_master_categories[
        (df_master_categories['SuperCategory'] == super_category) &
        (df_master_categories['Category'] == category) &
        (df_master_categories['SubCategory'] == sub_category)
    ].shape[0] > 0

    valid_company = df_master_companies[
        (df_master_companies['Company'] == company) &
        (df_master_companies['Brand'] == brand)
    ].shape[0] > 0

    valid_packaging = df_master_packaging[
        (df_master_packaging['Packaging'] == packaging)
    ].shape[0] > 0

    return valid_category and valid_company and valid_packaging

# Validate Measurement and Measurement Type
def validate_measurement(row):
    measurement = row['Measurement']
    measurement_type = row['MeasurementType']
    if not measurement or not re.match(r'^[\d.]+$', str(measurement)):
        return False
    
    try:
        measurement_value = float(measurement)
    except ValueError:
        return False

    if measurement_type in ['UNIT']:
        return True
    elif measurement_type in ['ML', 'GM', 'UNITS']:
        return 2 <= measurement_value <= 1000
    elif measurement_type in ['LITRE', 'KG']:
        return 1 <= measurement_value <= 100
    else:
        return False

def validate_existing_data(df_excel):
    # Convert all string columns to uppercase
    df_excel = df_excel.map(lambda x: x.upper() if isinstance(x, str) else x)

    # Apply validations
    logging.info("Applying Validations...")
    valid_cat_and_CB_and_P = df_excel.apply(validate_cat_CB_Packaging, axis=1)
    valid_measurement = df_excel.apply(validate_measurement, axis=1)
    valid_varient_segment_standardname = df_excel.apply(lambda row: not (pd.isna(row['Varient']) or pd.isna(row['Segment']) or pd.isna(row['StandardName'])), axis=1)


    # Filter out rows that fail validation checks
    df_final_cleaned = df_excel[valid_cat_and_CB_and_P & valid_measurement & valid_varient_segment_standardname]
    df_final_uncleaned = df_excel[~(valid_cat_and_CB_and_P & valid_measurement & valid_varient_segment_standardname)]

    # Save cleaned SKUs to Excel file
    columns_to_keep = ['Id', 'Productname', 'Barcode',  'Company', 'Brand', 'SuperCategory', 'Category', 'SubCategory', 'Segment', 'Color', 'Varient', 'Measurement', 'MeasurementType', 'Packaging', 'CPOffer', 'CaseSize', 'Local', 'Sourcing', 'TradePrice', 'MRP', 'Price', 'DiscountedPrice', 'StandardName']
    df_final_cleaned = df_final_cleaned[columns_to_keep]
    # df_final_cleaned.to_excel('df_final_cleaned.xlsx', index=False)
    # df_final_uncleaned.to_excel('df_final_uncleaned.xlsx', index=False)
    # print(f"Number of uncleaned records: {len(df_final_uncleaned)}")
    return df_final_cleaned, len(df_final_uncleaned)

def update_existing_data(df_excel):
    with engine.connect() as conn:
        records_updated = 0

        for i, row in tqdm(df_excel.iterrows()):
            primary_key_value = row['Id']

            # Check if a record with the same primary key already exists
            sql_check = text(f"SELECT * FROM products_new WHERE Id = :Id")
            existing_record = conn.execute(sql_check, {'Id': primary_key_value}).fetchone()

            if existing_record:
                # If the record exists, update the values on the basis of ID and donot update Barcode
                update_dict = {col: row[col] for col in df_excel.columns if col != 'Barcode' and not pd.isna(row[col])}
                if update_dict:
                    sql_update = text(f"UPDATE products_new SET {', '.join([f'{col} = :{col}' for col in update_dict.keys()])} WHERE Id = :Id")
                    try:
                        conn.execute(sql_update, {**update_dict, 'Id': primary_key_value})
                        records_updated += 1
                    except Exception as e:
                        print(f"Error updating record with Id {primary_key_value}: {e}")

        conn.commit()  # Commit changes to the database
        print(f"{records_updated} records updated.")

