from decimal import Decimal, ROUND_HALF_UP


def _round2(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def compute_item_shares(items, assignments, people):
    """
    Returns: dict person_id -> list of {name, share} for items they consumed,
    and dict person_id -> pre_tax_total (unrounded float).
    assignments: {str(item_index): [person_id, ...]}
    """
    person_items = {p["id"]: [] for p in people}
    person_pretax = {p["id"]: 0.0 for p in people}

    for idx, item in enumerate(items):
        assigned_ids = assignments.get(str(idx), [])
        if not assigned_ids:
            continue  # unassigned item contributes to no one (already warned earlier)
        share_per_person = item["line_total"] / len(assigned_ids)
        for pid in assigned_ids:
            if pid not in person_pretax:
                continue  # person may have been removed after assignment
            person_pretax[pid] += share_per_person
            person_items[pid].append({"name": item["name"], "share": share_per_person})

    return person_items, person_pretax


def calculate_split(bill, people, assignments):
    """
    bill: dict matching Bill pydantic model (already validated/corrected).
    people: [{"id": int, "name": str}, ...]
    assignments: {str(item_index): [person_id, ...]}

    Returns dict with per-person breakdown + reconciliation info.
    """
    items = bill["items"]
    person_items, person_pretax = compute_item_shares(items, assignments, people)

    total_pretax = sum(person_pretax.values())
    discount = bill.get("discount", 0) or 0
    tax = bill.get("tax", 0) or 0
    service_charge = bill.get("service_charge", 0) or 0

    breakdown = []
    running_total = 0.0

    person_list = list(people)
    for i, p in enumerate(person_list):
        pid = p["id"]
        pretax = person_pretax.get(pid, 0.0)
        proportion = (pretax / total_pretax) if total_pretax > 0 else 0

        discount_share = discount * proportion
        tax_share = tax * proportion
        service_share = service_charge * proportion

        final_payable = pretax - discount_share + tax_share + service_share

        breakdown.append({
            "person_id": pid,
            "name": p["name"],
            "items": person_items.get(pid, []),
            "pre_tax_subtotal": pretax,
            "discount_share": discount_share,
            "tax_share": tax_share,
            "service_share": service_share,
            "final_payable": final_payable,
        })
        running_total += final_payable

    # --- Rounding reconciliation ---
    calculated_total_unrounded = total_pretax - discount + tax + service_charge

    for b in breakdown:
        b["pre_tax_subtotal"] = _round2(b["pre_tax_subtotal"])
        b["discount_share"] = _round2(b["discount_share"])
        b["tax_share"] = _round2(b["tax_share"])
        b["service_share"] = _round2(b["service_share"])
        b["final_payable"] = _round2(b["final_payable"])
        for it in b["items"]:
            it["share"] = _round2(it["share"])

    rounded_sum = _round2(sum(b["final_payable"] for b in breakdown))
    calculated_total = _round2(calculated_total_unrounded)
    leftover = _round2(calculated_total - rounded_sum)

    if leftover != 0 and breakdown:
        largest = max(breakdown, key=lambda b: b["final_payable"])
        largest["final_payable"] = _round2(largest["final_payable"] + leftover)

    printed_total = bill.get("printed_total", 0) or 0
    mismatch_tolerance = 1.0  # ₹1 rounding tolerance
    total_mismatch = abs(calculated_total - printed_total) > mismatch_tolerance

    return {
        "breakdown": breakdown,
        "calculated_total": calculated_total,
        "printed_total": printed_total,
        "total_mismatch": total_mismatch,
        "mismatch_difference": _round2(calculated_total - printed_total),
        "num_people": len(people),
    }
