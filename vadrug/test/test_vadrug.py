from vadrug.vadrug import code_sets#, classes, category_to_class, class_to_category
from nose.tools import assert_equal


def test_vadrug():
    for (catname, vocabname), codes in code_sets.collectlevels().items():
        assert type(codes) is set
        assert isinstance(catname, basestring)
        assert_equal(vocabname, 'NDC')
#         
#         assert_equal(codes, classes[category_to_class[catname]])
#         assert_equal(class_to_category[category_to_class[catname]], catname)

if __name__ == '__main__':
    import sys
    import nose
    # This code will run the test in this file.'
    module_name = sys.modules[__name__].__file__

    result = nose.run(argv=[sys.argv[0],
                            module_name,
                            '-s', '-v'])