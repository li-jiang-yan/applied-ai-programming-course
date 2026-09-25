# Applied AI Studio labs

Extract the complete archive; keep the `labs` directory together. Run commands from inside `labs`. Use Python 3.11 and one virtual environment per module. Windows commands use `.venv\Scripts\python.exe`; on macOS/Linux substitute `.venv/bin/python`.

The website contains the ordered steps and expected results. Model-backed scripts require internet access for packages, weights, or hosted inference. Hosted calls can incur charges. No credentials are bundled. Set model IDs available to your account, as described in Module 1. The course uses only fictional policy data.

Dependency files express compatible major-version ranges, not a tested lockfile. After a successful installation, save `python -m pip freeze > environment-lock.txt` alongside your results. The authoring checks validate Python syntax and the offline agent/retrieval exercises; hosted calls and model training have not been executed as part of authoring.

- Module 1: `module01/providers.py`, `chain.py`, `private_qa.py`, `app.py`
- Module 2: `module02/backend.py`, `gradio_app.py`, `streamlit_app.py`
- Module 3: `module03/call_flow.py`; reuse Module 1's chain and private QA
- Module 4: `module04/retrieval.py`, `rag.py`, `tune_retriever.py`
- Module 5: `module05/train_sentiment.py`, `train_lm.py`, `train_ner.py`
- Module 6: `module06/agent.py`, `bandit.py`

Stop local servers with Ctrl+C. Delete a lab virtual environment only when you no longer need it; retain your report, source, model configuration, and package lockfile.
