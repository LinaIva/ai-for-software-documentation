import pandas as pd
import matplotlib.pyplot as plt


CODEXGLUE_PATH = "datasets/train.jsonl"
PSUM_PATH = "datasets/python_summary_synth_data.csv"

def clean_code(code):
    code = str(code)
    code = code.replace("<br>", "\n")
    code = code.strip()
    if code.startswith("python"):
        code = code[len("python"):]
    return code


def count_loc(code):
    code = clean_code(code)
    lines = code.split("\n")
    lines = [line for line in lines if line.strip()]
    return len(lines)

def count_words(text):
    return len(str(text).split())

def analyze_dataset(df, code_col, summary_col, dataset_name):
    df = df.copy()
    df["loc"] = df[code_col].apply(count_loc)
    df["summary_words"] = df[summary_col].fillna("").apply(count_words)
    print(f"\n===== {dataset_name} =====")
    print("\nLOC:")
    print("min:", df["loc"].min())
    print("max:", df["loc"].max())
    print("mean:", df["loc"].mean())
    print("\nSummary length:")
    print("min:", df["summary_words"].min())
    print("max:", df["summary_words"].max())
    print("mean:", df["summary_words"].mean())
    return df


def plot_distribution(df, column, title, xlabel, percentile_limit=0.95, bins=50):
    values = df[column].dropna()
    if values.empty:
        return

    upper_bound = values.quantile(percentile_limit)
    filtered_values = values[values <= upper_bound]

    plt.figure()
    counts, _, _ = plt.hist(filtered_values, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.xlim(0, upper_bound)
    if len(counts) > 0:
        plt.ylim(0, max(counts) * 1.1)
    plt.show()

def print_examples(df, code_col, summary_col, dataset_name):
    print(f"\n===== EXTREMES: {dataset_name} =====")
    min_loc_idx = df["loc"].idxmin()
    max_loc_idx = df["loc"].idxmax()
    print("\n--- Shortest code ---")
    print("LOC:", df.loc[min_loc_idx, "loc"])
    print(df.loc[min_loc_idx, code_col])
    print("\n--- Longest code ---")
    print("LOC:", df.loc[max_loc_idx, "loc"])
    print(df.loc[max_loc_idx, code_col])
    min_sum_idx = df["summary_words"].idxmin()
    max_sum_idx = df["summary_words"].idxmax()
    print("\n--- Shortest summary ---")
    print("Words:", df.loc[min_sum_idx, "summary_words"])
    print(df.loc[min_sum_idx, summary_col])
    print("\n--- Longest summary ---")
    print("Words:", df.loc[max_sum_idx, "summary_words"])
    print(df.loc[max_sum_idx, summary_col])



# 1. CodeXGLUE dataset

codexglue_df = pd.read_json(CODEXGLUE_PATH, lines=True)

codexglue_df = analyze_dataset(
    codexglue_df,
    code_col="code",
    summary_col="docstring",
    dataset_name="CodeXGLUE Python"
)



# 2. dataset

synth_df = pd.read_csv(PSUM_PATH)

synth_df = analyze_dataset(synth_df, code_col="prompter", summary_col="assistant",
                           dataset_name="guidevit/python_code_summarization")

# Графики

plot_distribution(
    codexglue_df,
    "loc",
    "LOC distribution - CodeXGLUE",
    "Lines of code"
)

plot_distribution(
    codexglue_df,
    "summary_words",
    "Summary length - CodeXGLUE",
    "Words"
)

plot_distribution(
    synth_df,
    "loc",
    "LOC distribution - guidevit/python_code_summarization",
    "Lines of code"
)

plot_distribution(
    synth_df,
    "summary_words",
    "Summary length - guidevit/python_code_summarization",
    "Words"
)

print_examples(
    codexglue_df,
    code_col="code",
    summary_col="docstring",
    dataset_name="CodeXGLUE Python"
)

print_examples(
    synth_df,
    code_col="prompter",
    summary_col="assistant",
    dataset_name="guidevit/python_code_summarization"
)
