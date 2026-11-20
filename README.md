# LLM Cost Tracker

A Python project that compares responses from two LLM providers: Google Gemini and Groq.

It tracks input and output tokens, measures response time, and calculates the estimated API cost for each provider. The results help understand the differences in token usage, speed, and cost between LLM providers.


## How to Run

1. Configure environment variables
Create a .env file in the project directory and add your API keys and model names.

2. Run the project

```bash
uv run tracker.py "Explain Agentic Ai in one paragraph."
```

## Sample Output
```text

--- GEMINI RESPONSE ---
**Agentic AI** refers to advanced artificial intelligence systems designed to act autonomously as goal-driven agents capable of making decisions, solving problems, and executing complex workflows with minimal human intervention. Unlike traditional AI that merely generates passive responses to static prompts, agentic AI can break down high-level objectives into smaller tasks, dynamically reason through options, utilize external tools (such as APIs or software applications), and adapt its strategy based on real-world feedback. This shift transforms AI from a simple, reactive assistant into a proactive partner capable of independently managing end-to-end operations from start to finish.

--- GROQ RESPONSE ---
Agentic AI refers to artificial intelligence systems designed to act with a sense of agency—meaning they possess autonomy, intentionality, and the capacity to pursue goals in a dynamic environment. Unlike conventional tool‑centric models that simply execute pre‑programmed instructions, agentic AI can form and revise internal objectives, make decisions based on context and experience, adapt strategies, and even initiate self‑improvement processes or resource acquisition. This autonomous behavior is often grounded in reinforcement learning, hierarchical planning, or evolutionary algorithms that enable the system to act as a self‑directed agent, capable of influencing its surroundings, learning from outcomes, and aligning its actions with higher‑level aims, thereby blurring the line between tool and autonomous actor.

--- PROVIDER COMPARISON ---
Provider    Input Tokens    Output Tokens    Seconds     Cost (USD)     
------------------------------------------------------------------------
Gemini      8               119              81.78       $0.00045225    
Groq        78              274              0.95        $0.00008805    


```

## What I Learned

- I learned how to track token usage, measure response time, and calculate estimated API costs.
- Different LLM providers can use different numbers of tokens for the same input