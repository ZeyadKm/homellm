# Manual Testing Procedure for HomeLLM

## Prerequisites

1. ✅ Dev server running: `npm run dev`
2. ✅ Browser open to: http://localhost:5173
3. ⚠️  Valid Anthropic API key (get from https://console.anthropic.com)

## Test 1: Verify App Loads

**Steps:**
1. Open http://localhost:5173
2. Open browser console (F12 or Cmd+Option+I)

**Expected:**
- HomeLLM interface visible with header
- API key input field visible
- Four tabs: "Email Generator", "Water Report Analysis", "Warranty Analysis", "Saved Drafts"
- No JavaScript errors in console

**If fails:**
- Check console for errors
- Check that all JS files loaded (Network tab)
- Verify no 404s for missing modules

---

## Test 2: API Key Validation

**Steps:**
1. Enter invalid key: `test123`
2. Check for error message

**Expected:**
- Error: "Invalid API key format. Must start with 'sk-ant-'"

**Steps:**
3. Enter valid format: `sk-ant-test123`
4. Error should clear

**If fails:**
- Check browser console for JavaScript errors
- Verify `validateApiKey` function is working

---

## Test 3: Email Generation (MAIN TEST)

### Setup:
1. Get real API key from https://console.anthropic.com
2. Enter API key in field at top
3. Fill ALL required fields:

**Required Fields:**
- Issue Type: `Air Quality / Mold / VOCs`
- Send To: `Property Management / Landlord`
- Property Address: `123 Test Street`
- City: `Denver`
- State: `Colorado`
- Evidence & Description: `Visible black mold growth in bathroom corner for 2 weeks. Strong musty odor. Previous requests ignored.`
- Desired Outcome: `Professional mold inspection and remediation within 5 business days`
- Your Name: `John Smith`
- Your Email: `test@example.com`

### Execute:
1. Click "Generate Email" button
2. Watch browser console for errors
3. Watch Network tab for API request

**Expected:**
- Button shows "Generating Email..." with spinner
- After 10-30 seconds, email appears in right panel
- Email includes:
  - Professional language
  - Specific regulations (EPA, state codes)
  - Timeline for action
  - Contact information
- Subject line generated at top

**If fails - Check these:**

### Network Error:
```
Failed to fetch
```
→ Check internet connection
→ Verify api.anthropic.com is accessible
→ Check browser Network tab for failed requests

### API Error 401:
```
Invalid API key
```
→ Verify API key is correct
→ Check API key has credits at console.anthropic.com
→ Try generating new API key

### API Error 400:
```
Bad request: ...
```
→ Check browser console for full error
→ Verify request format matches Anthropic API spec
→ Check if images are causing issue (try without images first)

### API Error 429:
```
Rate limit exceeded
```
→ Wait 60 seconds
→ Check API usage at console.anthropic.com
→ Verify you have available credits

### JavaScript Error:
- Open browser console
- Look for red errors
- Check if error is in:
  - `api-integration.js` → API call issue
  - `email-prompt-engine.js` → Prompt generation issue
  - `regulatory-knowledge-base.js` → Data structure issue
  - `HomeLLM.jsx` → UI/React issue

### No Response (timeout):
- Check if API call was made (Network tab)
- Check API response time
- Try with simpler prompt (remove images)

---

## Test 4: Document Analysis

### Water Report Test:
1. Click "Water Report Analysis" tab
2. Upload any clear image file (JPG/PNG, <5MB)
3. Click "Analyze Report"

**Expected:**
- Analysis appears after 20-40 seconds
- Shows contaminants, EPA comparison, health risks

**If fails:**
- Check file size (<5MB)
- Check file format (JPEG/PNG only)
- Check browser console for errors
- Verify API key is valid

### Warranty Document Test:
1. Click "Warranty Analysis" tab
2. Upload warranty document image
3. Click "Analyze Warranty"

**Expected:**
- Analysis shows coverage, unused benefits, expiration dates

---

## Test 5: Browser Console Debugging

Open console and run these commands:

### Check API key saved:
```javascript
localStorage.getItem('homellm_api_key')
```
Should show your API key (or null if not saved)

### Check React app loaded:
```javascript
document.querySelector('#root').innerHTML.length > 0
```
Should return `true`

### Enable debug mode:
```javascript
localStorage.setItem('homellm_debug', 'true')
location.reload()
```

### Check for React errors:
Look for red text in console starting with:
- `Error:`
- `Uncaught`
- `TypeError:`
- `ReferenceError:`

---

## Common Issues & Solutions

### Issue: "Form validation failing"
**Symptoms:** Button does nothing when clicked
**Solution:**
- Check all required fields are filled (marked with *)
- Open console, look for validation error message
- Verify email format is valid

### Issue: "API calls not being made"
**Symptoms:** No network request in Network tab
**Solution:**
- Check if API key validation is passing
- Check if form validation is passing
- Add `console.log()` in handleGenerateEmail to debug

### Issue: "CORS error"
**Symptoms:** `Access-Control-Allow-Origin` error
**Solution:**
- Should NOT happen (Anthropic API supports browser requests)
- If it does, may need to add proxy server
- Check if API endpoint URL is correct

### Issue: "Module not found"
**Symptoms:** `Cannot find module './xyz'`
**Solution:**
```bash
# Check all files exist
ls -la src/

# Should see:
# - HomeLLM.jsx
# - api-integration.js
# - email-prompt-engine.js
# - regulatory-knowledge-base.js
# - web-verification.js
# - etc.

# If missing, rebuild:
npm install
npm run build
```

### Issue: "Styles not loading"
**Symptoms:** Plain HTML with no styling
**Solution:**
```bash
# Rebuild Tailwind
npm run build

# Check if index.css exists
cat src/index.css

# Should see @tailwind directives
```

---

## Verification Checklist

After testing, verify:
- [ ] App loads without errors
- [ ] API key validation works
- [ ] Email generation works with valid API key
- [ ] Subject line is generated
- [ ] Email contains regulatory citations
- [ ] Email is professional and well-formatted
- [ ] Copy to clipboard works
- [ ] Save draft works
- [ ] Document analysis works (optional)
- [ ] No console errors during normal operation

---

## Debug Information to Collect

If issues persist, collect this info:

### Browser Info:
```javascript
console.log(navigator.userAgent)
```

### Check Build:
```bash
npm run build
# Should complete without errors
# Should show bundle size ~200-250KB
```

### Check Dependencies:
```bash
npm list --depth=0
# Should show all packages installed
```

### Check Dev Server:
```bash
npm run dev
# Should start on localhost:5173
# Should not show errors
```

### Check API Response:
1. Open Network tab
2. Generate email
3. Find request to `api.anthropic.com`
4. Right-click → Copy → Copy Response
5. Check response structure

---

## Expected API Response Format

```json
{
  "id": "msg_123abc",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Subject: [Generated Subject]\n\nDear [Recipient],\n\n[Email body with regulations]..."
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "usage": {
    "input_tokens": 1234,
    "output_tokens": 567
  }
}
```

---

## Testing Without Real API Key

If you don't have an API key yet:

1. Test form validation:
   - Leave fields empty, click Generate
   - Should show "Please fill in required fields" error

2. Test API key validation:
   - Enter invalid format: `test123`
   - Should show "Invalid API key format" error

3. Test UI functionality:
   - Switch between tabs
   - Upload images (won't analyze without API key)
   - Check copy buttons work
   - Check draft saving works

---

## Estimated Costs

Each operation with real API key:
- Email generation: $0.01-0.02 (2,000-5,000 tokens)
- Document analysis: $0.02-0.04 (3,000-8,000 tokens)
- Verification: $0.05-0.08 (10,000-15,000 tokens)

Total for full test: ~$0.08-0.14

---

## Next Steps if Still Not Working

1. **Check Model Availability:**
   - Verify `claude-sonnet-4-5-20250929` is accessible
   - Try with older model: `claude-3-5-sonnet-20241022`

2. **Add Debug Logging:**
   - Add `console.log()` statements throughout code
   - Check what data is being passed to API

3. **Test API Directly:**
   - Use curl or Postman to test Anthropic API
   - Verify API key works outside of app

4. **Check Browser Compatibility:**
   - Try different browser (Chrome, Firefox, Safari)
   - Disable browser extensions
   - Try incognito/private mode

5. **Review Recent Changes:**
   - Check git log for recent commits
   - Revert to last known working version if needed
