# Agentic

Agentic is an open-source Python-only multi-agent framework designed to be built for production-ready tool use cases.

Agentic provides: 
- A frontend purpose-built for testing agents
- Multi-agent paradigm following the Agent Protocol[1]
- Built-in easy deployment
- Configurable LLM abstractions
- Agent observability layer and tracing
- an API for your agent once deployed to easily work through things 
- A batteries-included agentic memory database (Knowledge-graph NOT vector databases are more similar to our biological memory.)

It is (in essence) an end-to-end agent framework that you can deploy

## Why Agentic

Most people building agents are rarely ever building it for themselves.
Usually, they built it with other people but they're stuck in their CLIs.
Furthermore - a large ecosystem of tools exists that do NOT exist in Python and so
these tools would benefit greatly from a GRPC agent-tool solution.

Some design choices we are making: 

- An opinionated front-end inspired by Chainlit
- An opinionated agent protocol inspired by LangRoid
- An opinionated deployment strategy inspired by some of the work that we are doing at Nullify AI

## Architecture

Agentic takes in best-in-class tooling across the stack. 

More specifically, we use: 
- Reflex for frontend (specifically their chat frontend for now but heavily inspired by ChainLit and StreamLit)
- LangRoid-inspired multi-agent protocol
- LogFire for observability
- GRPC for tool-calling with examples in Golang and TypeScript

## Design choices

- We did not use poetry because Reflex wasn't supported there, so we opted instead for a simple `pip install XYZ` instead.

### Why Knowledge Graphs and not Vector Databases

Let's start with proof by contradiction. You need to recall "What food did James order?" 
A vector database gives you a cosine similarity distance between embeddings. 

Great - now you have 10 solutions. Then you change it to a hybrid search to filter for the exact date. 

And then you get your answer.

Works well for a simple use case. But now let's try and think to a specific time in memory. 

All of a sudden - you realise vector databases can't really filter for it. 

Then you realize they're really only useful for vector recommendations.

## Okay - so how do you maek money?

Not really sure yet. Most likely by providing free, effortless deployment. 
Or excellent tools.
Or nice frontend components.

But the core of this framework will always remain open-source (not just source-available). We git-committed this so we sorta have
to stick to it. Sorry VCs.
