# Real-Time Crowd/Busyness Data for Riyadh Places — Research

**Date:** 2026-02-07
**Scope:** All methods to get live or near-live crowd data for restaurants, cafes, and places in Riyadh

---

## Table of Contents
1. [Google Maps Popular Times](#1-google-maps-popular-times)
2. [Google Places API (Official)](#2-google-places-api-official)
3. [Third-Party Scraping Services](#3-third-party-scraping-services)
4. [BestTime.app](#4-besttimeapp)
5. [Foursquare/Swarm API](#5-foursquareswarm-api)
6. [Social Media Signals](#6-social-media-signals)
7. [SafeGraph / Placer.ai](#7-safegraph--placerai)
8. [Waze / Traffic Data](#8-waze--traffic-data)
9. [User-Generated / Crowdsourced](#9-user-generated--crowdsourced)
10. [Telecom Data (STC/Zain/Mobily)](#10-telecom-data-stczainmobily)
11. [⭐ RECOMMENDED APPROACH](#-recommended-approach)

---

## 1. Google Maps Popular Times

### How It Works
Google calculates "Popular Times" from **aggregated, anonymized Location History data** from users who have opted into Google Location History. This data feeds two features:
- **Popular Times (Historical):** Average busyness by hour/day over recent weeks
- **Live Busyness:** Real-time deviation from the historical average (shown as "Live" on Google Maps)

Google uses differential privacy to ensure individual users can't be identified.

### Is There an Official API?
**NO.** As of 2026, Google does **NOT** expose Popular Times or Live Busyness data through any official API (Places API, Maps API, etc.). There is a long-standing [feature request on Google's Issue Tracker](https://issuetracker.google.com/issues/35827350) but it remains unaddressed.

**Key quote from Stack Overflow (confirmed 2025):**
> "It's not currently possible to get popular or busy times information from Google's Place API."

### Third-Party Scrapers
Since Google doesn't offer an API, several tools scrape this data:

#### a) `populartimes` Python library
- **GitHub:** [m-wrzr/populartimes](https://github.com/m-wrzr/populartimes)
- Gets **historical** Popular Times data only (not live)
- Requires a Google Maps API key (for Places API geocoding)
- Scrapes Google Maps HTML for popular times data
- **Free** (uses your own API key for geocoding only)

#### b) `LivePopularTimes` Python library
- **GitHub:** [GrocerCheck/LivePopularTimes](https://github.com/GrocerCheck/LivePopularTimes)
- Extension of `populartimes` that adds **live/current busyness**
- Scrapes Google Maps search results to get `current_popularity`
- Works by formatted address (no API call) or by Place ID (API call)
- **Returns:** `current_popularity` (0-100), `populartimes` by hour/day
- **Free** (scraping), but requires Google API key for place lookups
- **Risk:** Scraping violates Google ToS; may break if Google changes HTML

#### c) `gmaps_popular_times_scraper`
- **GitHub:** [philshem/gmaps_popular_times_scraper](https://github.com/philshem/gmaps_popular_times_scraper)
- Direct scraper for Google Maps popular times
- Less maintained than LivePopularTimes

### Legal Considerations
⚠️ **Google Maps Platform Terms of Service explicitly prohibit scraping:**
> "Customer will not export, extract, or otherwise scrape Google Maps Content for use outside the Services."

**Risks:**
- Account suspension/ban if detected
- Potential legal action (though rare for small-scale)
- Data may be inaccurate if Google changes format
- Rate limiting / CAPTCHAs

**Practical reality:** Many apps use scraping services (via intermediaries like SerpAPI/Outscraper) that handle the compliance gray area. For a small Riyadh app (<300 places), risk is low but non-zero.

### Availability in Saudi Arabia
✅ Popular Times data exists for many Riyadh venues (restaurants, malls, cafes). Not all venues have it — requires sufficient Google user foot traffic.

### Summary
| Aspect | Details |
|--------|---------|
| **Official API** | ❌ Not available |
| **Historical data** | ✅ Via scrapers (populartimes, LivePopularTimes) |
| **Live data** | ✅ Via LivePopularTimes or scraping services |
| **Cost** | Free (open-source scrapers) or $50-100/mo (SerpAPI) |
| **Saudi coverage** | Good for popular venues |
| **Legal risk** | Medium (violates Google ToS) |
| **Implementation** | Easy (Python libraries) |
| **Accuracy** | High (Google's own data) |

---

## 2. Google Places API (Official)

### What Crowd/Busyness Data Does It Provide?
The official Google Places API (New/v2) provides detailed place information but **does NOT include Popular Times or busyness data** in any field.

**Available fields include:** address, businessStatus, ratings, reviews, openingHours, photos, priceLevel, etc.

**NOT available:** popular_times, current_busyness, live_crowd_level, foot_traffic.

The only tangentially related field is `currentOpeningHours` which tells you if a place is currently open — but nothing about how busy it is.

### Cost for Riyadh-Scale (300+ places)
If we used Places API for other data (not busyness):
- **Place Details (Essentials):** ~$5 per 1,000 calls
- **Place Details (Pro):** ~$10 per 1,000 calls  
- **Place Details (Enterprise):** ~$20 per 1,000 calls
- **$200/month free credit** from Google Cloud
- For 300 places refreshed 4x/day = 36,000 calls/month ≈ **$180-720/month** depending on tier
- With free credit: could be **free** at Essentials tier

### How to Implement
```python
# Google Places API (New) - Place Details
import requests

url = f"https://places.googleapis.com/v1/places/{place_id}"
headers = {
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "displayName,rating,currentOpeningHours,userRatingCount"
}
response = requests.get(url, headers=headers)
```

### Summary
| Aspect | Details |
|--------|---------|
| **Busyness data** | ❌ Not available |
| **Useful for** | Place details, ratings, hours, photos |
| **Cost** | $200 free credit/month covers ~40K calls |
| **Saudi coverage** | Excellent |
| **Legal** | ✅ Fully legal/official |

---

## 3. Third-Party Scraping Services

### a) SerpAPI (Google Maps API)
- **What:** Managed scraping service for Google search results including Maps
- **Popular Times:** ✅ Returns `popular_times.graph_results` with `busyness_score` (0-100) per hour/day
- **Live data:** ✅ Returns current busyness if available
- **Pricing:**
  - Free: 100 searches/month
  - Developer: $50/month (5,000 searches)
  - Business: $130/month (15,000 searches)
  - Enterprise: from $3,750/month
- **For 300 places:** 300 place lookups/day × 30 = 9,000/month → **$130/month** (Business plan)
- **Saudi coverage:** ✅ Works for Riyadh places
- **Legal:** SerpAPI handles scraping; they claim legal compliance via "accessing publicly available data"
- **Implementation:** Simple REST API

```python
from serpapi import SerpApiClient

result = SerpApiClient({
    "engine": "google_maps",
    "place_id": "ChIJ...",
    "api_key": SERPAPI_KEY
}).get_dict()

popular_times = result["place_results"]["popular_times"]
```

### b) Outscraper
- **What:** Google Maps scraper with API
- **Popular Times:** ✅ Including live status (e.g., "little busy")
- **Pricing:**
  - Free: 500 records/month
  - Paid: $3 per 1,000 records
- **For 300 places:** 300 × 30 = 9,000/month → **~$27/month**
- **Very cost-effective** for our use case
- **Live data:** Only works for individual place searches (not bulk)

### c) DataForSEO
- **SERP API with Google Maps data**
- **Pricing:** From $0.0006 per request
- **For 300 places daily:** 9,000/month × $0.0006 = **~$5.40/month** (cheapest!)

### Summary
| Service | Popular Times | Live Data | Cost (300 places) | Ease |
|---------|--------------|-----------|-------------------|------|
| SerpAPI | ✅ | ✅ | ~$130/mo | Easy |
| Outscraper | ✅ | ✅ (limited) | ~$27/mo | Easy |
| DataForSEO | ✅ | Unclear | ~$5/mo | Easy |

---

## 4. BestTime.app

### How It Works
BestTime.app provides **foot traffic forecasts** for public venues worldwide. It:
- Aggregates data from multiple sources (GPS, Wi-Fi, etc.)
- Provides hourly forecasts for each day of the week
- Identifies peak hours, quiet hours, surge patterns
- Values displayed as 0-100% relative to weekly peak

### Saudi Arabia Coverage
✅ **BestTime explicitly covers Saudi Arabia and Riyadh.** They have dedicated pages for:
- Riyadh restaurants
- Riyadh cafes
- Riyadh parks/nature
- Various venue types

### Data Available
- **Forecast (historical patterns):** ✅ Hourly busyness per day of week
- **Live data:** ✅ Available on Pro plan (costs more credits)
- **Dwell time:** How long people typically stay
- **Peak/quiet analysis:** Automated detection of busy/quiet periods
- **Venue search/filter:** Search venues by busyness level, time, type

### Pricing
| Plan | Monthly | Per Credit | Notes |
|------|---------|------------|-------|
| **Starter** | $29 min | $0.04-0.06 | No live data, no CDN caching |
| **Pro (Metered)** | $99 + usage | $0.009 | Live data included, CDN caching |
| **Enterprise** | $2,000+ | Custom | SLA, unlimited, dedicated server |

**Credit costs for 300 places:**
- Forecast by filter (10 venues): 1 credit → 30 credits for 300 venues
- Forecast by name: 2 credits each → 600 credits for 300 venues
- Live data: 1 credit each → 300 credits per refresh
- Weekly refresh forecast: ~$5-18/week on Pro
- Daily live data (4x): 1,200 credits/day × 30 = 36,000/month × $0.009 = **~$324/month**
- **Just forecasts (no live):** Much cheaper — ~$30-50/month on Pro

### Implementation
```bash
# Get foot traffic forecast for a venue
curl -X POST "https://besttime.app/api/v1/forecasts" \
  -d '{"api_key_private": "KEY", "venue_name": "Cafe Name", "venue_address": "Riyadh, Saudi Arabia"}'
```

### Summary
| Aspect | Details |
|--------|---------|
| **Forecast data** | ✅ Good quality hourly patterns |
| **Live data** | ✅ Available (expensive) |
| **Saudi coverage** | ✅ Explicitly supported |
| **Cost (forecasts only)** | ~$30-50/month |
| **Cost (with live)** | ~$300+/month |
| **Accuracy** | Good for patterns, less accurate for real-time |
| **Implementation** | Easy (REST API) |
| **Legal** | ✅ Fully legal commercial service |

---

## 5. Foursquare/Swarm API

### What's Available
Foursquare provides:
- **Places API:** POI database with 100M+ places globally
- **Foot traffic data:** Available via enterprise partnerships (not self-serve)
- **Check-in data:** Historical via V2 API (free for some endpoints)

### Saudi Arabia Coverage
- Foursquare has decent POI data for Saudi Arabia
- Check-in culture is not as strong in KSA as in the US/Europe
- Foot traffic data quality for Saudi may be limited

### Pricing
- **V2 endpoints (checkins, tips):** Free
- **V3 Places API:** $200 free credit/month, then pay-as-you-go
  - Pro endpoints: Volume-based pricing
  - Premium endpoints (tips, photos): Higher cost
  - $18.75 CPM for newer accounts

### Busyness Data Specifically
⚠️ Foursquare does NOT provide real-time busyness or popular times via their self-serve API. Their foot traffic data (Foursquare Visits, Foursquare Attribution) is an **enterprise product** requiring sales contact and likely $10K+/month.

### Summary
| Aspect | Details |
|--------|---------|
| **Real-time busyness** | ❌ Not available (self-serve) |
| **Foot traffic** | Enterprise only ($10K+/month) |
| **Check-in data** | Limited use for busyness |
| **Saudi coverage** | Moderate |
| **Practical for us** | ❌ Not cost-effective |

---

## 6. Social Media Signals

### Instagram Location Tags
- Instagram Graph API does NOT expose location-based post counts or activity
- Third-party scrapers (Apify, HikerAPI) can scrape location pages
- Could theoretically count recent posts tagged at a location as a "busyness" proxy
- **Problems:**
  - Instagram aggressively blocks scrapers
  - Post count ≠ current busyness (people post hours/days later)
  - Very noisy signal
  - Against Instagram ToS
  - Apify Instagram Location Scraper: ~$5/1000 results

### Snapchat/Snap Map
- Snap Map shows heat maps of activity
- **No public API**
- Cannot be programmatically accessed
- Snapchat is hugely popular in Saudi Arabia — data would be valuable if accessible

### X/Twitter
- Twitter/X API v2 can search for location-tagged tweets
- Could search for place mentions + sentiment
- **Problems:**
  - Very few tweets are location-tagged
  - Low signal density for individual restaurants
  - X API Basic: $100/month for 10K tweets/month
  - Not real-time busyness indicator

### TikTok
- TikTok Research API exists but is very restricted
- Location tags in videos don't indicate current busyness
- No practical way to use this

### Summary
| Platform | Practical for Busyness | Quality | Cost |
|----------|----------------------|---------|------|
| Instagram | ❌ Very weak signal | Poor | ~$5-50/mo scrapers |
| Snapchat | ❌ No API | N/A | N/A |
| X/Twitter | ❌ Too sparse | Poor | $100/mo |
| TikTok | ❌ No useful API | N/A | N/A |

**Verdict:** Social media signals are NOT practical for real-time busyness data.

---

## 7. SafeGraph / Placer.ai

### SafeGraph
- Premium POI and foot traffic data provider
- Data sourced from mobile apps (GPS pings)
- **Coverage:** Primarily US-focused
- **Saudi Arabia:** ❌ Very limited or no coverage
- **Pricing:** Enterprise ($1,000+/month minimum)
- **Not suitable for Riyadh**

### Placer.ai
- Location intelligence platform with foot traffic analytics
- Uses mobile device data (SDK integrations in thousands of apps)
- **Coverage:** Primarily US
- **Saudi Arabia:** ❌ No confirmed coverage
- **Pricing:** Enterprise (custom, typically $1,000+/month)
- **Not suitable for Riyadh**

### Summary
Both SafeGraph and Placer.ai are US-centric enterprise solutions with no practical Saudi coverage. **Not viable for our use case.**

---

## 8. Waze / Traffic Data

### How It Could Work
- Waze provides real-time traffic data (jams, incidents, speed)
- Theory: High traffic near a restaurant = the restaurant is busy
- Waze Data Feed available for government/partner use

### Reality
- Correlation between nearby traffic and restaurant busyness is **very weak**
- Traffic jams could be unrelated (highway nearby, construction)
- Waze API is partner-only (not self-serve)
- Google Maps Routes/Traffic API could provide traffic data but same correlation problem
- **Not a reliable busyness indicator**

### Google Routes API (Alternative)
- Could check traffic density around a venue location
- $5 per 1,000 requests
- Same weak correlation problem

### Summary
| Aspect | Details |
|--------|---------|
| **Busyness indicator** | ❌ Very indirect, unreliable |
| **Practical** | ❌ Not suitable |

---

## 9. User-Generated / Crowdsourced

### Build Our Own "Is It Busy?" Feature
This is how apps like GrocerCheck (which built LivePopularTimes) and some restaurant apps work:

**Approach 1: User Reports**
- Users tap "How busy is it?" with options: Empty / Not Busy / Moderate / Busy / Very Busy
- Aggregate recent reports (last 1-2 hours)
- Weight recent reports higher
- Gamify: badges/points for reporting
- **Pros:** Real, human-verified data; free
- **Cons:** Needs critical mass of users; cold start problem; people may not bother

**Approach 2: Reservation/Waitlist Data**
- If places use reservation systems (e.g., Qlub, Foodics in Saudi), check availability
- Empty reservation slots = not busy
- **Pros:** Accurate for restaurants with reservations
- **Cons:** Most Saudi restaurants don't use open reservation APIs

**Approach 3: Hybrid**
- Start with Google Popular Times (historical patterns) as baseline
- Layer user reports on top for real-time adjustment
- As user base grows, shift toward user-generated data
- **This is the best long-term strategy**

### How "How Busy" Apps Work
Most crowd-reporting apps use a combination of:
1. Google Popular Times (scraped) as baseline/default
2. User self-reports
3. WiFi probe counting (for their own venues)
4. Computer vision (camera-based people counting)

### Summary
| Aspect | Details |
|--------|---------|
| **Cost** | Free (but needs development effort) |
| **Accuracy** | Low initially, improves with users |
| **Cold start** | ⚠️ Major challenge |
| **Long-term value** | ✅ Best proprietary data moat |
| **Implementation** | Medium (UI + backend + gamification) |

---

## 10. Telecom Data (STC/Zain/Mobily)

### How It Would Work
Telecom operators have anonymized cell tower connection data that shows device density in areas. This is used for:
- Urban planning
- Event crowd monitoring
- Transportation analysis

### Saudi Telecom Landscape
- **STC:** Has Smart City partnerships (e.g., with NEOM). Has anonymized mobility data programs.
- **Zain:** Offers some data analytics services
- **Mobily:** Similar capabilities

### Availability
⚠️ Telecom mobility data is available but:
- **Only via enterprise B2B agreements** (not self-serve API)
- Requires NDA and data licensing agreements
- Pricing: Likely $5,000-50,000+/month
- Data is area-level (cell tower resolution ~100-500m), not venue-level
- Privacy concerns under Saudi PDPL (Personal Data Protection Law)
- Need explicit purpose and data processing agreement

### Saudi PDPL Considerations
- PDPL applies to any processing of personal data of individuals in Saudi Arabia
- Location data is considered personal data
- Anonymized/aggregated data has fewer restrictions
- Must have lawful basis for processing
- Cross-border transfer restrictions apply

### Summary
| Aspect | Details |
|--------|---------|
| **Data quality** | Good for area-level, poor for venue-level |
| **Availability** | Enterprise B2B only |
| **Cost** | $5,000-50,000+/month |
| **Practical for us** | ❌ Way too expensive and complex |

---

## ⭐ RECOMMENDED APPROACH

### Best Strategy: Hybrid Multi-Layer System

Based on all research, here's what we can implement NOW, ranked by practicality:

### Tier 1: Implement Immediately (Free / Very Cheap)

#### 🥇 Option A: LivePopularTimes (Python Scraper) — FREE
```python
# pip install LivePopularTimes
import livepopulartimes

result = livepopulartimes.get_populartimes_by_address(
    "(Cafe Name) Address, Riyadh, Saudi Arabia"
)
# Returns: current_popularity (0-100), populartimes by hour/day
```
- **Cost:** Free (no API calls for address-based lookups)
- **Data:** Historical popular times + live busyness
- **Risk:** Scraping Google (ToS violation, may break)
- **Setup time:** 1-2 hours
- **Best for:** MVP / proof of concept

#### 🥈 Option B: Outscraper API — ~$27/month
- Official scraping service with Popular Times + Live data
- More reliable than DIY scraping
- 500 free records/month to start
- $3 per 1,000 records after
- Better for production use

### Tier 2: Production-Ready (Paid)

#### 🥉 Option C: BestTime.app Forecasts — ~$30-50/month
- Professional foot traffic forecasts
- Confirmed Saudi Arabia / Riyadh coverage
- Legal commercial service
- Hourly patterns per day of week
- No live data at this price (live adds ~$300/month)

#### Option D: SerpAPI — ~$130/month
- Most reliable popular times data
- Includes live busyness
- Well-documented API
- Good for production scale

### Tier 3: Long-Term Differentiator

#### Option E: Crowdsourced User Reports (Build It)
- Add "How busy is it?" to the app
- Users report busyness when they visit
- Gamify with points/badges
- Combine with historical data as baseline
- **Cost:** Development time only
- **Timeline:** Build after launch once you have users

---

### 🎯 MY RECOMMENDATION FOR RIYADH PLACES APP

**Phase 1 (MVP — NOW):**
1. Use **LivePopularTimes** (free) to get historical + live busyness for all 300 places
2. Cache data in your backend (refresh popular times weekly, live hourly during peak)
3. Display as "Usually busy" / "Not busy" with hourly chart
4. Fall back to "No data" for places without Google Popular Times

**Phase 2 (Production — Month 2):**
1. Switch to **Outscraper** ($27/mo) or **BestTime.app** ($50/mo) for reliability
2. Add live busyness refresh every 30-60 min during operating hours
3. Show "Live: Busy right now" vs "Usually: Not too busy at this time"

**Phase 3 (Growth — Month 3+):**
1. Add crowdsourced "Report busyness" feature
2. Users get badges for reporting
3. Weight: 70% Google data + 30% user reports → shifts as user base grows
4. This becomes your unique data moat competitors can't easily replicate

---

### Data Model Suggestion

```typescript
interface PlaceBusyness {
  placeId: string;
  
  // Historical patterns (updated weekly)
  popularTimes: {
    [day: string]: { // "sunday" | "monday" | ...
      [hour: number]: number; // 0-100 busyness score
    };
  };
  
  // Live/current (updated every 30-60 min)
  currentBusyness?: {
    score: number;        // 0-100
    label: string;        // "Not busy" | "A little busy" | "Busy" | "Very busy"
    updatedAt: string;    // ISO timestamp
    source: 'google' | 'user' | 'hybrid';
  };
  
  // User reports
  userReports: {
    score: number;        // Average of recent reports
    count: number;        // Number of reports in last 2 hours
    lastReport: string;   // ISO timestamp
  };
  
  // Metadata
  hasPopularTimes: boolean;
  typicalTimeSpent?: string; // "30 min - 1 hr"
  lastForecastUpdate: string;
}
```

### Cost Summary

| Approach | Monthly Cost | Data Quality | Live Data | Legal |
|----------|-------------|-------------|-----------|-------|
| LivePopularTimes | **$0** | High | ✅ | ⚠️ Gray area |
| Outscraper | **$27** | High | ✅ | ⚠️ Gray area |
| BestTime.app | **$50-130** | Good | ✅ (extra) | ✅ Legal |
| SerpAPI | **$130** | High | ✅ | ⚠️ Gray area |
| Crowdsourced | **$0** | Low→High | ✅ | ✅ Legal |

**Winner for MVP: LivePopularTimes (free) + plan to migrate to BestTime.app or Outscraper for production.**
