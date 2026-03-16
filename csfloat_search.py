 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/csfloat_search.py b/csfloat_search.py
new file mode 100644
index 0000000000000000000000000000000000000000..88a0d8b34575fa6470bedb4259b8ca37b5a73c22
--- /dev/null
+++ b/csfloat_search.py
@@ -0,0 +1,131 @@
+#!/usr/bin/env python3
+"""Petit script CLI pour rechercher des items CS2 sur CSFloat.
+
+Usage:
+  python csfloat_search.py --query "AK-47 | Redline (Field-Tested)"
+"""
+
+from __future__ import annotations
+
+import argparse
+import json
+import os
+import sys
+import urllib.error
+import urllib.parse
+import urllib.request
+from typing import Any
+
+BASE_URL = "https://csfloat.com/api/v1/listings"
+
+
+def build_params(args: argparse.Namespace) -> dict[str, Any]:
+    params: dict[str, Any] = {
+        "limit": args.limit,
+        "page": args.page,
+        "sort_by": args.sort_by,
+        "order": args.order,
+    }
+
+    if args.query:
+        params["market_hash_name"] = args.query
+
+    if args.min_price is not None:
+        params["min_price"] = args.min_price
+
+    if args.max_price is not None:
+        params["max_price"] = args.max_price
+
+    if args.min_float is not None:
+        params["min_float"] = args.min_float
+
+    if args.max_float is not None:
+        params["max_float"] = args.max_float
+
+    return params
+
+
+def format_price(price_cents: int | None) -> str:
+    if price_cents is None:
+        return "N/A"
+    return f"${price_cents / 100:.2f}"
+
+
+def fetch_json(params: dict[str, Any], token: str | None) -> dict[str, Any]:
+    query = urllib.parse.urlencode(params)
+    url = f"{BASE_URL}?{query}"
+
+    headers = {"Accept": "application/json"}
+    if token:
+        headers["Authorization"] = token
+
+    request = urllib.request.Request(url, headers=headers, method="GET")
+    with urllib.request.urlopen(request, timeout=20) as response:
+        return json.loads(response.read().decode("utf-8"))
+
+
+def run(args: argparse.Namespace) -> int:
+    token = os.getenv("CSFLOAT_API_KEY")
+    params = build_params(args)
+
+    try:
+        payload = fetch_json(params, token)
+    except urllib.error.HTTPError as exc:
+        body = exc.read().decode("utf-8", errors="replace")
+        print(f"Erreur HTTP CSFloat: {exc}", file=sys.stderr)
+        if body:
+            print(body, file=sys.stderr)
+        return 1
+    except urllib.error.URLError as exc:
+        print(f"Erreur réseau: {exc}", file=sys.stderr)
+        return 1
+    except TimeoutError as exc:
+        print(f"Timeout: {exc}", file=sys.stderr)
+        return 1
+
+    listings = payload.get("data", [])
+
+    if not listings:
+        print("Aucun résultat.")
+        return 0
+
+    print(f"{len(listings)} résultat(s) trouvé(s):")
+    for item in listings:
+        name = item.get("item", {}).get("market_hash_name", "Unknown")
+        float_value = item.get("item", {}).get("float_value")
+        price = format_price(item.get("price"))
+        listing_id = item.get("id", "?")
+        print(f"- {name}")
+        print(f"  ID: {listing_id} | Prix: {price} | Float: {float_value}")
+
+    return 0
+
+
+def parse_args() -> argparse.Namespace:
+    parser = argparse.ArgumentParser(
+        description="Recherche des listings CS2 sur CSFloat",
+    )
+    parser.add_argument("--query", help="Nom exact (market_hash_name) de l'item")
+    parser.add_argument("--min-price", type=int, help="Prix minimum en cents")
+    parser.add_argument("--max-price", type=int, help="Prix maximum en cents")
+    parser.add_argument("--min-float", type=float, help="Float minimum")
+    parser.add_argument("--max-float", type=float, help="Float maximum")
+    parser.add_argument("--limit", type=int, default=10, help="Nombre de résultats")
+    parser.add_argument("--page", type=int, default=0, help="Page à récupérer")
+    parser.add_argument(
+        "--sort-by",
+        default="lowest_price",
+        choices=["lowest_price", "highest_price", "most_recent", "best_deal"],
+        help="Tri CSFloat",
+    )
+    parser.add_argument(
+        "--order",
+        default="asc",
+        choices=["asc", "desc"],
+        help="Ordre de tri",
+    )
+    return parser.parse_args()
+
+
+if __name__ == "__main__":
+    raise SystemExit(run(parse_args()))
 
EOF
)
