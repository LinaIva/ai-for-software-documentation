from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import nltk


def evaluateSimilarity(reference: str, generated: str) -> dict:
    referenceTokens = nltk.word_tokenize(reference)
    generatedTokens = nltk.word_tokenize(generated)
    # BLEU
    smoothie = SmoothingFunction().method1
    bleu = sentence_bleu([referenceTokens], generatedTokens, smoothing_function=smoothie)
    # METEOR
    meteor = meteor_score([referenceTokens], generatedTokens)
    # ROUGE
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge_scores = scorer.score(reference, generated)

    overlap = averageTokenOverlap(referenceTokens, generatedTokens)
    return {
        "bleu": round(bleu, 4),
        # BLEU - степень совпадения n-грамм (насколько текст похож по словам и фразам)
        # BLEU - miera zhody n-gramov (ako veľmi sa texty zhodujú v slovách a frázach)
        "meteor": round(meteor, 4),
        # METEOR - учитывает совпадения слов, порядок и частично смысл (более гибкая метрика)
        # METEOR - zohľadňuje zhodu slov, ich poradie a čiastočne význam (flexibilnejšia metrika)
        "rouge1": round(rouge_scores["rouge1"].fmeasure, 4),
        # ROUGE-1 - совпадение отдельных слов (unigram overlap)
        # ROUGE-1 - zhoda jednotlivých slov (unigramy)
        "rouge2": round(rouge_scores["rouge2"].fmeasure, 4),
        # ROUGE-2 - совпадение пар слов (bigram overlap)
        # ROUGE-2 - zhoda dvojíc slov (bigramy)
        "rougeL": round(rouge_scores["rougeL"].fmeasure, 4),
        # ROUGE-L - совпадение по самой длинной общей последовательности слов
        # ROUGE-L - zhoda podľa najdlhšej spoločnej postupnosti slov
        "rouge_scores": rouge_scores,
        # Полный объект с ROUGE (precision, recall, fmeasure)
        # Kompletné ROUGE skóre (precision, recall, f-measure)
        "token_overlap": round(overlap, 4),
        # Average Token Overlap - доля общих слов между текстами
        # Average Token Overlap - podiel spoločných slov medzi textami
    }

def averageTokenOverlap(referenceTokens, generatedTokens):
    refSet = set(referenceTokens)
    genSet = set(generatedTokens)
    intersection = refSet.intersection(genSet)
    union = refSet.union(genSet)
    if len(union) == 0:
        return 0.0
    return len(intersection) / len(union)


if __name__ == "__main__":
    expected_doc = "This function sorts a list of integers in ascending order."
    generated_doc = "Sorts the input list of numbers in increasing order."
    # expected_doc = "The cat is on the table."
    # generated_doc = "The cat is here."
    # expected_doc = "The cat is on the table."
    # generated_doc = "My bird likes to be at home."
    res = evaluateSimilarity(expected_doc, generated_doc)
    print(res)
    for i, j in res.items():
        print(f'{i}: {j}')