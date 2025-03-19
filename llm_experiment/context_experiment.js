// Import OpenAI SDK using ES modules
import OpenAI from 'openai';

// Create OpenAI client instance
// Note: In Node.js, we often use environment variables for API keys
// You can use dotenv package to manage this
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY // Make sure to set this environment variable
});

// Helper function to make OpenAI calls and handle responses
async function askOpenAI(messages) {
  try {
    const response = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: messages
    });
    return response.choices[0].message.content;
  } catch (error) {
    console.error('Error calling OpenAI:', error);
    throw error;
  }
}

// Main async function to run our experiments
async function runExperiments() {
  try {
    // Example without context using "a"
    const responseNoContextA = await askOpenAI([
      { role: "system", content: "You are an assistant." },
      { role: "user", content: "What is a party for?" }
    ]);

    // Example without context using "the"
    const responseNoContextThe = await askOpenAI([
      { role: "system", content: "You are an assistant." },
      { role: "user", content: "What is the party for?" }
    ]);

    // Example with background context
    const responseWithContext = await askOpenAI([
      { role: "system", content: "You are an assistant." },
      { role: "user", content: "Today is Pete's 50th birthday, and Pete will take us on a tour of his ranch." },
      { role: "user", content: "What is the party for?" }
    ]);

    // Healthcare professional example
    const responseFromHealth = await askOpenAI([
      { role: "system", content: "You are an assistant." },
      { role: "user", content: `You are a virtual assistant trained as a healthcare professional 
        specializing in general wellness and preventive medicine. Your role is to provide accurate, 
        up-to-date, and practical health advice to individuals seeking to improve their overall health 
        and well-being. You are well-versed in topics such as diet, exercise, mental health, and 
        disease prevention. You base your recommendations on the latest clinical guidelines and research 
        findings in the field of medicine. Your advice is tailored to be understandable and actionable 
        by people of various health literacy levels. You aim to support individuals in making informed 
        decisions about their health and lifestyle choices` },
      { role: "user", content: "how can I organise my day?" }
    ]);

    // Print all responses
    console.log("Response without context, using 'a':");
    console.log(responseNoContextA);
    console.log("\nResponse without context, using 'the':");
    console.log(responseNoContextThe);
    console.log("\nResponse with background context:");
    console.log(responseWithContext);
    console.log("\nResponse from health professional context:");
    console.log(responseFromHealth);

  } catch (error) {
    console.error('Error running experiments:', error);
  }
}

// To use ES modules in Node.js, save this file with .mjs extension
// or add "type": "module" to your package.json
runExperiments();