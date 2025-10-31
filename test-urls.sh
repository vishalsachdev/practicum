#!/bin/bash

# Test all bolt.host URLs and report status

urls=(
    "https://syncup-landing-page-fqzr.bolt.host/"
    "https://dresscode-virtual-wa-rxk0.bolt.host/"
    "https://moneyquest-email-lan-pgwx.bolt.host/"
    "https://first-shares-landing-160x.bolt.host/"
    "https://longlink-couples-app-5cv0.bolt.host/"
    "https://net-umbrella-email-s-1cl7.bolt.host/"
    "https://bolt-gamified-habit-3qb3.bolt.host/"
    "https://youngeru-landing-pag-rkc6.bolt.host"
    "https://dresscodev2-dlyd.bolt.host/"
    "https://mental-wellness-plat-4vvr.bolt.host/"
    "https://cash-creates-landing-c5qg.bolt.host/"
    "https://syncup-student-produ-6rbz.bolt.host/"
    "https://dormplate-waitlist-l-j8sf.bolt.host/"
    "https://finly-college-budget-lu0g.bolt.host/"
    "https://first-shares-landing-dt74.bolt.host/"
    "https://ai-fitness-planner-l-gjon.bolt.host/"
    "https://longlink-app-landing-09cy.bolt.host/"
    "https://college-student-meal-89x7.bolt.host/"
    "https://friend-umbrella-high-vw36.bolt.host/"
    "https://thinkcad-ai-cad-land-vif1.bolt.host/"
    "https://promptcad-landing-pa-342s.bolt.host/"
    "https://bolt-gamified-habit-yktz.bolt.host/"
    "https://thinker-landing-page-ocn5.bolt.host/"
    "https://tone-match-ai-app-la-btsw.bolt.host/"
    "https://new-chat-nce2.bolt.host/"
    "https://youngeru-landing-pag-t1z3.bolt.host/"
)

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

echo "Testing bolt.host URLs..."
echo "=========================="
echo ""

working=()
broken=()

for i in "${!urls[@]}"; do
    url="${urls[$i]}"
    subdomain="${subdomains[$i]}"

    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")

    if [ "$status" -eq 200 ] || [ "$status" -eq 301 ] || [ "$status" -eq 302 ]; then
        echo "✅ $subdomain: $status - $url"
        working+=("$subdomain")
    else
        echo "❌ $subdomain: $status - $url"
        broken+=("$subdomain:$url")
    fi
done

echo ""
echo "=========================="
echo "Summary:"
echo "Working: ${#working[@]}"
echo "Broken: ${#broken[@]}"

if [ ${#broken[@]} -gt 0 ]; then
    echo ""
    echo "Broken URLs:"
    for item in "${broken[@]}"; do
        echo "  - $item"
    done
fi
