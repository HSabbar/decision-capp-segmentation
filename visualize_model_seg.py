import gensim
import evaluate
import utils
from pathlib2 import Path
from argparse import ArgumentParser
import torch
import choiloader
import numpy as np

goldset_delimiter = "********"
section_delimiter = "========"

def segment(path, model, word2vec, output_folder):
    file_id = str(path).split('/')[-1:][0]

    splited_sentences, target, _ = choiloader.read_choi_file(path, word2vec, False, False)

    sentences = [' '.join(s) for s in splited_sentences]
    gold_set = np.zeros(len(splited_sentences)).astype(int)
    gold_set[np.asarray(target)] = 1



    cutoffs = evaluate.predict_cutoffs(sentences, model, word2vec)
    total = []
    segment = []
    for i, (sentence, cutoff) in enumerate(zip(sentences, cutoffs)):
        segment.append(sentence)
        if cutoff or gold_set[i] == 1:
            full_segment ='\n'.join(segment) + '.\n'
            if cutoff:
                full_segment = full_segment + '\n' + section_delimiter + '\n'
                if gold_set[i] == 1:
                    full_segment = full_segment + goldset_delimiter + '\n'
            else:
                full_segment = full_segment + '\n' +  goldset_delimiter + '\n'
            total.append(full_segment + '\n')
            segment = []



    # Model does not return prediction for last sentence
    segment.append(sentences[-1:][0])
    total.append('.'.join(segment) + '\n')

    output_file_content = "".join(total)
    output_file_full_path = Path(output_folder).joinpath(Path(file_id))

    print(output_file_full_path)
    with output_file_full_path.open('w') as f:
        f.write(output_file_content)

def main(args):
    utils.read_config_file(args.config)
    utils.config.update(args.__dict__)

    with Path(args.file).open('r') as f:
        file_names = f.read().strip().split('\n')

    word2vec = None

    with open(args.model, 'rb') as f:
        model = torch.load(f)
        model.eval()


    for name in file_names:
        if name:
            segment(Path(name), model, word2vec, args.output)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--model', help='Model to run - will import and run', required=True)
    parser.add_argument('--config', help='Path to config.json', default='config.json')
    parser.add_argument('--file', help='file containing file names to segment by model', required=True)
    parser.add_argument('--output', help='output folder', required=True)


    main(parser.parse_args())
