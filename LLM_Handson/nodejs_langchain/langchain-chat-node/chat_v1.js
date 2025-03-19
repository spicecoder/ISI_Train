// chat_v1.js
import dotenv from 'dotenv';
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import readline from 'readline';

// Load environment variables
dotenv.config();

// Create readline interface for command line input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function createChat() {
    return new ChatOpenAI({
        temperature: 0.7
    });
}

// Promise wrapper for readline
function askQuestion(query) {
    return new Promise((resolve) => {
        rl.question(query, resolve);
    });
}

async function main() {
    const chat = createChat();
    
    console.log("Welcome to SimpleChat! (type 'quit' to exit)");
    
    while (true) {
        const userInput = await askQuestion("\nYou: ");
        
        if (userInput.toLowerCase() === 'quit') {
            break;
        }
        
        try {
            const messages = [
                new SystemMessage("You are a helpful AI assistant."),
                new HumanMessage(userInput)
            ];
            
            const response = await chat.invoke(messages);
            console.log(`\nAssistant: ${response.content}`);
        } catch (error) {
            console.error("\nError:", error.message);
        }
    }
    
    rl.close();
}

// Add this to package.json to accomodate import: { "type": "module" }
main().catch(console.error);