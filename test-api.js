// Quick test script to verify API integration works
// Run with: node test-api.js

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_VERSION = '2023-06-01';
const MODEL = 'claude-sonnet-4-5-20250929';

// Test API key (replace with real key to test)
const TEST_API_KEY = process.env.ANTHROPIC_API_KEY || 'sk-ant-test-key-here';

async function testAPI() {
  console.log('Testing Claude API integration...');
  console.log('Model:', MODEL);
  console.log('API URL:', ANTHROPIC_API_URL);
  console.log('API Key (first 10 chars):', TEST_API_KEY.substring(0, 10) + '...');

  const requestBody = {
    model: MODEL,
    max_tokens: 100,
    temperature: 1,
    system: 'You are a helpful assistant.',
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: 'Say "API test successful" and nothing else.'
          }
        ]
      }
    ]
  };

  console.log('\nRequest body:', JSON.stringify(requestBody, null, 2));

  try {
    const response = await fetch(ANTHROPIC_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': TEST_API_KEY,
        'anthropic-version': ANTHROPIC_VERSION
      },
      body: JSON.stringify(requestBody)
    });

    console.log('\nResponse status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    const data = await response.json();
    console.log('\nResponse data:', JSON.stringify(data, null, 2));

    if (response.ok) {
      console.log('\n✅ SUCCESS! API is working correctly.');
      console.log('Response text:', data.content?.[0]?.text);
    } else {
      console.log('\n❌ ERROR! API returned error.');
      console.log('Error:', data.error);
    }
  } catch (error) {
    console.error('\n❌ EXCEPTION:', error.message);
    console.error('Stack:', error.stack);
  }
}

testAPI();
