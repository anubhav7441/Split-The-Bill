import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.split_engine import calculate_split


def make_people(n):
    return [{"id": i + 1, "name": f"Person{i+1}"} for i in range(n)]


def test_individual_item_goes_to_one_person():
    bill = {
        "items": [{"name": "Coke", "line_total": 100}],
        "discount": 0, "tax": 0, "service_charge": 0, "printed_total": 100,
    }
    people = make_people(2)
    assignments = {"0": [1]}
    result = calculate_split(bill, people, assignments)
    p1 = next(b for b in result["breakdown"] if b["person_id"] == 1)
    p2 = next(b for b in result["breakdown"] if b["person_id"] == 2)
    assert p1["final_payable"] == 100
    assert p2["final_payable"] == 0


def test_shared_item_splits_equally_among_consumers():
    bill = {
        "items": [{"name": "Biryani", "line_total": 600}],
        "discount": 0, "tax": 0, "service_charge": 0, "printed_total": 600,
    }
    people = make_people(3)  # only 2 of 3 consume it
    assignments = {"0": [1, 2]}
    result = calculate_split(bill, people, assignments)
    p1 = next(b for b in result["breakdown"] if b["person_id"] == 1)
    p2 = next(b for b in result["breakdown"] if b["person_id"] == 2)
    p3 = next(b for b in result["breakdown"] if b["person_id"] == 3)
    assert p1["final_payable"] == 300
    assert p2["final_payable"] == 300
    assert p3["final_payable"] == 0


def test_tax_and_service_distributed_proportionally_not_equally():
    bill = {
        "items": [
            {"name": "Biryani", "line_total": 600},
            {"name": "Coke", "line_total": 100},
            {"name": "Dal", "line_total": 300},
        ],
        "discount": 0, "tax": 100, "service_charge": 100, "printed_total": 1200,
    }
    people = make_people(3)
    assignments = {"0": [1, 2], "1": [3], "2": [1, 2, 3]}
    result = calculate_split(bill, people, assignments)
    total_final = sum(b["final_payable"] for b in result["breakdown"])
    assert abs(total_final - result["calculated_total"]) < 0.01
    p1 = next(b for b in result["breakdown"] if b["person_id"] == 1)
    p3 = next(b for b in result["breakdown"] if b["person_id"] == 3)
    assert p1["tax_share"] != p3["tax_share"]


def test_printed_total_mismatch_detected():
    bill = {
        "items": [{"name": "Item", "line_total": 100}],
        "discount": 0, "tax": 0, "service_charge": 0, "printed_total": 500,
    }
    people = make_people(1)
    assignments = {"0": [1]}
    result = calculate_split(bill, people, assignments)
    assert result["total_mismatch"] is True
    assert result["mismatch_difference"] != 0


def test_no_naive_equal_division_of_total_bill():
    bill = {
        "items": [{"name": "Biryani", "line_total": 700}],
        "discount": 0, "tax": 0, "service_charge": 0, "printed_total": 700,
    }
    people = make_people(7)
    assignments = {"0": [1, 2]}
    result = calculate_split(bill, people, assignments)
    naive_share = 700 / 7
    p1 = next(b for b in result["breakdown"] if b["person_id"] == 1)
    p7 = next(b for b in result["breakdown"] if b["person_id"] == 7)
    assert p1["final_payable"] != naive_share
    assert p1["final_payable"] == 350
    assert p7["final_payable"] == 0
