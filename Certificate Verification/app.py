import hashlib
import os
import sqlite3
import uuid
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
import qrcode
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = "certificate_secret_key"

# Configuration for file directories
UPLOAD_FOLDER = "uploads"
QR_FOLDER = "qrcodes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["QR_FOLDER"] = QR_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# Initialize the blockchain object
blockchain = Blockchain()


def generate_hash(file_path):
    """Generates a SHA-256 hash of the uploaded file contents."""
    with open(file_path, "rb") as file:
        content = file.read()
    return hashlib.sha256(content).hexdigest()


@app.route("/qrcodes/<filename>")
def serve_qr(filename):
    """Safely serves generated QR code images from the backend to the frontend."""
    return send_from_directory(app.config["QR_FOLDER"], filename)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/")

        return "<h3>Invalid Login</h3>"

    return render_template("login.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        student_name = request.form["student_name"]
        reg_no = request.form["reg_no"]
        file = request.files["certificate"]

        # Save the uploaded certificate file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Generate unique certificate details
        certificate_hash = generate_hash(file_path)
        certificate_id = "CERT-" + str(uuid.uuid4())[:8]
        
        # DYNAMIC LINK: Automatically scales to local server OR deployed live cloud domain
        verification_url = f"{request.url_root}verify_id/{certificate_id}"

        # Generate and save the QR code image using the dynamic URL
        qr = qrcode.make(verification_url)
        qr_filename = f"{certificate_id}.png"
        qr_path = os.path.join(app.config["QR_FOLDER"], qr_filename)
        qr.save(qr_path)

        # Append data to the blockchain
        blockchain.create_block(certificate_hash)

        # Store details in the SQLite Database
        conn = sqlite3.connect("certificates.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO certificates
            VALUES (?, ?, ?, ?)
            """,
            (reg_no, student_name, certificate_hash, certificate_id),
        )
        conn.commit()
        conn.close()

        # Returns success screen displaying the newly generated QR Code
        return f"""
        <div class='container mt-5' style="text-align: center; font-family: Arial, sans-serif;">
            <h2 class='text-success' style='color: green;'>Certificate Stored Successfully</h2>
            
            <div style="margin: 25px 0;">
                <img src="/qrcodes/{qr_filename}" alt="Certificate QR Code" style="border: 1px solid #ddd; padding: 10px; border-radius: 8px; width: 220px;"/>
                <br>
                <small style="color: #666; display: block; margin-top: 5px;">Scan this QR code to instantly verify authenticity</small>
            </div>

            <div style="text-align: left; display: inline-block; width: 350px; background: #f9f9f9; padding: 15px; border-radius: 5px;">
                <p><b>Student Name:</b> {student_name}</p>
                <p><b>Register Number:</b> {reg_no}</p>
                <p><b>Certificate ID:</b> {certificate_id}</p>
                <p><b>Certificate Hash:</b> <span style="font-size: 12px; color: #555;">{certificate_hash[:20]}...</span></p>
            </div>
            <br><br>
            <a href="/" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">Go Home</a>
        </div>
        """

    return render_template("upload.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        reg_no = request.form["reg_no"]
        file = request.files["certificate"]

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"], "verify_" + file.filename
        )
        file.save(file_path)

        uploaded_hash = generate_hash(file_path)

        conn = sqlite3.connect("certificates.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_name,
                   certificate_hash,
                   certificate_id
            FROM certificates
            WHERE reg_no = ?
            """,
            (reg_no,),
        )
        record = cursor.fetchone()
        conn.close()

        if record:
            student_name = record[0]
            stored_hash = record[1]
            certificate_id = record[2]

            if uploaded_hash == stored_hash:
                return f"""
                <div class='container mt-5'>
                    <h2 class='text-success'>Certificate Verified Successfully</h2>
                    <p><b>Student Name:</b> {student_name}</p>
                    <p><b>Register Number:</b> {reg_no}</p>
                    <p><b>Certificate ID:</b> {certificate_id}</p>
                    <br>
                    <a href="/" class="btn btn-primary">Go Home</a>
                </div>
                """

        return """
        <div class='container mt-5'>
            <h2 class='text-danger'>Certificate Invalid or Tampered</h2>
            <br>
            <a href="/" class="btn btn-primary">Go Home</a>
        </div>
        """

    return render_template("verify.html")


@app.route("/verify_id/<certificate_id>")
def verify_by_id(certificate_id):
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT reg_no,
               student_name
        FROM certificates
        WHERE certificate_id = ?
        """,
        (certificate_id,),
    )
    record = cursor.fetchone()
    conn.close()

    if record:
        return f"""
        <div class='container mt-5'>
            <h2 class='text-success'>Certificate Verified Successfully</h2>
            <p><b>Student Name:</b> {record[1]}</p>
            <p><b>Register Number:</b> {record[0]}</p>
            <p><b>Certificate ID:</b> {certificate_id}</p>
            <h3 style='color:green'>Authentic Blockchain Certificate</h3>
            <a href="/" class="btn btn-primary">Go Home</a>
        </div>
        """

    return """
    <div class='container mt-5'>
        <h2 class='text-danger'>Certificate Not Found</h2>
        <a href="/" class="btn btn-primary">Go Home</a>
    </div>
    """


@app.route("/blockchain")
def show_blockchain():
    return render_template("blockchain.html", chain=blockchain.chain)


@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM certificates")
    total_certificates = cursor.fetchone()[0]
    conn.close()

    total_blocks = len(blockchain.chain)

    return render_template(
        "dashboard.html",
        total_certificates=total_certificates,
        total_blocks=total_blocks,
    )


if __name__ == "__main__":
    app.run(debug=True)