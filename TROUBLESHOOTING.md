# HomeLLM Troubleshooting Guide

## ✅ **Current Configuration Verified:**

- **Model**: `claude-sonnet-4-5-20250929` (Latest Claude Sonnet 4.5) ✓
- **Build**: Successfully builds (214KB) ✓
- **Dependencies**: All installed ✓
- **Imports**: Fixed (no .js extensions) ✓

---

## 🐛 **If Features Not Working - Step-by-Step Diagnosis**

### **Step 1: Check if App Loads**

Open browser to http://localhost:5173

**Expected**: You should see HomeLLM interface with header "HomeLLM" and API key input

**If blank screen**:
1. Open browser console (F12 → Console tab)
2. Look for errors
3. Common issues:
   - "Cannot find module" → Check imports
   - "Tailwind not loading" → Check index.css imports

---

### **Step 2: Test API Key Validation**

1. Enter any text in API key field
2. Should show error: "Invalid API key format. Must start with 'sk-ant-'"
3. Enter valid format: `sk-ant-test123`
4. Error should clear

**If validation not working**:
- Check browser console for JavaScript errors
- Verify `api-integration.js` is loaded

---

### **Step 3: Test Email Generation**

**Required fields** (must all be filled):
- Issue Type: Select any
- Send To: Select any
- Property Address: Enter any
- City: Enter any
- State: Select any
- Evidence & Description: Enter text
- Desired Outcome: Enter text
- Your Name: Enter name
- Your Email: Enter email

**Then**:
1. Click "Generate Email"
2. If API key invalid → See error message
3. If API key valid → Should see "Generating Email..." spinner
4. After 10-30 seconds → Email appears in right panel

**If not generating**:
```javascript
// Check browser console for these errors:

// Network Error
"Failed to fetch" or "ERR_NETWORK"
→ Check internet connection
→ Check if Anthropic API is accessible

// API Error
"Invalid API key"
→ Get new key from console.anthropic.com
→ Ensure sufficient credits

// 400 Bad Request
→ Check request format
→ May be image size issue

// CORS Error
→ Should NOT happen (API supports browser requests)
→ If it does, report bug

// Timeout
→ API taking too long
→ Try again or reduce image count
```

---

### **Step 4: Check Browser Console**

**How to open**:
- Chrome/Edge: F12 or Ctrl+Shift+I (Cmd+Opt+I on Mac)
- Firefox: F12 or Ctrl+Shift+K
- Safari: Cmd+Opt+I

**Look for**:
```
1. Red errors (❌)
   → Copy exact error message

2. Network tab
   → Click "Generate Email"
   → Look for request to "api.anthropic.com"
   → Check response status:
      - 200 ✓ Success
      - 400 ❌ Bad request
      - 401 ❌ Invalid API key
      - 429 ❌ Rate limit
      - 500 ❌ Server error

3. Console warnings (⚠️)
   → Usually safe to ignore
   → Unless blocking functionality
```

---

### **Step 5: Test with Curl (Verify API Key)**

```bash
# Test your API key directly
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: YOUR_API_KEY_HERE" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

**Expected**: JSON response with Claude's message

**If fails**:
- 401 → API key invalid
- 429 → Rate limited
- Check https://console.anthropic.com for account status

---

## 🔧 **Common Issues & Fixes**

### **Issue 1: "Email not generating"**

**Checklist**:
- [ ] All required fields filled?
- [ ] Valid API key entered?
- [ ] API key has credits?
- [ ] Browser console shows error?

**Fix**:
```javascript
// Test in browser console:
localStorage.getItem('homellm_api_key')
// Should show your API key

// If null, API key not saved
// Re-enter and check "Remember me" works
```

### **Issue 2: "Document analysis not working"**

**Checklist**:
- [ ] File uploaded successfully?
- [ ] File is image (JPEG/PNG)?
- [ ] File size < 5MB?
- [ ] API key valid?

**Fix**:
```javascript
// Check file size
console.log(document.querySelector('input[type="file"]').files[0].size)
// Should be < 5MB (5242880 bytes)

// If too large, resize image first
```

### **Issue 3: "Verification not working"**

**Note**: Verification requires:
1. Email already generated
2. Click "Verify Regulations Against Current Laws"
3. Wait 30-60 seconds (runs 6+ AI queries)

**If fails**:
- Check API credits (uses ~10,000 tokens)
- Each verification costs ~$0.15-0.30

### **Issue 4: "Styles not loading / looks broken"**

**Fix**:
```bash
# Rebuild Tailwind
npm run build

# Or check if Tailwind processing
# Look in browser console for:
# "Tailwind CSS" or styles loaded
```

### **Issue 5: "Module not found" errors**

**Fix**:
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

---

## 🧪 **Manual Testing Checklist**

### **Email Generation Test**:
```
1. [ ] Open http://localhost:5173
2. [ ] Enter API key (get from console.anthropic.com)
3. [ ] Fill required fields:
   - Issue: "Air Quality / Mold / VOCs"
   - Recipient: "Property Management / Landlord"
   - Address: "123 Test St"
   - City: "Denver"
   - State: "Colorado"
   - Evidence: "Visible mold in bathroom for 2 weeks"
   - Desired: "Professional mold inspection within 5 days"
   - Name: "Test User"
   - Email: "test@example.com"
4. [ ] Click "Generate Email"
5. [ ] Wait 10-30 seconds
6. [ ] Email should appear with:
   - Subject line
   - Professional tone
   - Regulatory citations (California Civil Code, EPA guidelines)
   - Specific timeline
   - Contact info
```

**Expected Output Example**:
```
Subject: Formal Request: Air Quality and Mold Issue at 123 Test St

Dear Property Management,

I am writing to formally request immediate attention to a serious health
and safety issue at my residence located at 123 Test St, Denver, Colorado.

ISSUE DESCRIPTION:
Visible mold growth has been present in the bathroom for approximately
two weeks...

LEGAL OBLIGATIONS:
Under Colorado's warranty of habitability (C.R.S. § 38-12-503), landlords
must maintain...

EPA mold remediation guidelines recommend...

REQUESTED ACTION:
I request a professional mold inspection be conducted within 5 business
days...

[continues with proper format]
```

### **Water Analysis Test**:
```
1. [ ] Click "Water Report Analysis" tab
2. [ ] Upload test image (any clear image)
3. [ ] Click "Analyze Report"
4. [ ] Wait 20-40 seconds
5. [ ] Should show analysis with:
   - Contaminants identified
   - EPA comparison
   - Health risks
   - Recommendations
```

### **Benefits Discovery Test**:
```
1. [ ] Would require warranty document upload
2. [ ] Should analyze coverage
3. [ ] Identify unused benefits
4. [ ] Estimate value
```

---

## 📊 **Performance Benchmarks**

**Expected timings**:
- App load: < 3 seconds
- Email generation: 10-30 seconds
- Document analysis: 20-40 seconds
- Verification: 30-60 seconds

**If slower**:
- Check internet speed
- Check API response time
- Reduce image sizes
- Check console for errors

---

## 🔍 **Debug Mode**

Add to browser console:
```javascript
// Enable debug logging
localStorage.setItem('homellm_debug', 'true')

// Then reload page and check console for detailed logs
```

---

## 💰 **API Cost Tracking**

Each operation uses approximately:
- Email generation: ~2,000-5,000 tokens ($0.01-0.02)
- Document analysis: ~3,000-8,000 tokens ($0.02-0.04)
- Verification (6 queries): ~10,000-15,000 tokens ($0.05-0.08)
- Complete benefit scan: ~15,000-30,000 tokens ($0.08-0.15)

**If hitting rate limits**:
- Check usage at console.anthropic.com
- Upgrade plan or add credits
- Reduce concurrent requests

---

## 🆘 **Still Not Working?**

### **Gather Debug Info**:
```bash
# 1. Check build
npm run build

# 2. Check dev server logs
npm run dev
# Look for errors

# 3. Browser info
console.log(navigator.userAgent)

# 4. Check API response
# Network tab → Find request to anthropic.com
# Copy response body
```

### **Report Issues**:
Include:
1. Browser + version
2. OS
3. Exact error message from console
4. Steps to reproduce
5. Screenshot if possible

---

## ✅ **Verification Completed**

After following this guide:
- [ ] App loads in browser
- [ ] API key validates correctly
- [ ] Email generation works
- [ ] Subject line generated
- [ ] Email contains regulations
- [ ] Document analysis works (optional feature)
- [ ] No console errors

**If all checked**: App is working correctly! 🎉

**If some fail**: Review specific section above for that feature.

---

## 🎯 **Quick Start for Testing**

```bash
# Terminal 1: Start dev server
npm run dev

# Terminal 2: Test build
npm run build

# Browser:
# 1. Open http://localhost:5173
# 2. Enter API key from console.anthropic.com
# 3. Fill ALL required fields (* marked)
# 4. Click "Generate Email"
# 5. Wait for result

# Expected: Professional email with regulations in 10-30 seconds
```

---

## 📝 **Model Configuration Confirmed**

```javascript
// src/api-integration.js line 6:
const MODEL = 'claude-sonnet-4-5-20250929'; // ✓ Latest Sonnet 4.5

// Verified: This IS the most advanced Claude model (as of Sept 2025)
```

---

**Need more help?** Check browser console first - 90% of issues show errors there!
