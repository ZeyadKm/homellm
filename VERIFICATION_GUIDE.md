# Web Verification System - HomeLLM

## Overview

HomeLLM now includes an **AI-powered web verification system** that double-checks the accuracy of regulations, standards, and legal citations in generated emails.

## How It Works

### Two-Stage Verification Process

1. **Regulatory Research Phase**
   - Constructs 6 targeted search queries based on your issue type, state, and city
   - Example queries:
     - "California mold remediation laws 2025"
     - "EPA lead copper rule revisions 2025"
     - "New York tenant rights habitability 2025"
   - Uses Claude to research current regulations (simulates web search)
   - Focuses on official government sources (.gov domains)

2. **Cross-Check Phase**
   - Extracts all regulation citations from your generated email
   - Compares each citation against verified current sources
   - Identifies outdated, incorrect, or missing citations
   - Provides accuracy rating (High/Medium/Low)
   - Suggests corrections if needed

## Using the Verification System

### Step-by-Step

1. **Generate Your Email First**
   - Fill out the form completely
   - Click "Generate Email"
   - Review the generated advocacy letter

2. **Click "Verify Regulations Against Current Laws"**
   - Button appears below the action buttons
   - Takes 30-60 seconds (runs 6+ AI queries)
   - Shows "Verifying Regulations..." with spinner

3. **Review Verification Report**
   - Green badge appears: "✓ Regulations Verified"
   - Click "View Verification Report" to see details
   - Report includes:
     - **Accuracy Rating**: Overall confidence (High/Medium/Low)
     - **Citations Verified**: List of regulations checked
     - **Issues Found**: Any inaccuracies or outdated info
     - **Recommended Corrections**: Suggested fixes with proper citations
     - **Sources Consulted**: List of queries run

4. **Use Verified Email with Confidence**
   - Verification badge shows recipients the email is fact-checked
   - Copy, download, or save as usual

## What Gets Verified

### Federal Regulations
- ✓ EPA standards (air, water, lead, etc.)
- ✓ HUD housing quality standards
- ✓ OSHA workplace safety limits
- ✓ Clean Air Act provisions
- ✓ Safe Drinking Water Act standards
- ✓ Federal statute citations (42 U.S.C. §, 40 CFR)

### State Regulations
- ✓ State environmental laws
- ✓ Tenant rights and habitability statutes
- ✓ State-specific health standards
- ✓ Repair timeline requirements
- ✓ Disclosure obligations

### Local Codes
- ✓ Building codes (IBC, IRC)
- ✓ Municipal health ordinances
- ✓ Local housing standards
- ✓ City-specific requirements

### Standards & Guidelines
- ✓ ASHRAE ventilation standards
- ✓ EPA action levels
- ✓ Industry best practices

## Example Verification Report

```
ACCURACY VERIFICATION REPORT
Timestamp: 2025-01-09 14:32:15

Overall Accuracy Rating: HIGH

✓ CITATIONS VERIFIED (7 found):

1. Safe Drinking Water Act (42 U.S.C. §300f et seq.)
   Status: ACCURATE - Current federal law
   Source: EPA.gov

2. Lead Action Level: 15 ppb
   Status: ACCURATE - Current EPA standard (40 CFR 141.80)
   Source: EPA Lead and Copper Rule

3. California Health & Safety Code §116270
   Status: ACCURATE - California Safe Drinking Water Act
   Source: California Legislative Information

4. Warranty of Habitability (Civil Code §1941)
   Status: ACCURATE - California tenant rights law
   Source: California Civil Code

5. 30-day repair timeline
   Status: ACCURATE - California standard for non-urgent repairs
   Source: CA Civil Code §1942

6. HUD Housing Quality Standards (24 CFR §982.401)
   Status: ACCURATE - Federal housing program standards
   Source: HUD.gov

7. Repair and deduct remedy
   Status: ACCURATE - California Civil Code §1942
   Source: CA tenant rights statute

⚠️ ISSUES FOUND: None

✓ RECOMMENDED ACTIONS: No corrections needed. All citations are current and accurate as of 2025.

CONFIDENCE LEVEL: High (100% of citations verified)

Sources Consulted:
• California drinking water standards 2025
• EPA lead copper rule revisions 2025
• California tenant rights habitability 2025
• California landlord repair timeline requirements
• HUD housing quality standards 2025
• EPA safe drinking water act 2025
```

## Limitations & Important Notes

### Current Limitations

1. **Not True Web Search (Yet)**
   - Currently uses Claude's knowledge (up to Jan 2025)
   - Does NOT actually crawl live websites
   - To enable true web search, integrate:
     - Google Custom Search API
     - Bing Search API
     - SerpAPI
     - (See "Integration Guide" below)

2. **Knowledge Cutoff**
   - Claude's knowledge ends January 2025
   - Very recent law changes (last few months) may not be included
   - Always verify critical citations with official sources

3. **No Substitute for Legal Advice**
   - Verification helps accuracy but doesn't constitute legal advice
   - Consult licensed attorneys for legal matters
   - Use official government websites for authoritative sources

### Best Practices

✓ **DO**:
- Run verification on every generated email before sending
- Check the accuracy rating (aim for "High")
- Review any flagged issues and apply corrections
- Verify critical citations at official .gov sources
- Note the verification timestamp

✗ **DON'T**:
- Rely solely on verification without manual review
- Skip verification for formal/legal escalation levels
- Use outdated verifications (re-verify if >30 days old)
- Ignore warnings or medium/low accuracy ratings

## Integration with Real Web Search

To enable **true live web search**, integrate one of these APIs:

### Option 1: Google Custom Search API

1. Get API key: [Google Cloud Console](https://console.cloud.google.com/)
2. Create Custom Search Engine: [programmablesearchengine.google.com](https://programmablesearchengine.google.com/)
3. Update `web-verification.js`:

```javascript
// Enable real Google search
const GOOGLE_API_KEY = 'your-api-key';
const SEARCH_ENGINE_ID = 'your-search-engine-id';

async function searchAndVerify(apiKey, query) {
  // Use googleCustomSearch instead of Claude simulation
  const searchResults = await googleCustomSearch(
    query,
    GOOGLE_API_KEY,
    SEARCH_ENGINE_ID
  );

  // Filter for .gov sources
  const officialResults = filterOfficialSources(searchResults.results);

  // Then use Claude to analyze the search results
  // ...
}
```

### Option 2: SerpAPI (Easiest)

1. Sign up: [serpapi.com](https://serpapi.com/)
2. Get API key
3. Update `web-verification.js`:

```javascript
const SERPAPI_KEY = 'your-serpapi-key';

async function searchAndVerify(apiKey, query) {
  const searchResults = await serpApiSearch(query, SERPAPI_KEY);
  // Process results...
}
```

### Option 3: Bing Search API

1. Azure subscription required
2. Create Bing Search resource
3. Similar integration pattern

## Cost Considerations

### Current (Claude-only) Implementation
- **Cost per verification**: ~$0.15-0.30
  - 6 queries × ~1000 tokens input
  - 6 queries × ~500 tokens output
  - 1 cross-check × ~3000 tokens input/output
- **Total tokens**: ~10,000-15,000 per verification

### With Web Search APIs
- **Google Custom Search**: $5 per 1000 queries (after free 100/day)
- **SerpAPI**: $50/month for 5000 searches
- **Bing**: $7 per 1000 transactions

**Recommendation**: For production use, combine free Google Custom Search (100/day) with Claude analysis.

## Privacy & Security

✓ **Verification queries DO NOT include**:
- Your personal information
- Property addresses
- Names or contact details
- Specific evidence or measurements

✓ **Queries only include**:
- Issue type (e.g., "water quality")
- State/city (e.g., "California", "Los Angeles")
- Year (for current standards)
- Generic regulation names

Example query: "California lead paint disclosure laws 2025"

## Troubleshooting

**Verification fails or times out:**
- Check internet connection
- Verify API key is valid and has credits
- Try reducing number of queries (edit `buildVerificationQueries()`)
- Check browser console for specific errors

**Low accuracy rating:**
- Regenerate email with more specific evidence
- Manually add regulation references to form
- Update static knowledge base if outdated
- Consider consulting local attorney

**Verification takes too long:**
- Normal: 30-60 seconds for full verification
- Can reduce queries from 6 to 3 for faster results
- Consider caching verification results

## Roadmap

Future enhancements:
- [ ] True web scraping of .gov sites
- [ ] Verification result caching (reduce repeat queries)
- [ ] Scheduled re-verification of saved drafts
- [ ] Export verification report as PDF
- [ ] Bulk verification of multiple emails
- [ ] Integration with legal citation databases (Westlaw, LexisNexis)
- [ ] Crowdsourced regulatory updates
- [ ] Real-time regulation change notifications

## Technical Architecture

```
User generates email
       ↓
Clicks "Verify Regulations"
       ↓
System builds 6 targeted queries
       ↓
For each query:
  - Construct search query
  - Execute web search (or Claude knowledge)
  - Extract official sources
  - Compile findings
       ↓
Extract citations from generated email
       ↓
Cross-check citations vs. verified sources
       ↓
Generate accuracy report
       ↓
Display verification badge + report
```

## Support

For issues or questions about the verification system:
- Check browser console for detailed errors
- Verify API key has sufficient credits
- Review query construction in `web-verification.js`
- Open GitHub issue with verification report

---

**Verification adds confidence to your advocacy. Use it every time.** ✓
