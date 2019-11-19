import re

def process_raw_vocabs(raw_vocabs):
    endtag = '#'
    new_vocabs = {}
    for vocab, cnt in raw_vocabs.items():
        word = " ".join(vocab) + " " + endtag     # add space and endtag
        new_vocabs[word] = cnt
    return new_vocabs

def get_status(vocabs):
    pairs = {}
    for vocab, cnt in vocabs.items():
        characters = vocab.split(" ")
        for i in range(len(characters) - 1):
            pair_key = (characters[i], characters[i + 1])
            if pair_key not in pairs:
                pairs[pair_key] = cnt
            else:
                pairs[pair_key] += cnt # pair count
    return pairs

def merge_vocab(best_pair, vocabs):
    new_vocabs = {}
    bigram = re.escape(" ".join(best_pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)') # construct pattern of best_pair
    for vocab, cnt in vocabs.items():
        new_vocab = p.sub("".join(best_pair), vocab) # replace seprated vocabs to a merged vocab
        new_vocabs[new_vocab] = cnt
    return new_vocabs

if __name__ == "__main__":
    raw_vocabs = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
    vocabs = process_raw_vocabs(raw_vocabs)
    print(vocabs)

    num_merges = 10
    for i in range(num_merges):
        pairs = get_status(vocabs)
        # print(pairs)
        best = max(pairs, key=pairs.get) # choose paisssr with max count
        print("best pairs:", best)
        vocabs = merge_vocab(best, vocabs)
        print(vocabs)