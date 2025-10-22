# Long / Short Term RAG

---

The goal of this project is to implement a long and short term memory to an ai converstation to work with small models and limited context windows (e.g. Ollama)

### Short term

The short term memory will be stored as summaries in a sql table.

* Summary of human message
* Summary of ai message
* initial question
* timestamp
* session_id

### Long term

The long term memory will be stored in a vectore database. The goal is to find better context if the given summary is not enough.

* Human messages
* Ai messages
* session_id
* timestamp
