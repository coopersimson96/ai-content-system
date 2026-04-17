#!/usr/bin/env python3
"""
Batch import leads into Beehiiv via the Subscribe API.

Reads leads_ranked.csv (or any CSV you specify) and subscribes each lead.

Expected CSV columns:
    email            (required)
    first_name       (recommended)
    tier_label       (optional - e.g. "warm", "cold", "tier_1")
    resources        (optional - comma-separated list of things they've downloaded)
    resources_count  (optional)

If your CSV uses different column names, either rename them in the CSV or
update the column references in the import_leads() function below.

Usage:
    python3 import_leads.py              # dry run (count only)
    python3 import_leads.py --go         # actually import
    python3 import_leads.py --go --limit 10  # import first 10 only
"""

import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from beehiiv_api import BeehiivClient

CSV_PATH = Path(__file__).parent / "leads_ranked.csv"


def import_leads(dry_run=True, limit=None):
    client = BeehiivClient()

    if not CSV_PATH.exists():
        print(f"ERROR: Leads file not found at {CSV_PATH}")
        print("Place your leads CSV there (with columns: email, first_name, tier_label)")
        return

    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total = len(rows)
    if limit:
        rows = rows[:limit]

    print(f"{'DRY RUN - ' if dry_run else ''}Importing {len(rows)} of {total} leads into Beehiiv", flush=True)
    print(f"Publication: {client.pub_id}\n", flush=True)

    if dry_run:
        tiers = {}
        for row in rows:
            label = row.get("tier_label", "untagged")
            tiers[label] = tiers.get(label, 0) + 1
        for label, count in sorted(tiers.items()):
            print(f"  {label}: {count}")
        print(f"\nRun with --go to actually import.")
        return

    success = 0
    errors = 0
    skipped = 0

    for i, row in enumerate(rows):
        email = row["email"]
        first_name = row.get("first_name", "")
        tier = row.get("tier_label", "")

        if "@" in first_name:
            first_name = first_name.split("@")[0]

        try:
            custom_fields = []
            if tier:
                custom_fields.append({"name": "lead_tier", "value": tier})
            if row.get("resources_count"):
                custom_fields.append({"name": "resources_count", "value": row["resources_count"]})

            client.subscribe(
                email=email,
                first_name=first_name,
                utm_source="lead_import",
                utm_campaign=f"tier_{tier}" if tier else "import",
                double_opt="off",
                reactivate=True,
                custom_fields=custom_fields or None,
            )
            success += 1
        except Exception as e:
            err_msg = str(e)
            if "already exists" in err_msg.lower() or "already subscribed" in err_msg.lower():
                skipped += 1
            else:
                errors += 1
                if errors <= 5:
                    print(f"  ERROR [{i+1}] {email}: {err_msg}")

        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{len(rows)} (success={success}, skip={skipped}, err={errors})", flush=True)

        # Rate limit: Beehiiv API allows ~10 req/sec
        if (i + 1) % 10 == 0:
            time.sleep(1.1)

    print(f"\n{'='*50}")
    print(f"IMPORT COMPLETE")
    print(f"  Total processed: {len(rows)}")
    print(f"  Success: {success}")
    print(f"  Skipped (already exists): {skipped}")
    print(f"  Errors: {errors}")


if __name__ == "__main__":
    dry_run = "--go" not in sys.argv
    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx + 1])

    import_leads(dry_run=dry_run, limit=limit)
