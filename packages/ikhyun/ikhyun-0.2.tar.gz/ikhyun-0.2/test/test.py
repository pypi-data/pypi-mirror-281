from ikhyun.data.tn_dataset_builder import LoaderInterface, WriterInterface, TextNormDatasetBuilder, MetaMap, MetaValue
from ikhyun.normalization import Normalizer
from ikhyun.normalization.filter import ko_filter
from logging import Logger
import re
from pathlib import Path
import csv
from tqdm import tqdm


class SHLoader(LoaderInterface):
    file_path = None

    def __init__(self, file_path):
        self.file_path = file_path

    @overrides
    def __call__(self, logger:Logger) -> MetaMap:
        meta = MetaMap()
        han_re = re.compile(r"^[가-힣\s.,!?\'\"]+$")
        trs_re = re.compile("[a-zA-Z\d]")
        #processor = MosesTokenizer(lang = "ko")

        logger.info("Searching json files...(%s)", self.file_path)
        path = Path(self.file_path)

        norm = Normalizer()
        norm.set({"ko_magic_filter": ko_filter})

        #self.logger.debug(path)
        with path.open(encoding = 'utf-8-sig') as f:
            reader = csv.reader(f, delimiter='\t')

            for i, row in tqdm(enumerate(reader), desc = f'Loading : {self.file_path}'):
                org_str = norm(row[1])
                trs_str = norm(row[0] if trs_re.search(org_str) else org_str)
                #org_str = processor.tokenize(org_str, return_str = True)
                #trs_str = processor.tokenize(trs_str, return_str = True)


                if not han_re.match(trs_str):
                    logger.warning("Invalid TransLabelText : %s", trs_str)
                    continue
                meta[org_str] = MetaValue(org_str, trs_str)
        return meta

class NeMoWriter(WriterInterface):
    def __init__(self, file_path, sils):
        self._file_path = file_path
        self._sils = sils

    @overrides
    def __call__(self, sents, logger):
        with open(self._file_path, 'w', newline="", encoding="utf-8") as fout:
            writer = csv.writer(fout, delimiter='\t')
            writer.writerow(['Semiotic Class', 'Input Token', 'Output Token'])
            for sent in tqdm(sents, desc = f'Writing : {self.file_path}'):
                for words in sent:
                    if words['matched_org_seq'] in self._sils:
                        writer.writerow(["PUNCT", words['matched_org_seq'], "sil"])
                    elif words['matched_org_seq'] ==  words['matched_trs_seq']:
                        writer.writerow(["PLAIN", words['matched_org_seq'], "<self>"])
                    else: # 태그 여부와 상관 없이 org와 trs가 다른경우
                        if len(words['matched_org_seq']) == 1 and not words['matched_trs_seq'].strip(): # sil.
                            writer.writerow(['PUNCT', words['matched_org_seq'], "sil"])
                        elif words['matched_cls'][0][2:]: # NER 태그가 존재할 경우
                            writer.writerow([words['matched_cls'][0][2:], words['matched_org_seq'], words['matched_trs_seq']])
                        elif words['matched_trs_seq'].strip(): # NER 태그는 없지만 org와 trs가 다르고 trs가 sil이 아닌경우
                            writer.writerow(['OT', words['matched_org_seq'], words['matched_trs_seq']])
                        else:
                            logger.warning(f'Unexpected case detected [{words}], [{sent}]')

                writer.writerow(['<eos>', '<eos>'])
def main():

    sils =[",","\'", "\"","!","?", "."]
    loader = SHLoader1("./label.csv")
    writer = NeMoWriter("./res.csv", sils)
    builder = TextNormDatasetBuilder(
        'Leo97/KoELECTRA-small-v3-modu-ner',
        loader,
        writer,
        batch_size = 32,
        device = 'cuda')

    aligned_res = builder.process(8)

    builder._write(aligned_res)

if __name__ == '__main__':
    main()
