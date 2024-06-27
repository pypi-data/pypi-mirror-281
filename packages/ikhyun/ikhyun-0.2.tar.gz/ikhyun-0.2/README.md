# Ikhyunss utils

TN, ITN 데이터셋 생성기

## Installation

You can install the package using `pip`:
```sh
pip install ikhyun
```

## Usage

```python
from ikhyun.data.tn_dataset_builder import LoaderInterface, WriterInterface, TextNormDatasetBuilder, MetaMap, MetaValue

class MyLoader(LoaderInterface):

    def __call__(self, logger:Logger) -> MetaMap:
        ## Override this method to load a file and return MetaMap.
        return meta


class MyWriter(WriterInterface):

    def __call__(self, sents, logger):
        ## Override this method to process setns.

def main():

    loader = MyLoader()
    writer = NeMoWriter()
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
```