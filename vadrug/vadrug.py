import pandas
import os
from .resources import resources
from clinvoc.ndc import NDC
from clinvoc.code_collections import CodeCollection
from clinvoc.base import left_pad
from modulecache.invalidators import FileChangeInvalidator
from modulecache.backends import PickleBackend

def _process_drug_file():
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
        
        if (cls, vocab.vocab_name, vocab.vocab_domain) in va_class:
            va_class[(cls, vocab.vocab_domain, vocab.vocab_name)].add(ndc)
        else:
            va_class[(cls, vocab.vocab_domain, vocab.vocab_name)] = {ndc}
    
    return va_class  
        # Don't need the special case because not attempting to map between "classes" and "categories"
    #     # Correct one special case
    #     va_class['NONSALICYLATE NSAIDs,ANTIRHEUMATIC'] = va_class['NONSALICYLATE NSAIS,ANTIRHEUMATIC']
    #     del va_class['NONSALICYLATE NSAIS,ANTIRHEUMATIC']
    #         

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
cache_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'va_drug_cache.pkl')
suppress = globals().keys()
with PickleBackend(cache_filename, suppress) as cache, FileChangeInvalidator(cache, os.path.abspath(__file__)):
    code_sets = CodeCollection(*_process_drug_file().items(), name='vadrug', levels=['category', 'domain', 'vocabulary'])
# category_to_class, class_to_category = _process_class_file()
# classes = {category_to_class[k]:v for k, v in categories.items()}



