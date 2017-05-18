import pandas
import os
from .resources import resources
from clinvoc.ndc import NDC
import pickle
from clinvoc.code_collections import CodeCollection
from clinvoc.base import left_pad
from . import __version__
from ._version import get_versions

def _process_drug_file():
    try:
        with open(os.path.join(resources, 'cache.pickle'), 'rb') as infile:
            result, v = pickle.load(infile)
        assert v == __version__
        assert not get_versions()['dirty']
        return result
    except:
        ndf = pandas.read_excel(os.path.join(resources, 'NDF_January_2016.xlsx'), sheetname='Sheet1', )
        vocab = NDC()
        va_class = {}
        for _, row in ndf.iterrows():
            # Some rows are malformed.  Correct them.
            if '^' in str(row['NDC_1']):
                row_list= list(row)
                assert row['NDC_1'] == row_list[0]
                row_ = pandas.Series((row_list[0].split('^') + row_list[1:])[:len(row_list)], index=row.index)
            else:
                row_ = row
            
            cls = row_['VA_CLASS']
            ndc = vocab.standardize(left_pad('%.11s' % int(row_['NDF_NDC']), 11))
            
            if (cls, vocab.vocab_name) in va_class:
                va_class[(cls, vocab.vocab_name)].add(ndc)
            else:
                va_class[(cls, vocab.vocab_name)] = {ndc}
                
        # Don't need the special case because not attempting to map between "classes" and "categories"
    #     # Correct one special case
    #     va_class['NONSALICYLATE NSAIDs,ANTIRHEUMATIC'] = va_class['NONSALICYLATE NSAIS,ANTIRHEUMATIC']
    #     del va_class['NONSALICYLATE NSAIS,ANTIRHEUMATIC']
    #         
        with open(os.path.join(resources, 'cache.pickle'), 'wb') as outfile:
            pickle.dump((va_class, __version__), outfile)
        return va_class

# Not attempting to map between "classes" and "categories" because, upon inspection, there are repeats in both columns
# of the mapping file.  Perhaps these can be dealt with later.
# def _process_class_file():
#     mapping = pandas.read_excel(os.path.join(resources, 'VADrugClass2132012.xls'), sheetname='VA Drug Class 2-13-2012')
#     category_to_class, class_to_category = dict(zip(mapping['VA Category'], mapping['VA Class'])), dict(zip(mapping['VA Class'], mapping['VA Category']))
#     
#     # Correct one special case
#     category_to_class['NONSALICYLATE NSAIDs,ANTIRHEUMATIC'] = category_to_class['NONSALICYLATE NSAIs,ANTIRHEUMATIC']
#     del category_to_class['NONSALICYLATE NSAIs,ANTIRHEUMATIC']
#     class_to_category['MS102'] = 'NONSALICYLATE NSAIDs,ANTIRHEUMATIC'
#     
#     return category_to_class, class_to_category
#     
_code_sets = _process_drug_file()
code_sets = CodeCollection(*_code_sets.items(), name='vadrug', levels=['category', 'vocabulary'])
# category_to_class, class_to_category = _process_class_file()
# classes = {category_to_class[k]:v for k, v in categories.items()}



