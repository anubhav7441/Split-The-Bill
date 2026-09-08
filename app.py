import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from pydantic import ValidationError
from werkzeug.utils import secure_filename
from config import Config
from services.ocr_service import extract_bill_data, load_demo_bills, get_demo_bill
from services.split_engine import calculate_split
from models.bill_models import Bill

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.SESSION_FILE_DIR, exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route("/")
def index():
    demo_bills = load_demo_bills()
    return render_template("index.html", demo_bills=demo_bills)


@app.route("/demo/<bill_id>", methods=["GET", "POST"])
def demo_load(bill_id):
    demo = get_demo_bill(bill_id)
    bill_dict = demo.get("bill")
    if not bill_dict:
        flash("Demo bill not found.")
        return redirect(url_for("index"))

    try:
        bill = Bill(**bill_dict)
    except ValidationError as e:
        flash(f"Invalid demo bill data: {e}")
        return redirect(url_for("index"))

    session["bill_data"] = bill.model_dump()
    session["demo_bill_title"] = demo.get("title")
    session["demo_bill_icon"] = demo.get("icon", "🧾")
    session["demo_bill_image"] = demo.get("image_file")
    # Clear previous people/assignments when loading a new bill
    session.pop("people", None)
    session.pop("assignments", None)
    flash(f"Loaded demo bill: {demo.get('title')} ({demo.get('category')})")
    return redirect(url_for("review"))


@app.route("/upload", methods=["POST"])
def upload():
    if "bill_image" not in request.files:
        flash("No file selected.")
        return redirect(url_for("index"))

    file = request.files["bill_image"]

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload a PNG or JPG image.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    raw_data = extract_bill_data(
        filepath,
        api_key=Config.VISION_API_KEY,
        demo_mode=Config.DEMO_MODE,
        model=Config.VISION_MODEL,
    )

    try:
        bill = Bill(**raw_data)
    except ValidationError as e:
        flash(f"Extraction produced invalid data, please retry or check the image. Details: {e}")
        return redirect(url_for("index"))

    session["bill_data"] = bill.model_dump()
    # Clear previous people/assignments when a new bill is uploaded
    session.pop("people", None)
    session.pop("assignments", None)
    return redirect(url_for("review"))


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        bill_data = session.get("bill_data")
        if not bill_data:
            flash("No bill data found. Please upload a bill first.")
            return redirect(url_for("index"))
        return render_template("review.html", bill=bill_data)

    # POST: rebuild bill from corrected form data.
    # Collect ALL item indices actually present in the submitted form
    # (not a sequential 0,1,2... loop) so removing a middle row via JS doesn't
    # cause later rows to be silently dropped.
    form = request.form
    item_indices = sorted({
        int(m.group(1))
        for key in form.keys()
        for m in [re.match(r"^item_name_(\d+)$", key)]
        if m
    })

    items = []
    for idx in item_indices:
        name = form.get(f"item_name_{idx}", "").strip()
        if not name:
            continue  # row was cleared/removed
        try:
            items.append({
                "name": name,
                "quantity": float(form.get(f"item_quantity_{idx}", 0) or 0),
                "unit_price": float(form.get(f"item_unit_price_{idx}", 0) or 0),
                "line_total": float(form.get(f"item_line_total_{idx}", 0) or 0),
                "confidence": 1.0,  # user-confirmed
            })
        except ValueError:
            pass

    try:
        raw_data = {
            "items": items,
            "subtotal": float(form.get("subtotal", 0) or 0),
            "discount": float(form.get("discount", 0) or 0),
            "tax": float(form.get("tax", 0) or 0),
            "service_charge": float(form.get("service_charge", 0) or 0),
            "printed_total": float(form.get("printed_total", 0) or 0),
        }
    except ValueError:
        flash("Please enter valid numbers in all fields.")
        return render_template("review.html", bill=session.get("bill_data"))

    try:
        bill = Bill(**raw_data)
    except ValidationError as e:
        errors = [f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}" for err in e.errors()]
        fallback = raw_data | {
            "subtotal_confidence": 1, "discount_confidence": 1, "tax_confidence": 1,
            "service_charge_confidence": 1, "printed_total_confidence": 1,
            "items": [dict(i, confidence=1.0) for i in raw_data["items"]] or [
                {"name": "", "quantity": 1, "unit_price": 0, "line_total": 0, "confidence": 1.0}
            ]
        }
        return render_template("review.html", bill=fallback, errors=errors)

    session["bill_data"] = bill.model_dump()
    flash("Bill corrections saved.")
    return redirect(url_for("review"))


@app.route("/people", methods=["GET"])
def people():
    bill_data = session.get("bill_data")
    if not bill_data:
        flash("No bill data found. Please upload a bill first.")
        return redirect(url_for("index"))

    people_list = session.get("people", [])
    assignments = session.get("assignments", {})

    return render_template(
        "people.html",
        bill=bill_data,
        people=people_list,
        assignments=assignments,
    )


@app.route("/people/add", methods=["POST"])
def add_person():
    name = request.form.get("person_name", "").strip()
    if not name:
        flash("Person name cannot be empty.")
        return redirect(url_for("people"))

    people_list = session.get("people", [])
    new_id = (max(p["id"] for p in people_list) + 1) if people_list else 1
    people_list.append({"id": new_id, "name": name})
    session["people"] = people_list
    return redirect(url_for("people"))


@app.route("/people/remove", methods=["POST"])
def remove_person():
    try:
        person_id = int(request.form.get("person_id", ""))
    except (ValueError, TypeError):
        flash("Invalid person ID.")
        return redirect(url_for("people"))

    people_list = session.get("people", [])
    people_list = [p for p in people_list if p["id"] != person_id]
    session["people"] = people_list

    assignments = session.get("assignments", {})
    for item_idx, assigned_ids in assignments.items():
        assignments[item_idx] = [pid for pid in assigned_ids if pid != person_id]
    session["assignments"] = assignments

    return redirect(url_for("people"))


@app.route("/assign", methods=["POST"])
def assign():
    bill_data = session.get("bill_data")
    people_list = session.get("people", [])

    if not people_list:
        flash("Add at least one person before assigning items.")
        return redirect(url_for("people"))

    if not bill_data:
        flash("No bill data found. Please upload a bill first.")
        return redirect(url_for("index"))

    all_person_ids = [p["id"] for p in people_list]
    assignments = {}

    for idx in range(len(bill_data["items"])):
        mode = request.form.get(f"mode_{idx}", "individual")
        if mode == "everyone":
            assignments[str(idx)] = all_person_ids
        else:
            selected = request.form.getlist(f"item_{idx}_people")
            assignments[str(idx)] = [int(pid) for pid in selected]

    unassigned = [
        bill_data["items"][int(i)]["name"]
        for i, ids in assignments.items() if not ids
    ]
    if unassigned:
        flash(f"Warning: these items have no one assigned yet: {', '.join(unassigned)}")

    session["assignments"] = assignments
    flash("Assignments saved.")
    return redirect(url_for("people"))


@app.route("/calculate")
def calculate():
    bill_data = session.get("bill_data")
    people_list = session.get("people", [])
    assignments = session.get("assignments", {})

    if not bill_data:
        flash("No bill data found. Please upload a bill first.")
        return redirect(url_for("index"))
    if not people_list:
        flash("Add at least one person before calculating.")
        return redirect(url_for("people"))
    if not assignments:
        flash("Please assign items to people before calculating.")
        return redirect(url_for("people"))

    result = calculate_split(bill_data, people_list, assignments)
    session["result"] = result

    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
