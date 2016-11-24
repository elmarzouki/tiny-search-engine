# about:
# This code was written by Mostafa El-Marzouki @iSuperMostafa
# Occupation: Faculty of computer science and information Helwan university.
# Related courses: information storage and retrieval
# ------------------------------------------------------------
# summery:
# This project is a Tiny Search Engine, that do searching in
# unlimited number of files in directory called data.
# The input is query like Term AND Term.
# The output the documents that matching this query.

import TinyEngine


TinyEngine = TinyEngine.TinyEngine()
while True:
    Query = input('Search: ')

    # print the Binary vector for each term
    TermsBinaryVectors, TermsBinaryDictionary, TermsByOrder = TinyEngine.Search(Query)
    print(TermsBinaryVectors)
    print(TermsBinaryDictionary)
    print(TermsByOrder)

    # print the matched documents
    if not TinyEngine.BitwiseCalculator(Query):
        print('No documents matched!')
    else:
        print(TinyEngine.BitwiseCalculator(Query))
