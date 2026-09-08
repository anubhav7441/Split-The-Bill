# 🧾 Split the Bill

> **Upload a bill. Review it. Assign items. Split it fairly.**

**Split the Bill** is a smart bill-splitting web application that extracts items and prices from a restaurant bill photograph, allows users to assign items to individuals or groups, and calculates accurate individual shares including GST/taxes, service charges, discounts, and shared-item costs.

---

## ✨ Features

### 📸 Bill Photo Extraction
Upload a photograph of a restaurant bill and extract important information such as:

- Item names
- Quantities
- Unit prices
- Line totals
- Subtotal
- Discounts
- GST / Taxes
- Service charges
- Final / printed total

### 🔎 Structured Bill Data

Extracted information is converted into structured data using **Pydantic**, making the bill easier to validate, edit, and process reliably.

### 👥 Smart Item Assignment

Every item can be assigned to:

- 👤 One person
- 👥 Multiple people
- 👨‍👩‍👧‍👦 Everyone

For example:

```text
Biryani → Person 1 + Person 2
Coke    → Person 3
Dal     → Everyone

⚖️ Fair Shared-Item Splitting

Shared items are divided according to the people who actually consumed them instead of simply dividing the entire bill by the number of people.

💰 Proportional GST & Service Charge

GST/tax and service charges are distributed proportionally according to each person's pre-tax consumption.

For example:
Person A → ₹500 consumption
Person B → ₹300 consumption
Person C → ₹200 consumption

Total → ₹1,000
GST   → ₹50

GST distribution:

Person A → 50% → ₹25
Person B → 30% → ₹15
Person C → 20% → ₹10

This ensures that the final split is based on actual consumption.

🎯 Human-in-the-Loop Review

OCR and automated extraction are not blindly trusted.

Before any bill calculation:

Extract bill information
Show confidence information
Allow the user to review the data
Allow the user to correct mistakes
Perform calculations using the corrected values
⚠️ Bill Total Validation

The application compares the calculated bill total with the printed bill total.

If they don't match, the system displays a warning instead of silently trusting the printed value.

Example:

⚠️ TOTAL MISMATCH

Calculated Total: ₹1,245.00
Printed Total:    ₹1,265.00
Difference:       ₹20.00
📊 Detailed Individual Breakdown

Each person receives a complete breakdown of their bill.

Example:

Person 1

Biryani              ₹300.00
Coke                   ₹80.00
Shared Dal             ₹75.00
--------------------------------
Pre-tax share         ₹455.00
GST                    ₹22.75
Service Charge         ₹45.50
Discount               -₹10.00
--------------------------------
FINAL PAYABLE         ₹513.25


🏗️ How It Works
             📸 BILL PHOTO
                   │
                   ▼
          🔍 OCR / EXTRACTION
                   │
                   ▼
          📦 STRUCTURED DATA
             (Pydantic)
                   │
                   ▼
          🎯 CONFIDENCE CHECK
                   │
                   ▼
            🔎 REVIEW & EDIT
                   │
                   ▼
              👥 ADD PEOPLE
                   │
                   ▼
             🍽️ ASSIGN ITEMS
                   │
                   ▼
          🧮 CALCULATE SHARES
                   │
                   ▼
       ⚖️ PROPORTIONAL TAX /
          SERVICE CHARGE
                   │
                   ▼
          📊 FINAL BREAKDOWN


🛠️ Tech Stack

Component	Technology
Backend	Python
Web Framework	Flask
Frontend	HTML5, CSS3, JavaScript
Data Validation	Pydantic
OCR	OCR-based text extraction
Image Processing	Python image processing
Storage	Lightweight local storage
Version Control	Git & GitHub
