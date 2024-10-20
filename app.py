from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, request, jsonify
from datetime import datetime

# MongoDB connection URI
uri = "mongodb+srv://AlexMercher:onecompletecircle@cluster0.8gq9g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Using ServerApi class instead of a dictionary
client = MongoClient(uri, server_api=ServerApi('1', strict=True, deprecation_errors=True))

def get_client():
    return client

db = client["library"]

app = Flask(__name__)

@app.route("/borrow", methods=["POST"])
def borrow_book():
    try:
        data = request.json
        book_code = data.get("bookCode")
        book_name = data.get("bookName")
        designation = data.get("designation")
        usn = data.get("usn")

        borrowed_book = {
            "bookCode": book_code,
            "bookName": book_name,
            "designation": designation,
            "usn": usn,
            "borrowedAt": datetime.now().strftime("%Y-%m-%d"),
            "returnedAt": None
        }

        collection = db["borrowedBooks"]
        collection.insert_one(borrowed_book)

        return jsonify({"message": "Book borrowed successfully"}), 200

    except Exception as e:
        print(f"Error borrowing book: {e}")
        return jsonify({"error": "Error borrowing book"}), 500

@app.route("/borrowedList", methods=["GET"])
def get_borrowed_list():
    try:
        borrowed_collection = db["borrowedBooks"]
        borrowed_data = list(borrowed_collection.find())

        for item in borrowed_data:
            item["_id"] = str(item["_id"])

        return jsonify(borrowed_data), 200
    
    except Exception as e:
        print(f"Error fetching borrowed data: {e}")
        return jsonify({"error": "Error fetching borrowed data"}), 500

@app.route("/history", methods=["GET"])
def get_history():
    try:
        history_collection = db["history"]
        history_data = list(history_collection.find())

        for item in history_data:
            item["_id"] = str(item["_id"])

        return jsonify(history_data), 200

    except Exception as e:
        print(f"Error fetching history data: {e}")
        return jsonify({"error": "Error fetching history data"}), 500

@app.route("/return", methods=["POST"])
def return_book():
    try:
        data = request.json
        book_code = data.get("bookCode")
        usn = data.get("usn")
        return_date = datetime.now().strftime("%Y-%m-%d")

        borrowed_collection = db["borrowedBooks"]
        borrowed_book = borrowed_collection.find_one({
            "bookCode": book_code,
            "usn": usn,
            "returnedAt": None
        })

        if not borrowed_book:
            return jsonify({"error": "Book not found or already returned"}), 404

        borrowed_book["returnedAt"] = return_date

        history_collection = db["history"]
        history_collection.insert_one(borrowed_book)

        borrowed_collection.delete_one({"_id": borrowed_book["_id"]})

        return jsonify({"message": "Book returned successfully"}), 200
    
    except Exception as e:
        print(f"Error returning book: {e}")
        return jsonify({"error": "Error returning book"}), 500

if __name__ == "__main__":
    app.run(debug=True)
