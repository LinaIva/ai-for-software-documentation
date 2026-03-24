# AI for software documentation

## Requirements
...

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