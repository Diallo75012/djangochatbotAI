# **Agile Retrospective Report**

1. **What Went Well** 🌟
- Successfully identified and isolated issues with PostgreSQL pgvector collections and overlapping embeddings.
- Implemented a clean approach to ensure unique document IDs using a combination of `business_document_uuid` and incremental counts to avoid ID collisions across collections.
- Integrated the use of formatted collection names using a normalization function to standardize collection names and prevent duplication or inconsistencies.
- Handled missing chatbot data gracefully by adding a robust fallback mechanism using `DEFAULT_AI_PERSONALITY_TRAIT`.
- Developed a deeper understanding of how `langchain_pg_embedding` stores documents and metadata, as well as how it behaves with overriding and re-embedding processes.


2. **Challenges Encountered** 🛠️
|Challenge   |How It Was Resolved   |
|---|---|
|Overlapping Embeddings: Documents from different collections appeared under incorrect collections due to shared IDs.    | Used a combination of unique `business_document_uuid` + incremental counter to generate distinct document IDs.  |
|---|---|
|Collection Name Inconsistencies: Mixed use of quotes ("") and case sensitivity caused unpredictable behavior in embedding storage.   | Implemented a normalization function to clean and standardize collection names before embedding.  |
|---|---|
| Default Chatbot Configuration: Missing chatbot settings caused errors when loading avatars or attributes in the UI. | Added fallback logic to load chatbot traits from environment variables (`DEFAULT_AI_PERSONALITY_TRAIT`). |
|---|---|
| Embedding Update Confusion: Re-embedding with the same collection name caused uncertainty about whether it replaces or appends data. | Confirmed that pgvector does not automatically replace embeddings and added documentation for clear behavior. |


3.**Decision-Making Process** 🤔
- Approach to Challenges:
  - I took an iterative and investigative approach:
    Observation: Reproduced errors, analyzed database behaviors, and checked how pgvector stores and retrieves embeddings.
    Documentation: Researched official documentation for LangChain’s pgvector integration and psycopg3’s behavior.
    Root Cause Analysis: Narrowed down the issues to ID conflicts, non-standardized collection names, and missing data handling.

- Solution Design: 
  - Decided to:
    Use unique IDs (business_document_uuid) to ensure no overlap.
    Normalize collection names to maintain consistency.
    Add fallback defaults for missing chatbot configurations.

- Validation: Tested embedding, retrieval, and the UI under multiple edge cases to confirm fixes worked as expected.

- Decision Framework:
  - Always prioritize data consistency in the database.
  - Ensure changes align with future scalability.

- Maintain simplicity: Small, incremental fixes rather than refactoring entire processes unnecessarily.


4. **Progress Made** 🚀
- Embeddings Process: Improved reliability by generating unique IDs and standardizing collection names.
- Error Handling: Reduced UI and backend failures by robust fallback defaults for missing configurations.
- Understanding of pgvector: Gained insights into how pgvector behaves with updates, IDs, and collections.
- Code Clarity: Streamlined processes while maintaining clean, well-documented code.


5. **What Can Be Improved** ✨

  1. Automate Re-embedding for Updates
    If a business user updates their data, an automated pipeline to clear the old embeddings and re-embed with the new data could save manual work.
    Use a clear naming convention or versioning for collections to prevent confusion.
  2. Enhance Database Monitoring
    Implement logs or alerts to monitor when embeddings or collections overlap or behave unexpectedly.
    Use database queries to confirm consistency after re-embedding processes.
  3. Simplify Decision-Making for Updates
    Instead of appending or overriding manually, build helper functions or workflows:
    A “replace collection” function to drop and recreate embeddings for updates.
    A “merge collection” function to append new embeddings to existing data.
  4. Documentation and Testing
    Document the embedding and retrieval process clearly for future reference.
    Add more unit tests for edge cases like:
    Missing chatbot settings.
    Overlapping document IDs.
    Partial embedding failure.
   5. Productivity Tip
    Time-Box Investigations: Allocate a fixed amount of time for debugging before seeking external help or refactoring. This prevents getting stuck too long on one issue.
    Automate Simple Tasks: Use scripts for repetitive tasks like embedding data, clearing old collections, or validating database states.

6. **Final Notes** 📝
You are successfully building a system that balances robustness and flexibility.
By addressing challenges iteratively and ensuring no data collisions occur,
your process is becoming more reliable. 

Focus on improving productivity by automating repetitive processes, documenting workflows,
and introducing small helpers for decision-making.

Keep iterating at your own pace – it’s better to do things the way you want but make incremental improvements that save you time and energy in the long run.
