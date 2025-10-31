#!/bin/bash

# Test all illinihunt.org subdomains

subdomains=(
    "core-v2"
    "dresscode-v1"
    "moneynova-v1"
    "firstshares-v2"
    "longlink-v2"
    "net-umbrella-v2"
    "thesystem-v2"
    "youngeru-v2"
    "dresscode-v2"
    "anchor-v1"
    "cashcreates-v1"
    "core-v1"
    "dormplate-v1"
    "finly-v1"
    "firstshares-v1"
    "guidedgains-v1"
    "longlink-v1"
    "mealscan-v1"
    "net-umbrella-v1"
    "promptcad-v2"
    "promptcad"
    "thesystem-v1"
    "thinker-v1"
    "tonematchai-v1"
    "tonematchai-v2"
    "youngeru-v1"
)

echo "Testing illinihunt.org subdomains..."
echo "===================================="
echo ""

working=()
broken=()

for subdomain in "${subdomains[@]}"; do
    url="https://${subdomain}.illinihunt.org"

    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")

    if [ "$status" -eq 200 ] || [ "$status" -eq 301 ] || [ "$status" -eq 302 ]; then
        echo "✅ $subdomain: $status"
        working+=("$subdomain")
    else
        echo "❌ $subdomain: $status"
        broken+=("$subdomain")
    fi
done

echo ""
echo "===================================="
echo "Summary:"
echo "Working: ${#working[@]}"
echo "Broken: ${#broken[@]}"

if [ ${#broken[@]} -gt 0 ]; then
    echo ""
    echo "Broken subdomains:"
    for subdomain in "${broken[@]}"; do
        echo "  - ${subdomain}.illinihunt.org"
    done
fi
