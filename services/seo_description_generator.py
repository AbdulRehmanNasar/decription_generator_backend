from flask import request, jsonify
import pandas as pd
import traceback
from io import BytesIO
import base64
import concurrent.futures
from processors.row_processor import process_row
import openai

def handle_generate_seo_descriptions():
    print("Received request to /generate-seo-descriptions")

    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({"error": "No Excel file uploaded"}), 400

    file = request.files['file']
    print(f"File received: {file.filename}")

    try:
        df = pd.read_excel(file)
        print(f"Excel loaded with {len(df)} rows")
        
        # Check if the file is empty (no rows)
        if df.empty:
            print("Excel file is empty")
            return jsonify({"error": "The uploaded Excel file is empty"}), 400

        # Check for all missing required columns
        required_cols = ["URUNADI", "KATEGORILER", "SEO_SAYFAACIKLAMA"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            error_msg = f"Missing required columns: {', '.join(missing_cols)}"
            print(f"{error_msg}")
            return jsonify({"error": error_msg}), 400
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Failed to read Excel file: {str(e)}"}), 500

    try:
        try:
            from config import client
            client.models.list()
        except openai.AuthenticationError as auth_err:
            print(f"Invalid API key: {auth_err}")
            return jsonify({"error": "Failed to process file due to server configuration issue"}), 502

        print("Starting parallel processing of rows...")
        results = ["" for _ in range(len(df))]
        errors = ["" for _ in range(len(df))]

        def safe_process(args):
            idx, row = args
            try:
                desc = process_row((idx, row), df)
                return idx, desc, ""
            except RuntimeError as re:
                raise re
            except Exception as ex:
                error_msg = f"Error in row {idx}: {str(ex)}"
                print(f"{error_msg}")
                return idx, "", error_msg

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(safe_process, (idx, row)) for idx, row in df.iterrows()]
            try:
                for future in concurrent.futures.as_completed(futures):
                    idx, desc, err = future.result()
                    if desc:
                        print(f"Row {idx} processed. Description length: {len(desc)} chars")
                    results[idx] = desc
                    errors[idx] = err
            except RuntimeError as fatal_api_err:
                print(f"Fatal processing error: {fatal_api_err}")
                for future in futures:
                    future.cancel()
                traceback.print_exc()
                return jsonify({"error": "Failed to process file due to server configuration issue"}), 502

        df["SEO_SAYFAACIKLAMA"] = results

        print("Saving updated Excel to memory buffer...")
        output_buffer = BytesIO()
        df.to_excel(output_buffer, index=False)
        output_buffer.seek(0)

        print("Preparing response with updated file and errors")

        encoded_file = base64.b64encode(output_buffer.read()).decode('utf-8')

        response = {
            "file": encoded_file,
            "errors": [err for err in errors if err]
        }

        return jsonify(response)

    except Exception as e:
        print(f"Processing failed: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500