import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint to verify the service is running."""
    return jsonify({"status": "healthy"}), 200

@app.route("/generate", methods=["POST"])
def generate():
    """
    Generates property presentation slides based on input data.
    Expected JSON: { "propertyType": str, "location": str, "price": str/int }
    """
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({
                "error": "Invalid JSON",
                "message": "The request body must be a valid JSON object."
            }), 400

        # Validate required fields
        required_fields = ['propertyType', 'location', 'price']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": "Missing Required Fields",
                "message": f"Please provide: {', '.join(missing_fields)}"
            }), 400

        property_type = str(data['propertyType']).strip()
        location = str(data['location']).strip()
        price = str(data['price']).strip()

        # Input sanitization/validation
        if not all([property_type, location, price]):
            return jsonify({
                "error": "Validation Error",
                "message": "Fields cannot be empty."
            }), 400

        logger.info(f"Generating slides for {property_type} in {location}")

        slides = [
            {
                "id": 1,
                "title": "Executive Summary",
                "content": f"A premium {property_type} opportunity located in the heart of {location}, offered at ₹{price}."
            },
            {
                "id": 2,
                "title": "Market Dynamics",
                "content": f"The {location} real estate market is currently experiencing high demand for {property_type} assets, driven by infrastructure growth and limited supply."
            },
            {
                "id": 3,
                "title": "Investment Potential",
                "content": f"At the attractive price point of ₹{price}, this {property_type} represents a high-yield investment with strong projected capital appreciation in {location}."
            }
        ]

        return jsonify({
            "success": True,
            "data": {
                "property_details": {
                    "type": property_type,
                    "location": location,
                    "price": price
                },
                "slides": slides
            }
        }), 200

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server."
        }), 500

if __name__ == "__main__":
    # Standard production port is 5000 in this environment
    app.run(host="0.0.0.0", port=5000, debug=False)
