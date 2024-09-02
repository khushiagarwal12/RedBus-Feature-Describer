from flask import Flask, request, render_template, redirect
import google.generativeai as genai
import io

# Attempt to import pytesseract and handle the ImportError
try:
    from PIL import Image
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except ImportError:
    pytesseract = None
    print("Warning: pytesseract is not installed. Text extraction from images will not be available.")

api_key = "YOUR_API_KEY"  # Please replace with your API key
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
    if pytesseract is None:
        return "Error: pytesseract is not installed. Text extraction is unavailable."
    
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error: Unable to process the image."

def identify_feature(text):
    """
    Function to identify which app feature the extracted text might be talking about.
    """
    features_info = {
        'Login': {
            'Functionality': 'Allows users to log into their accounts.',
            'User Interactions': 'Users enter their credentials and access their accounts.',
            'Edge Cases': 'Incorrect login details, account lockout, or password reset issues.'
        },
        'Registration': {
            'Functionality': 'Enables new users to create an account.',
            'User Interactions': 'Users provide their details to register and create a new account.',
            'Edge Cases': 'Duplicate account creation, invalid input details, or email verification issues.'
        },
        'Offers': {
            'Functionality': 'Provides special discounts and promotional offers.',
            'User Interactions': 'Users can view and apply offers during booking or payment.',
            'Edge Cases': 'Expired offers, invalid offer codes, or offer application errors.'
        },
        'Filters': {
            'Functionality': 'Allows users to filter search results based on various criteria.',
            'User Interactions': 'Users can select filters like price range, bus type, or departure time.',
            'Edge Cases': 'No results found with selected filters, filter conflicts, or slow response times.'
        },
        'Bus': {
            'Functionality': 'Displays information about available buses.',
            'User Interactions': 'Users can view bus details such as timings, amenities, and routes.',
            'Edge Cases': 'Bus information not available, outdated schedules, or incorrect bus details.'
        },
        'Information': {
            'Functionality': 'Provides general information about the service or system.',
            'User Interactions': 'Users can access FAQs, contact details, or service descriptions.',
            'Edge Cases': 'Incorrect or outdated information, access issues, or missing details.'
        },
        'Payment': {
            'Functionality': 'Handles financial transactions for bookings.',
            'User Interactions': 'Users enter payment details, apply discounts or offers, and complete the payment.',
            'Edge Cases': 'Payment failure, incorrect card details, or expired offers.'
        },
        'Bus Selection': {
            'Functionality': 'Allows users to choose a specific bus from available options.',
            'User Interactions': 'Users select a bus based on preferences like departure time, route, or amenities.',
            'Edge Cases': 'Bus selection errors, unavailable options, or conflicting schedules.'
        },
        'Seat Selection': {
            'Functionality': 'Enables users to choose their preferred seats.',
            'User Interactions': 'Users select seats based on availability and preferences.',
            'Edge Cases': 'Seat availability issues, conflicting seat selections, or booking errors.'
        },
        'Source': {
            'Functionality': 'Allows users to specify the starting point of their journey.',
            'User Interactions': 'Users enter or select their departure location.',
            'Edge Cases': 'Invalid source location, no matches found, or location input errors.'
        },
        'Destination': {
            'Functionality': 'Allows users to specify the end point of their journey.',
            'User Interactions': 'Users enter or select their destination location.',
            'Edge Cases': 'Invalid destination location, no matches found, or location input errors.'
        },
        'Date Selection': {
            'Functionality': 'Enables users to choose the date for their journey.',
            'User Interactions': 'Users select a date from a calendar or input it manually.',
            'Edge Cases': 'Invalid date selection, past dates, or date conflicts.'
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
