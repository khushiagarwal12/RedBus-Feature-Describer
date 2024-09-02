from flask import Flask, request, render_template, redirect
import google.generativeai as genai
from PIL import Image
import pytesseract
import io


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


api_key = "AIzaSyBN0hWC25Bx4cwX8VCtQLLjNpipEqPI17g" 
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Creating the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def extract_text_from_image(image_file):
    """
    Function to extract text from an image using pytesseract.
    """
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def identify_feature(text):
    """
    Function to identify which app feature the extracted text might be talking about.
    """
    features_info = {
        'Booking': {
            'Functionality': 'Allows users to book rides, reserve seats, or purchase tickets.',
            'User Interactions': 'Users can search for available buses or trains, select a ride, and confirm their booking.',
            'Edge Cases': 'No buses available, invalid seat selection, or booking errors.'
        },
        'Payment': {
            'Functionality': 'Handles financial transactions for bookings.',
            'User Interactions': 'Users enter payment details, apply discounts or offers, and complete the payment.',
            'Edge Cases': 'Payment failure, incorrect card details, or expired offers.'
        },
        'Cancelation': {
            'Functionality': 'Allows users to cancel bookings and request refunds.',
            'User Interactions': 'Users can cancel their bookings and request refunds through their account settings.',
            'Edge Cases': 'Cancellation deadlines, refund processing issues, or non-refundable bookings.'
        },
        'User Profile': {
            'Functionality': 'Manages user account information and preferences.',
            'User Interactions': 'Users can update personal information, review booking history, and manage settings.',
            'Edge Cases': 'Profile update failures, incorrect personal information, or data synchronization issues.'
        }
        
    }
    
    # Checking for feature based on extracted text
    for feature, info in features_info.items():
        if any(keyword.lower() in text.lower() for keyword in info['Functionality'].lower().split()):
            return info
    return {'Functionality': 'Feature not identified', 'User Interactions': 'N/A', 'Edge Cases': 'N/A'}

def describe_images(image_files, context):
    """
    Function to describe the uploaded images using the Google Gemini model.
    """
    descriptions = []
    for image_file in image_files:
        extracted_text = extract_text_from_image(image_file)
        if not extracted_text.strip():
            descriptions.append("Error: No text extracted from the image.")
            continue

        # Starting a chat session with the model
        try:
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(f"{context}\n{extracted_text}")
            description = response.text.strip().split('\n')  # Split into bullet points
        except Exception as e:
            description = [f"Error during model interaction: {e}"]

        # Identifying the app feature
        feature_info = identify_feature(extracted_text)
        descriptions.append({
            'description': description,
            'Functionality': feature_info['Functionality'].split('. '),  # Split into bullet points
            'User Interactions': feature_info['User Interactions'].split('. '),  # Split into bullet points
            'Edge Cases': feature_info['Edge Cases'].split('. ')  # Split into bullet points
        })
    
    return descriptions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'files' not in request.files or 'context' not in request.form:
            return redirect(request.url)
        files = request.files.getlist('files')
        context = request.form['context']
        if not files:
            return redirect(request.url)
        descriptions = describe_images(files, context)
        return render_template('result.html', descriptions=descriptions)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
