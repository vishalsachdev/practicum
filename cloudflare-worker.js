/**
 * Cloudflare Worker - Reverse Proxy for illinihunt.org subdomains
 * Maps subdomains to bolt.host hosted sites
 *
 * AUTO-GENERATED from subdomains.json
 * Run: python3 generate-worker.py
 */

// SUBDOMAIN CONFIGURATION
const SUBDOMAIN_MAP = {
  "core-v2": "https://syncup-landing-page-fqzr.bolt.host",
  "dresscode-v1": "https://dresscode-virtual-wa-rxk0.bolt.host",
  "moneynova-v1": "https://moneyquest-email-lan-pgwx.bolt.host",
  "firstshares-v2": "https://first-shares-landing-160x.bolt.host",
  "longlink-v2": "https://longlink-couples-app-5cv0.bolt.host",
  "net-umbrella-v2": "https://net-umbrella-email-s-1cl7.bolt.host",
  "thesystem-v2": "https://bolt-gamified-habit-3qb3.bolt.host",
  "youngeru-v2": "https://youngeru-landing-pag-rkc6.bolt.host",
  "dresscode-v2": "https://dresscodev2-dlyd.bolt.host",
  "anchor-v1": "https://mental-wellness-plat-4vvr.bolt.host",
  "cashcreates-v1": "https://cash-creates-landing-c5qg.bolt.host",
  "core-v1": "https://syncup-student-produ-6rbz.bolt.host",
  "dormplate-v1": "https://dormplate-waitlist-l-j8sf.bolt.host",
  "finly-v1": "https://finly-college-budget-lu0g.bolt.host",
  "firstshares-v1": "https://first-shares-landing-dt74.bolt.host",
  "guidedgains-v1": "https://ai-fitness-planner-l-gjon.bolt.host",
  "longlink-v1": "https://longlink-app-landing-09cy.bolt.host",
  "mealscan-v1": "https://college-student-meal-89x7.bolt.host",
  "net-umbrella-v1": "https://friend-umbrella-high-vw36.bolt.host",
  "promptcad-v2": "https://thinkcad-ai-cad-land-vif1.bolt.host",
  "promptcad": "https://promptcad-landing-pa-342s.bolt.host",
  "thesystem-v1": "https://bolt-gamified-habit-yktz.bolt.host",
  "thinker-v1": "https://thinker-landing-page-ocn5.bolt.host",
  "tonematchai-v1": "https://tone-match-ai-app-la-btsw.bolt.host",
  "tonematchai-v2": "https://new-chat-nce2.bolt.host",
  "youngeru-v1": "https://youngeru-landing-pag-t1z3.bolt.host",
  "localoop": "https://localoop-mobile-even-vb7c.bolt.host",
  "longlink": "https://longlink-app-a7dy.bolt.host",
  "net-umbrella": "https://net-umbrella-friends-an16.bolt.host",
  "tonematchai": "https://ai-email-tone-matchi-ztwh.bolt.host",
  "moneynova": "https://moneynova-study-abro-kxw0.bolt.host",
  "thinker": "https://student-learning-app-yg75.bolt.host",
  "firstshares": "https://firstshares-scnv.bolt.host",
  "anchor": "https://anchor-ar-vr-wellnes-js3q.bolt.host",
  "fridgemate": "https://fridgemate-student-m-jdth.bolt.host",
  "core": "https://student-productivity-1ni6.bolt.host",
  "dormplate": "https://dormplate-complete-b-op4o.bolt.host",
  "dresscode": "https://dresscode-virtual-wa-rxk0.bolt.host",
  "guidedgains": "https://guided-gains-ai-fit.bolt.host",
  "youngeru": "https://youngeru-app-g0w6.bolt.host",
  "thesystem": "https://thesystem-gamma.vercel.app"
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

  // Let root domain pass through (don't intercept)
  // This allows illinihunt.org to be handled by its Vercel deployment
  if (isRootDomain) {
    return fetch(request);
  }

  // Check if subdomain is mapped
  const targetBase = SUBDOMAIN_MAP[subdomain];

  if (!targetBase) {
    return new Response(`Subdomain "${subdomain}" not configured\nAvailable: ${Object.keys(SUBDOMAIN_MAP).join(', ')}`, {
      status: 404,
      headers: { 'Content-Type': 'text/plain' }
    });
  }

  // Build target URL
  // targetBase can be either a full URL or a project ID (legacy)
  let targetUrl;
  if (targetBase.startsWith('http://') || targetBase.startsWith('https://')) {
    // Full URL format
    const baseUrl = new URL(targetBase);
    targetUrl = `${baseUrl.origin}${url.pathname}${url.search}`;
  } else {
    // Legacy project ID format (assume bolt.host)
    targetUrl = `https://${targetBase}.bolt.host${url.pathname}${url.search}`;
  }

  // Create new request to target
  const modifiedRequest = new Request(targetUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body,
    redirect: 'follow'
  });

  // Fetch from target
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
