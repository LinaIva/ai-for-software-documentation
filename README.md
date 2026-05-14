# AI for software documentation

## Project Description

This project explores the use of artificial intelligence in software documentation and code comprehension, with a focus on source code summarization. The current implementation investigates how large language models can generate concise natural-language summaries of Python code. The project also explores retrieval-based context enhancement and evaluation methods for comparing generated summaries with reference documentation.
## Goal

Design and implement an AI-based solution for software documentation and code comprehension.

## Selected Subtask

- Automated source code summarization
- Prompt-based documentation generation
- Summarization with additional context from similar code examples
- Evaluation of generated summaries with text similarity metrics

## Evaluation

The current prototype is evaluated by comparing generated summaries with reference summaries from the dataset. The evaluation currently includes:

- BLEU
- METEOR
- ROUGE

The project also compares different summarization strategies, including zero-shot prompting, few-shot prompting, the ROSES framework, and Retrieval-Augmented Generation(RAG).

## Future work

- Extend the comparison of prompting strategies
- Explore an agent-based approach using LangGraph
- Evaluate whether the agent-based approach improves summarization quality

## Requirements
- Python 3.10 or newer
- An OpenAI API key for running the summarization scripts
- Python packages listed in `requirements.txt`
- Downloaded NLTK resources required for evaluation
- Internet access for calling the OpenAI API and downloading models on first use

This project uses:
- `openai` for LLM-based summary generation
- `sentence-transformers` for code embeddings
- `qdrant-client` for local vector storage and retrieval
- `nltk`, `rouge-score`, and `scikit-learn` for evaluation and similarity analysis
- `pandas` and `matplotlib` for dataset exploration

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/LinaIva/ai-for-software-documentation.git
```

### 2. Create a `.env` file
In order to utilize OpenAI API, you need to copy `.env.example` to `.env` and set the `OPENAI_API_KEY`.
Create a .env file in the project root and add your OpenAI API key:

`OPENAI_API_KEY=your_api_key_here`

Make sure `.env` is included in `.gitignore`.

### 3. Install dependencies
Install required Python packages:

```bash
pip install -r requirements.txt
python setup_nltk.py
```

### Notes
- The `.env` file should never be committed to GitHub
- API keys must remain private

## Weekly Progress Journal

### Week 1
- Searched for relevant papers in IEEE Xplore
- Collected several papers on software documentation to understand their inputs, outputs, and overall research direction
- Started the literature review in this area
- Set up Firefox proxy access for article retrieval

### Week 2
- Explored 1-2 papers in more detail and discussed them
- Looked for key papers on LLM-based software documentation, including arXiv versions, preprints, reviews, and related work on code summarization
- Created a Python script capable of calling an LLM and returning a response

### Week 3
- Read three selected papers in preparation for discussion
- Analyzed the main research problem, approach, datasets, evaluation metrics, and baselines used in these papers
- Implemented an initial demo for LLM-based code summarization using zero-shot and few-shot prompting
- Prepared multiple prompts and examples for experimentation

### Week 4
- Ran an existing project and analyzed where its weakest evaluation results appeared and whether they could be improved
- Studied LangGraph and explored the idea of adding a custom agent
- Investigated LangGraph graph visualization for showing agent communication
- Implemented a simple RAG-style experiment by selecting relevant examples from a larger set
- Continued selecting and filtering relevant articles

### Week 5
- Implemented a function for comparing expected documentation with generated documentation
- Added similarity evaluation metrics: BLEU, METEOR, and ROUGE
- Returned the results in a structured form for later evaluation of summarization quality

### Week 6
- Explored text embeddings and vector representations using a Sentence-BERT embedding model
- Calculated cosine similarity between text representations
- Studied Average Token Overlap and considered integrating it into the evaluation code
- Continued working with RAG and gained a clearer understanding of vector databases
- Revisited the selected papers and narrowed down the most relevant one

### Week 7
- Refactored the RAG implementation
- Improved zero-shot prompting so that the user does not need to manually prepare all inputs
- Implemented a zero-shot prompting variant based on the ROSES framework
- Moved prompts into a centralized structure such as a field or JSON-like collection
- Continued reading related papers
- Identified LangGraph as a remaining task for future work

### Week 8
- Continued work on prompt structure organization using object- or dictionary-based representations
- Looked for a suitable dataset containing many code-summary pairs
- Investigated vector database technology to make retrieval more efficient

### Week 9
- Improved the prompt configuration structure using dictionary-based objects
- Analyzed the distribution of lines of code and summary lengths for both datasets
- Studied the paper "Using an LLM to Help with Code Understanding"
- Read about CodeXGLUE and identified its dataset relevance for this project

### Week 10
- Continued reading and reviewing the selected papers
- Presentation

## Future Work
- Develop a more advanced documentation assistant based on DocAgent using LangGraph
- Evaluate whether the agent-based approach improves summarization quality and usability
- Compare different prompting strategies
- Analyze the advantages and limitations of the different approaches

## Technologies Used

- Python
- OpenAI API
- LangGraph
- Sentence Transformers
- Qdrant
- NLTK
- ROUGE
- scikit-learn
- pandas
- matplotlib
- datasets
