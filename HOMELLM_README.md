# HomeLLM - AI-Powered Home Health Advocacy Platform

An intelligent application designed to help homeowners, tenants, and advocacy organizations draft professional, legally-grounded emails to escalate home health and safety concerns to HOAs, utility companies, government agencies, and other entities.

## 🎯 Purpose

HomeLLM empowers individuals and organizations focused on indoor home evaluations and optimization (air purifiers, water filters, etc.) to effectively advocate for healthier living environments by:

- Drafting professional correspondence backed by federal, state, and local regulations
- Analyzing water quality reports and warranty documents
- Providing regulatory citations and legal frameworks
- Escalating concerns appropriately based on issue severity
- Documenting evidence and health impacts systematically

## 🏗️ Architecture

### Core Components

1. **Regulatory Knowledge Base** (`regulatory-knowledge-base.js`)
   - Comprehensive database of federal regulations (EPA, HUD, OSHA, etc.)
   - State-specific laws for all 50 states
   - Local code references and HOA regulations
   - Water quality standards, air quality limits, hazardous material thresholds
   - Dynamic lookup by issue type, state, and recipient

2. **Email Prompt Engine** (`email-prompt-engine.js`)
   - Context-aware prompt generation for Claude API
   - Escalation-level specific guidance (Initial → Professional → Formal → Legal)
   - Recipient-specific templates (HOA, landlord, utility, government, nonprofit)
   - Document analysis prompts for water reports, warranties, test results
   - Subject line generation

3. **API Integration** (`api-integration.js`)
   - Claude API communication (using Sonnet 4.5)
   - Vision capabilities for document image analysis
   - Building code lookup via AI
   - Draft management (save/load/delete)
   - Export functionality (TXT, HTML)
   - Clipboard operations

4. **React Component** (`HomeLLM.jsx`)
   - Complete user interface with four main tabs:
     - Email Generator
     - Water Report Analysis
     - Warranty Analysis
     - Saved Drafts
   - Form validation and error handling
   - Urgency assessment and alerts
   - Image attachment with preview
   - Real-time API key validation

## 📋 Features

### Email Generator
- **11 Issue Types**: Air quality, water quality, HVAC, lead/asbestos, radon, CO, pests, structural, noise, utility, EMF
- **7 Recipient Types**: HOA, landlord, utility, local/state/federal government, nonprofit
- **4 Escalation Levels**: Initial request → Professional follow-up → Formal complaint → Legal notice
- **4 Urgency Levels**: Low → Medium → High → Emergency
- **Evidence Tracking**: Photos, measurements, health impacts, previous contacts
- **Auto Code Lookup**: AI-powered building code and regulation lookup
- **Smart Alerts**: Automatic urgency detection based on measurements (e.g., CO levels > 70 ppm)

### Document Analysis
- **Water Quality Reports**: EPA standard comparison, contaminant analysis, health risk assessment
- **Warranty Documents**: Coverage analysis, claim process, legal rights explanation
- **Image OCR**: Extract text from document images using Claude's vision
- **Export to Email**: One-click transfer of analysis to email generator

### Draft Management
- Save generated emails for later use
- Load previous drafts to modify
- Timestamp tracking
- Persistent localStorage

## 🚀 Setup & Installation

### Prerequisites
- Node.js 14+ and npm/yarn
- React 17+ project
- Anthropic API key (get from [console.anthropic.com](https://console.anthropic.com))
- Lucide React icons
- Tailwind CSS (for styling)

### Installation

1. **Copy files to your React project:**
```bash
# Copy all files to your src/ directory
cp HomeLLM.jsx src/
cp regulatory-knowledge-base.js src/
cp email-prompt-engine.js src/
cp api-integration.js src/
```

2. **Install dependencies:**
```bash
npm install lucide-react
# or
yarn add lucide-react
```

3. **Import and use the component:**
```jsx
import HomeLLM from './HomeLLM';

function App() {
  return <HomeLLM />;
}
```

4. **Add your API key:**
   - Launch the app
   - Enter your Anthropic API key in the header
   - Key is saved to localStorage for future sessions

## 📖 Usage Guide

### Basic Email Generation Workflow

1. **Enter API Key** (first time only)
   - Get key from [console.anthropic.com](https://console.anthropic.com)
   - Paste in header field
   - Key is validated and saved automatically

2. **Fill Issue Details**
   - Select issue type (e.g., "Air Quality / Mold / VOCs")
   - Choose recipient (e.g., "Property Management / Landlord")
   - Enter property address, city, and state

3. **Provide Evidence**
   - Describe the issue in detail
   - Add measurements (e.g., "Mold test: 50,000 spores/m³")
   - Document health impacts
   - Upload photos as evidence
   - Note previous contact attempts

4. **Set Escalation & Urgency**
   - Choose escalation level based on previous attempts
   - Set urgency (system will alert if measurements indicate emergency)

5. **Add Context (Optional)**
   - Click "Auto-Lookup Local Codes" for AI-powered regulation research
   - Add any additional regulations or context

6. **Enter Desired Outcome**
   - Specify what action you want (e.g., "Professional mold inspection within 5 days")

7. **Provide Contact Info**
   - Your name, email, phone, address

8. **Generate Email**
   - Click "Generate Email"
   - Wait 10-30 seconds for AI generation
   - Review generated email with subject line

9. **Take Action**
   - Copy to clipboard
   - Download as .txt file
   - Save as draft for later
   - Edit in your email client and send

### Document Analysis Workflow

**Water Reports:**
1. Click "Water Report Analysis" tab
2. Upload water quality report (image or PDF)
3. Click "Analyze Report"
4. Review analysis (contaminants, health risks, EPA comparisons)
5. Click "Use in Email Generator" to add to evidence

**Warranties:**
1. Click "Warranty Analysis" tab
2. Upload warranty document
3. Click "Analyze Warranty"
4. Review coverage, exclusions, claim process
5. Use analysis in email if relevant

## 🧠 How It Works

### Regulatory Training Data

The system uses a comprehensive knowledge base organized by:

**Federal Level:**
- Clean Air Act, Safe Drinking Water Act, Fair Housing Act
- EPA standards (PM2.5, lead, VOCs, water contaminants)
- HUD housing quality standards
- OSHA workplace standards

**State Level:**
- State-specific environmental laws (California CARB, NY mold laws, etc.)
- Stricter state standards (CA lead 5ppb vs federal 15ppb)
- State tenant protection laws
- State water quality rules

**Local Level:**
- International Building Code (IBC)
- International Residential Code (IRC)
- Local municipal ordinances
- HOA governing documents

### AI Prompt Engineering

The system constructs detailed prompts that include:

1. **Expert Persona**: Legal/environmental health advocate with regulatory knowledge
2. **Regulatory Context**: Relevant laws, standards, and citations for the specific issue
3. **Escalation Guidance**: Tone, approach, consequences, and timeline based on escalation level
4. **Recipient Guidance**: Specific strategies for HOAs, landlords, utilities, government
5. **Structural Requirements**: Subject line, opening, legal framework, action items, closing
6. **Evidence Integration**: Photos, measurements, health impacts, previous contacts

### Urgency Assessment

Automatic emergency detection based on:
- Keywords: "carbon monoxide", "gas leak", "collapse", "unconscious"
- Thresholds: CO > 70ppm, Radon > 10 pCi/L, lead in blood > 5 μg/dL
- Alerts user to call 911 if emergency detected

## 📊 Supported Issue Types & Standards

| Issue Type | Key Standards | Agencies |
|-----------|---------------|----------|
| Air Quality / Mold | No federal mold limit (EPA guidance); PM2.5: 12 μg/m³ annual | EPA, CDC, State Health Depts |
| Water Quality | Lead: 15ppb; Arsenic: 10ppb; PFAS: 4ppt (proposed) | EPA, State Water Boards |
| HVAC/Ventilation | ASHRAE 62.2: 15 CFM/person + 3 CFM/100 sq ft | ASHRAE, HUD, Local Building |
| Lead/Asbestos | Lead dust: 10 μg/ft² (floors); Asbestos: NESHAP rules | EPA, HUD, OSHA |
| Radon | 4 pCi/L action level | EPA, State Health Depts |
| Carbon Monoxide | 9 ppm (8-hour); 35 ppm (1-hour) | EPA, Local Fire Dept |

## 🔐 Security & Privacy

- **API Key Storage**: Stored in browser localStorage only (never sent to external servers except Anthropic)
- **No Data Collection**: All processing happens client-side or via Claude API
- **Draft Storage**: Drafts saved locally in browser localStorage
- **No Server Required**: Pure client-side React application

## ⚖️ Legal Disclaimer

**This tool provides information only and does not constitute legal, medical, or professional advice.**

- Consult licensed attorneys for legal matters
- Consult medical professionals for health concerns
- Consult licensed contractors/inspectors for home issues
- Verify all regulations with official sources
- Local laws may override state/federal laws

The developers assume no liability for actions taken based on this tool's output.

## 🎨 Customization

### Adding New States
Edit `regulatory-knowledge-base.js`:
```javascript
states: {
  YourState: {
    airQuality: { laws: [...], standards: {...}, agencies: [...] },
    waterQuality: { laws: [...], standards: {...} },
    tenantRights: { laws: [...], repairTimelines: '...', remedies: '...' }
  }
}
```

### Adding New Issue Types
1. Add to `issueTypes` array in `HomeLLM.jsx`
2. Add mapping in `issueTypeMapping` in `regulatory-knowledge-base.js`
3. Add federal regulations in `regulatoryKnowledgeBase.federal`

### Customizing Escalation Levels
Edit `getEscalationGuidance()` in `email-prompt-engine.js`

### Changing AI Model
Edit `MODEL` constant in `api-integration.js`:
```javascript
const MODEL = 'claude-3-5-sonnet-20241022'; // Change to different model
```

## 🐛 Troubleshooting

**"Invalid API key" error:**
- Ensure key starts with `sk-ant-`
- Check key at [console.anthropic.com](https://console.anthropic.com)
- Verify sufficient API credits

**Email generation fails:**
- Check internet connection
- Verify all required fields are filled
- Try reducing image count/size
- Check browser console for detailed errors

**Document analysis not working:**
- Only image formats supported (JPEG, PNG)
- PDF requires manual text extraction for now
- Ensure image is clear and readable

**Drafts not saving:**
- Check localStorage is enabled in browser
- Clear browser cache if quota exceeded
- Try incognito/private mode to test

## 🚧 Roadmap / Future Enhancements

- [ ] PDF text extraction (pdf.js integration)
- [ ] Email sending integration (Gmail, Outlook)
- [ ] Template library (pre-written email templates)
- [ ] Multi-language support (Spanish, Chinese, etc.)
- [ ] Batch processing (multiple properties)
- [ ] Agency contact database (emails, phone numbers)
- [ ] Case tracking (track progress of complaints)
- [ ] PDF export of full case file
- [ ] Integration with DoNotPay API
- [ ] Mobile app (React Native)
- [ ] Voice input (speech-to-text)
- [ ] Accessibility improvements (WCAG AA)

## 📚 Resources

### Regulatory References
- [EPA Air Quality Standards](https://www.epa.gov/criteria-air-pollutants/naaqs-table)
- [EPA Drinking Water Standards](https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations)
- [HUD Housing Quality Standards](https://www.hud.gov/program_offices/public_indian_housing/programs/hcv/hqs)
- [ASHRAE Ventilation Standards](https://www.ashrae.org/technical-resources/bookstore/standards-62-1-62-2)
- [CDC Healthy Housing Reference Manual](https://www.cdc.gov/nceh/publications/books/housing/housing.htm)

### Legal Resources
- [HUD Fair Housing Laws](https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_act_overview)
- [Nolo Tenant Rights Guide](https://www.nolo.com/legal-encyclopedia/renters-rights)
- [American Bar Association Housing Resources](https://www.americanbar.org/groups/legal_aid_indigent_defense/resource_center_for_access_to_justice/)

### Tools & APIs
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)

## 👥 Contributing

This is an open-source project. Contributions welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Add regulations for your state/locality
4. Improve prompt engineering
5. Add new document analysis types
6. Commit changes (`git commit -m 'Add AmazingFeature'`)
7. Push to branch (`git push origin feature/AmazingFeature`)
8. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Claude](https://www.anthropic.com/claude) by Anthropic
- Inspired by [DoNotPay](https://donotpay.com)
- Regulatory data compiled from EPA, HUD, CDC, state agencies
- Icon set by [Lucide](https://lucide.dev/)

## 📧 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Email: [your-support-email]
- Documentation: [your-docs-url]

---

**Built for healthier homes. Powered by AI. 🏡💚**
