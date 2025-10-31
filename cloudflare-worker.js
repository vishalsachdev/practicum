/**
 * Cloudflare Worker - Reverse Proxy for illinihunt.org subdomains
 * Maps subdomains to bolt.host hosted sites
 *
 * AUTO-GENERATED from subdomains.json
 * Run: python3 generate-worker.py
 */

// SUBDOMAIN CONFIGURATION
const SUBDOMAIN_MAP = {
  "core-v2": "syncup-landing-page-fqzr",
  "dresscode-v1": "dresscode-virtual-wa-rxk0",
  "moneynova-v1": "moneyquest-email-lan-pgwx",
  "firstshares-v2": "first-shares-landing-160x",
  "longlink-v2": "longlink-couples-app-5cv0",
  "net-umbrella-v2": "net-umbrella-email-s-1cl7",
  "thesystem-v2": "bolt-gamified-habit-3qb3",
  "youngeru-v2": "youngeru-landing-pag-rkc6",
  "dresscode-v2": "dresscodev2-dlyd",
  "anchor-v1": "mental-wellness-plat-4vvr",
  "cashcreates-v1": "cash-creates-landing-c5qg",
  "core-v1": "syncup-student-produ-6rbz",
  "dormplate-v1": "dormplate-waitlist-l-j8sf",
  "finly-v1": "finly-college-budget-lu0g",
  "firstshares-v1": "first-shares-landing-dt74",
  "guidedgains-v1": "ai-fitness-planner-l-gjon",
  "longlink-v1": "longlink-app-landing-09cy",
  "mealscan-v1": "college-student-meal-89x7",
  "net-umbrella-v1": "friend-umbrella-high-vw36",
  "promptcad-v2": "thinkcad-ai-cad-land-vif1",
  "promptcad": "promptcad-landing-pa-342s",
  "thesystem-v1": "bolt-gamified-habit-yktz",
  "thinker-v1": "thinker-landing-page-ocn5",
  "tonematchai-v1": "tone-match-ai-app-la-btsw",
  "tonematchai-v2": "new-chat-nce2",
  "youngeru-v1": "youngeru-landing-pag-t1z3"
};

/**
 * Main request handler
 */
async function handleRequest(request) {
  const url = new URL(request.url);
  const hostname = url.hostname;

  // Extract subdomain from hostname
  const subdomain = hostname.split('.')[0];
  const isRootDomain = hostname === 'illinihunt.org' || hostname === 'www.illinihunt.org';

  // Log for debugging
  console.log(`Request: ${hostname} -> Subdomain: ${subdomain}`);

  // Handle root domain and www
  if (isRootDomain) {
    return new Response('illinihunt.org - Subdomain proxy active\nConfigured subdomains: ' + Object.keys(SUBDOMAIN_MAP).join(', '), {
      status: 200,
      headers: { 'Content-Type': 'text/plain' }
    });
  }

  // Check if subdomain is mapped
  const boltProjectId = SUBDOMAIN_MAP[subdomain];

  if (!boltProjectId) {
    return new Response(`Subdomain "${subdomain}" not configured\nAvailable: ${Object.keys(SUBDOMAIN_MAP).join(', ')}`, {
      status: 404,
      headers: { 'Content-Type': 'text/plain' }
    });
  }

  // Build target URL
  const targetUrl = `https://${boltProjectId}.bolt.host${url.pathname}${url.search}`;

  // Create new request to bolt.host
  const modifiedRequest = new Request(targetUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body,
    redirect: 'follow'
  });

  // Fetch from bolt.host
  const response = await fetch(modifiedRequest);

  // Create response with modified headers
  const modifiedResponse = new Response(response.body, response);

  // Update headers for proper proxying
  modifiedResponse.headers.set('Access-Control-Allow-Origin', '*');
  modifiedResponse.headers.delete('X-Frame-Options');

  return modifiedResponse;
}

/**
 * Cloudflare Worker entry point
 */
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});
