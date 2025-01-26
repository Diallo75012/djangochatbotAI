# Project Retrospective

## Project Progress Overview
The project aims to create a chatbot that serves as an intelligent agent for user interaction, with the following main goals:

- Streamline Business Data Interaction: Allow business users to upload data and define chatbot personalities.
- Client-User Interaction: Enable client users to interact with AI chatbots using a structured UI.
- LLM Integration: Use Rust for handling complex LLM API calls for efficient and optimized performance.
- Multi-Purpose Agents: Create agents that can handle not only chat interaction but also log processing and generating operational reports.

### Challenges Encountered and Solutions Implemented

1. **Setting Up the Chat Flow Between Frontend and Backend**

#### Challenge: Initially, the chat interface wasn't connected well with the backend, causing incomplete information to appear, and the entire web UI would sometimes be replaced by returned messages.
  **Solution**:
    - Utilized AJAX for smooth interactions without reloading the page.
    - Modified Django views to return JSON responses properly instead of rendering full-page responses that broke the front-end UI.
    - Leveraged a cache mechanism to persist messages, allowing users to revisit the chat and find their previous conversations intact.

2. Rust Integration with Django
#### Challenge: Integrating Rust via PyO3 and Maturin to handle LLM API calls presented multiple challenges, such as compilation errors, handling Rust-Python bindings, and ensuring smooth JSON serialization and deserialization.
  **Solutions**:

   Library Development and Setup:
     - Created a Rust library using Maturin to integrate with Django.
     - Deployed the library by compiling it through Maturin, ensuring proper linkage to Python environments.

   Error Handling and Match Statements:
     - Pivoted from using .unwrap() to match statements for error handling in Rust, ensuring a more robust solution suitable for production.
     - Instead of directly parsing responses via struct fields (which initially caused missing fields), decided to return raw responses for flexibility and simplicity.

   Debugging and Logging:
     - Added log files to trace the flow within Rust, as print statements in Rust weren’t visible when called from Python. Enhanced robustness by avoiding .unwrap(), and ensured logging by properly handling file operations in Rust.

3. Web UI and Template Consistency
#### Challenge: Consistencies in web templates, like image paths not showing up properly or fields being inconsistent between the front-end and Django context.
  **Solution**:
    - Updated paths in templates to use full /static/images/... paths to ensure proper asset loading.
    - Resolved discrepancies with JavaScript fetching incorrect data from form elements due to typos and inconsistent camelCase/snake_case usage.

4. User Experience and Data Flow Consistency
#### Challenge: The requirement to maintain AI personality settings that align well with each document uploaded by business users.
  **Solution**:
    - Implemented default chatbot settings in the sidebar that can be modified or overridden by client users as needed.
    - Created custom personality settings for users when a default was absent, adding flexibility in the interaction.
    - Fetched chatbot details dynamically with a dropdown, using JavaScript to request settings from Django endpoints.

## Pivots and Refactoring Decisions

1. Consolidating Rust Functions
The initial implementation had separate functions for each LLM API call, like Groq and Ollama. Eventually, it made sense to consolidate them into a single function that could handle any LLM API call.

- Reason: Reduced code redundancy and allowed a more scalable architecture for adding new LLMs in the future without duplicating logic.

2. Moving Towards Decoupled Agent Management
- Consideration: Whether to put agents into the common app or create a dedicated app.
- Reasoning: Since LLM and agent technologies evolve rapidly, decoupling would allow for better maintainability and future changes without significantly refactoring the entire project.

3. Rust Taking Over Heavy Lifting
Moving computationally intensive or latency-sensitive tasks (like LLM API calls, embeddings, and retrievals) to Rust was a conscious decision to benefit from Rust's performance.
This led to refactoring Python-heavy tasks to rely on Rust for core computations and maintain Python's role as the orchestrator for managing interactions between different services.

## Future Direction and Recommendations

1. Rust for Embedding and Retrieval
Plan to add more functions in Rust to handle embedding generation and vector search for retrieval.
  **Recommendation**:
    - Encapsulate these functions into specific, focused modules for embeddings and retrievals.
    - Ensure the functions have clear inputs and outputs to maintain reusability.

2. Decoupling Agent Logic
You need to decide between putting the agents in the common app or creating a new agents app.
  **Recommendation**:
    - Create a Dedicated agents App: This will allow better decoupling and future portability if you decide to split your system into microservices or introduce new technologies.
    - Why: Agents are a unique abstraction, distinct from common utilities. Having them in their own app allows for better modularity, testing, and the possibility of containerizing or deploying them separately in the future.

3. User Flow from Data Entry to Chat Interaction
The final goal is to allow business users to input data, set up AI personalities, and let client users interact with the documents.
  **Recommendation**:
    - Data Storage: Store document data in Postgres, with vector embeddings in pgvector for RAG (Retrieval Augmented Generation).
    - Dynamic Personality Settings: Allow chatbot personalities to be adjusted dynamically through the chat interface. This can be helpful if businesses have frequent changes in branding.
    - LangGraph Integration: Use LangGraph to create agents with specialized tasks (document retrieval, external search, etc.). Set up rules to determine when an agent should call Rust functions for embeddings, retrieval, or LLM responses.

4. Rust and Python Roles Clarification
- Rust: Focus on computational-heavy tasks, e.g., LLM API calls, embedding generations, file reading, etc.
- Python/Django: Coordinate user interactions, orchestrate data flow, manage agents, and ensure that the right API call is made based on the context.

5. Log-Based Agent Reporting
You plan to create another stream where logs are analyzed by LLM agents and reports are periodically generated for DevOps.
  **Recommendation**:
    - Store logs as structured files (e.g., JSON or CSV) so that LLMs can easily interpret them.
    - Use Django for task scheduling (like Celery) to automate periodic log analysis.
    - Use Rust for efficient file reading and batch processing of log data to reduce the burden on Python.

## Summary
Your project has evolved significantly, adapting Rust for performance, refining Django to manage interactions, and ensuring a consistent user experience on the web UI. Pivots were necessary to align technologies with the vision of scalable and maintainable software. Moving forward, focus on modularity, optimizing computational tasks with Rust, and maintaining Python as the central orchestrator. Given your plans, having a dedicated agents app and leveraging Rust for performance-critical functions aligns well with your end goals of flexibility, scalability, and future adaptability.



