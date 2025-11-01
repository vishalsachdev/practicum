#!/bin/bash
# Bulk create DNS records for subdomains

SUBDOMAINS=(
    "localoop"
    "longlink"
    "net-umbrella"
    "tonematchai"
    "moneynova"
    "thinker"
    "firstshares"
    "anchor"
    "fridgemate"
    "core"
    "dormplate"
    "dresscode"
    "guidedgains"
    "youngeru"
    "thesystem"
)

echo "Creating DNS records for ${#SUBDOMAINS[@]} subdomains..."
echo ""

SUCCESS=0
FAILED=0

for subdomain in "${SUBDOMAINS[@]}"; do
    echo "Creating DNS record: ${subdomain}.illinihunt.org"

    if .github/scripts/manage-dns.py create "$subdomain" 2>&1 | grep -q "SUCCESS\|already exists"; then
        echo "  ✅ Success"
        ((SUCCESS++))
    else
        echo "  ❌ Failed"
        ((FAILED++))
    fi

    echo ""
done

echo "================================"
echo "Summary: ${SUCCESS} successful, ${FAILED} failed"
