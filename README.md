# blockchain-certificate-verifier
An immutable Flask and Blockchain web application utilizing SHA-256 document hashing and dynamic QR codes to issue and securely verify authentic certificates.
# 🎓 Blockchain-Based Certificate Verification System

A secure, web-based certificate issuance and verification application built with **Flask** and an immutable **Blockchain** ledger. This system addresses the issue of credential forgery by extracting a unique cryptographic fingerprint (SHA-256 hash) from certificate documents, anchoring them to a data chain, and generating dynamic QR codes for instant, real-time authentication.

---

## 🚀 Key Features

* **Secure File Upload & Hashing:** Computes a unique **SHA-256 digital fingerprint** for every uploaded certificate file.
* **Immutable Blockchain Ledger:** Hooks certificate hashes directly into a cryptographic chain to ensure records cannot be altered, backdated, or deleted.
* **Relational Local Registry:** Stores student details, register numbers, and randomly generated unique Certificate IDs using an optimized **SQLite3** layer.
* **Dynamic QR Code Generation:** Automatically embeds live, domain-adaptive verification URLs inside a custom QR code image upon document processing.
* **Dual-Stream Verification:**
  1. **File-to-Ledger Matching:** Re-upload a certificate file to dynamically compare its live hash against the verified registry.
  2. **Instant QR Scanning:** Scan the generated QR code or navigate to the Certificate ID link to instantly fetch authentic student records.
* **Live Analytics Dashboard:** Displays critical platform metrics such as total certificates registered and the current block height of the chain.

---

## 🛠️ Technical Stack

* **Backend Engine:** Flask (Python)
* **Storage Engine:** SQLite3
* **Cryptographic Layer:** SHA-256 (`hashlib`)
* **Identifiers:** UUID v4 (`uuid`)
* **QR Automation:** `qrcode` & `Pillow` (PIL)
* **Frontend Design:** HTML5, CSS3, Bootstrap Framework

---

## 🔄 System Workflow

1. **Upload:** Authorized administrative staff logs into the portal and uploads a student's digital certificate document.
2. **Hash Processing:** The system processes the binary contents of the certificate and extracts its unique mathematical fingerprint.
3. **Block Commitment:** The certificate hash is committed to the local `Blockchain` object as a new block entry.
4. **Link Generation:** A unique `CERT-ID` is minted, the database writes the tracking record, and a live verification URL (`request.url_root`) is wrapped inside a downloadable QR code image.
5. **Verification:** Third parties (e.g., employers, institutions) scan the QR code to pull instant, validated integrity confirmations right from your secure server.

---

## ⚙️ Installation & Local Environment Setup

Follow these commands to clone, configure, and boot up the system locally on your machine:

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/blockchain-certificate-verifier.git](https://github.com/YOUR_USERNAME/blockchain-certificate-verifier.git)
cd blockchain-certificate-verifier
