# HomeLLM Setup Instructions

## Current Situation

You're currently in a **Python project** (air pollution literature agent), but HomeLLM is a **React/JavaScript application**. The files I created need to be moved to a React project.

## Option 1: Quick Setup (Create New React Project)

### Step 1: Create React App with Vite

```bash
# Navigate to parent directory
cd ..

# Create new React project
npm create vite@latest homellm-app -- --template react

# Navigate into project
cd homellm-app

# Install dependencies
npm install

# Install required packages
npm install lucide-react
```

### Step 2: Move HomeLLM Files

```bash
# Copy all HomeLLM files to src folder
cp ../Mrpsych1/HomeLLM.jsx ./src/
cp ../Mrpsych1/regulatory-knowledge-base.js ./src/
cp ../Mrpsych1/email-prompt-engine.js ./src/
cp ../Mrpsych1/api-integration.js ./src/
cp ../Mrpsych1/web-verification.js ./src/
cp ../Mrpsych1/utility-report-analyzer.js ./src/
cp ../Mrpsych1/benefits-discovery-engine.js ./src/
cp ../Mrpsych1/automated-claim-assistant.js ./src/
cp ../Mrpsych1/opportunity-detector.js ./src/
```

### Step 3: Update App.jsx

```bash
# Edit src/App.jsx
cat > src/App.jsx << 'EOF'
import HomeLLM from './HomeLLM'
import './App.css'

function App() {
  return <HomeLLM />
}

export default App
EOF
```

### Step 4: Add Tailwind CSS (for styling)

```bash
# Install Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Configure Tailwind
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

# Update src/index.css
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF
```

### Step 5: Run the App

```bash
npm run dev
```

Then open http://localhost:5173 in your browser!

---

## Option 2: Quick Test (Single HTML File)

For quick testing without full React setup:

```bash
cd ~/Documents/Mrpsych1

# Create standalone HTML version
cat > homellm-demo.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HomeLLM Demo</title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { margin: 0; font-family: system-ui, -apple-system, sans-serif; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel" src="./HomeLLM.jsx"></script>
  <script type="text/babel">
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<HomeLLM />);
  </script>
</body>
</html>
EOF

# Open in browser
open homellm-demo.html
```

---

## Option 3: Add to Existing React Project

If you already have a React project:

```bash
# Copy files to your React project's src folder
cp HomeLLM.jsx /path/to/your-react-app/src/
cp *.js /path/to/your-react-app/src/

# Install dependencies
cd /path/to/your-react-app
npm install lucide-react

# Import in your App.jsx or router
import HomeLLM from './HomeLLM';

// Use in your component
<HomeLLM />
```

---

## Troubleshooting

### Issue: "Module not found"

**Solution**: Make sure all .js files are in the same directory as HomeLLM.jsx

### Issue: "Tailwind classes not working"

**Solution**: Make sure Tailwind CSS is installed and configured (see Option 1, Step 4)

### Issue: "lucide-react not found"

**Solution**:
```bash
npm install lucide-react
```

### Issue: API calls failing

**Solution**: Check browser console for errors. Make sure:
1. You've entered a valid Anthropic API key
2. API key has sufficient credits
3. No CORS issues (should work from localhost)

---

## Recommended: Option 1 (Full React Setup)

For best experience, use **Option 1** which gives you:
- ✅ Hot reload during development
- ✅ Proper build system
- ✅ Full React ecosystem
- ✅ Easy deployment

**Quick Command Summary:**
```bash
cd ~/Documents
npm create vite@latest homellm-app -- --template react
cd homellm-app
npm install
npm install lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Copy all HomeLLM files
cp ../Mrpsych1/*.js ./src/
cp ../Mrpsych1/HomeLLM.jsx ./src/

# Update App.jsx (see Step 3 above)
# Configure Tailwind (see Step 4 above)

npm run dev
```

Then open http://localhost:5173

---

## Next Steps After Setup

1. **Enter API Key**: Get from https://console.anthropic.com
2. **Test Email Generation**: Fill out form and generate an advocacy email
3. **Try Verification**: Click "Verify Regulations Against Current Laws"
4. **Explore Other Features**:
   - Water Report Analysis tab
   - Warranty Analysis tab
   - Saved Drafts tab

---

## Files You Have

In `/Users/zeyadkassem/Documents/Mrpsych1/`:

**Core Application:**
- ✅ `HomeLLM.jsx` - Main React component
- ✅ `regulatory-knowledge-base.js` - Regulations database
- ✅ `email-prompt-engine.js` - AI prompt system
- ✅ `api-integration.js` - Claude API integration
- ✅ `web-verification.js` - Regulatory verification

**Benefits Optimizer:**
- ✅ `utility-report-analyzer.js`
- ✅ `benefits-discovery-engine.js`
- ✅ `automated-claim-assistant.js`
- ✅ `opportunity-detector.js`

**Documentation:**
- ✅ `HOMELLM_README.md`
- ✅ `BENEFITS_OPTIMIZER_GUIDE.md`
- ✅ `VERIFICATION_GUIDE.md`
- ✅ `NEW_FEATURES_SUMMARY.md`

---

## Need Help?

1. **React Setup Issues**: https://vitejs.dev/guide/
2. **Tailwind Issues**: https://tailwindcss.com/docs/installation
3. **API Issues**: https://docs.anthropic.com/claude/reference/getting-started-with-the-api

---

**You're ready to build! Choose Option 1 for the best experience.** 🚀
