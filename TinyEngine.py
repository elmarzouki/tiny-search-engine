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
import os
from collections import defaultdict

class TinyEngine:
    def __init__(self):
        self.StopWords = ['AND', 'OR', 'NOT']
        self.Braces = ['(', ')']

    # Get all Files in Directory
    # we can also return it's subdirectories
    def AllocateAllFiles(self, Directory):
        AllFilles = []
        for Root, Dirs, Files in os.walk(Directory):
            for File in Files:
                if File.endswith('.txt') or File.endswith('.docx'):
                    AllFilles.append(File)
        return AllFilles

    # Search for the terms of the query in files
    def Search(self, Query):
        # append spaces to the Query to split it Ex: (Term op Term)
        for Index, Value in enumerate(Query):
            if len(Query) > Index+1 and Query[Index] is '(' and Query[Index+1] is not ' ':
                Query = Query[:Index+1] + ' ' + Query[Index+1:]
            elif len(Query) > Index+1 and Query[Index+1] is ')' and Query[Index] is not ' ':
                Query = Query[:Index+1] + ' ' + Query[Index+1:]
        TermsBinaryVectors = {}
        Terms = Query.split()
        Files = self.AllocateAllFiles('data')
        TermsBinaryDictionary = defaultdict(list)
        TermsByOrder = []
        TermsOccurrenceCounter = dict()
        for Term in Terms:
            if not Term in self.StopWords and not Term in self.Braces:
                if not Term in TermsBinaryVectors:
                    # this's a problem the term can be added to the array without appending the new value
                    # just placing it randomly
                    TermsBinaryVectors[Term] = {}
                    TermsOccurrenceCounter[Term] = 0
            # the previous problem solved by this list selector
            TermsByOrder.append(Term)
            if not Term in self.StopWords and not Term in self.Braces:
                FilesCounter = len(Files)
                for File in Files:
                    with open('data/' + File) as Lines:
                        for Line in Lines:
                            if Term in Line:
                                TermsBinaryVectors[Term][File] = True
                            else:
                                if not File in TermsBinaryVectors[Term] or not TermsBinaryVectors[Term][File] is True:
                                    TermsBinaryVectors[Term][File] = False
                    if not Term in TermsBinaryDictionary:
                        TermsBinaryDictionary[Term].append(TermsBinaryVectors[Term][File])
                        TermsOccurrenceCounter[Term] += 1
                    elif not TermsOccurrenceCounter[Term] > FilesCounter - 1:
                        TermsBinaryDictionary[Term].append(TermsBinaryVectors[Term][File])
                        TermsOccurrenceCounter[Term] += 1
            # we need to loop on TermsByOrder to append AND
            for Index, Value in enumerate(TermsByOrder):
                # append AND between (Term op Term)(Term op Term)
                if Index+1 < len(TermsByOrder) and TermsByOrder[Index] is ')' and TermsByOrder[Index+1] is '(':
                    TermsByOrder.insert(Index+1, 'AND')
                # append AND Before NOT EX: ( Term op Term ) NOT Term
                if Index+1 < len(TermsByOrder) and TermsByOrder[Index+1] == 'NOT' and not \
                        any([TermsByOrder[Index] in Seek for Seek in self.StopWords]) and not TermsByOrder[Index] is '(':
                    TermsByOrder.insert(Index+1, 'AND')
        return TermsBinaryVectors, TermsBinaryDictionary, TermsByOrder

    # NOT gate
    def NOTGate(self, Term):
        NOTTerm = ''
        for Digit in Term:
            if Digit is '1':
                NOTTerm += '0'
            elif Digit is '0':
                NOTTerm += '1'
        return NOTTerm

    # AND gate
    def ANDGate(self, LeftTerm, RightTerm):
        TermANDTerm = ''
        for LeftDigit, RightDigit in zip(LeftTerm, RightTerm):
            if LeftDigit is '1' and RightDigit is '1':
                TermANDTerm += '1'
            else:
                TermANDTerm += '0'
        return TermANDTerm

    # OR gate
    def ORGate(self, LeftTerm, RightTerm):
        TermORTerm = ''
        for LeftDigit, RightDigit in zip(LeftTerm, RightTerm):
            if LeftDigit is '0' and RightDigit is '0':
                TermORTerm += '0'
            else:
                TermORTerm += '1'
        return TermORTerm

    # get the terms from query and applay the bitwise function
    def BitwiseCalculator(self, Query):
        BitwiseQuery = ''
        TermsBinaryVectors, TermsBinaryDictionary, TermsByOrder = self.Search(Query)
        for Term in TermsByOrder:
            if not Term in self.StopWords and not Term in self.Braces:
                BinaryTerm = ''
                for value in TermsBinaryDictionary[Term]:
                    if value is True:
                        BinaryTerm += '1'
                    elif value is False:
                        BinaryTerm += '0'
                BitwiseQuery += BinaryTerm
            else:
                BitwiseQuery += Term
            BitwiseQuery += ' '
        SplitedBitwiseQuery = BitwiseQuery.split()
        if '(' in self.Braces:
            while '(' in SplitedBitwiseQuery:
                LeftBracePosition = len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') - 1
                # RightBracePosition = SplitedBitwiseQuery.index(')', LeftBracePosition)
                LeftTerm = SplitedBitwiseQuery[LeftBracePosition + 1]
                if LeftTerm == 'NOT':
                    NextTerm = SplitedBitwiseQuery[LeftBracePosition + 2]
                    try:
                        NOTTerm = self.NOTGate(NextTerm)
                    finally:
                        SplitedBitwiseQuery[LeftBracePosition + 2] = SplitedBitwiseQuery[LeftBracePosition + 2].replace(
                            SplitedBitwiseQuery[LeftBracePosition + 2], NOTTerm)
                        SplitedBitwiseQuery.remove('NOT')
                        if (len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') - 1) > 0:
                            if len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') + 1 \
                                    == SplitedBitwiseQuery.index(')', LeftBracePosition):
                                SplitedBitwiseQuery.pop(SplitedBitwiseQuery.index(')', LeftBracePosition))
                                SplitedBitwiseQuery.pop(LeftBracePosition)
                        else:
                            SplitedBitwiseQuery.pop(SplitedBitwiseQuery.index(')', LeftBracePosition))
                            SplitedBitwiseQuery.pop(LeftBracePosition)
                else:
                    Operator = SplitedBitwiseQuery[LeftBracePosition + 2]
                    RightTerm = SplitedBitwiseQuery[LeftBracePosition + 3]
                    if Operator == 'AND':
                        try:
                            TermANDTerm = self.ANDGate(LeftTerm, RightTerm)
                        finally:
                            SplitedBitwiseQuery[LeftBracePosition + 1] = LeftTerm.replace(LeftTerm, TermANDTerm)
                            SplitedBitwiseQuery.pop(LeftBracePosition + 2)
                            SplitedBitwiseQuery.pop(LeftBracePosition + 2)
                            if (len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') - 1) > 0:
                                if len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') + 1\
                                        == SplitedBitwiseQuery.index(')', LeftBracePosition):
                                    SplitedBitwiseQuery.pop(SplitedBitwiseQuery.index(')', LeftBracePosition))
                                    SplitedBitwiseQuery.pop(LeftBracePosition)
                            else:
                                SplitedBitwiseQuery.pop(SplitedBitwiseQuery.index(')', LeftBracePosition))
                                SplitedBitwiseQuery.pop(LeftBracePosition)

                    elif Operator == 'OR':
                        try:
                            TermORTerm = self.ORGate(LeftTerm, RightTerm)
                        finally:
                            SplitedBitwiseQuery[LeftBracePosition + 1] = LeftTerm.replace(LeftTerm, TermORTerm)
                            SplitedBitwiseQuery.pop(LeftBracePosition + 2)
                            SplitedBitwiseQuery.pop(LeftBracePosition + 2)
                            if (len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') - 1) > 0:
                                if (len(SplitedBitwiseQuery) - SplitedBitwiseQuery[::-1].index('(') - 1) + \
                                        (LeftBracePosition + 1) == SplitedBitwiseQuery.index(')', LeftBracePosition):
                                    SplitedBitwiseQuery.pop(SplitedBitwiseQuery.index(')', LeftBracePosition))
                                    SplitedBitwiseQuery.pop(LeftBracePosition)
                            else:
                                SplitedBitwiseQuery.pop(SplitedBitwiseQuery.index(')', LeftBracePosition))
                                SplitedBitwiseQuery.pop(LeftBracePosition)
            if not '(' in SplitedBitwiseQuery:
                while len(SplitedBitwiseQuery) > 1:
                    if 'NOT' in SplitedBitwiseQuery:
                        TheNextTermAfterNOT = SplitedBitwiseQuery.index('NOT') + 1
                        NOTTerm = self.NOTGate(SplitedBitwiseQuery[TheNextTermAfterNOT])
                        SplitedBitwiseQuery[TheNextTermAfterNOT] = SplitedBitwiseQuery[TheNextTermAfterNOT].replace(
                            SplitedBitwiseQuery[TheNextTermAfterNOT], NOTTerm)
                        SplitedBitwiseQuery.remove('NOT')
                    elif 'AND' in SplitedBitwiseQuery:
                        TheNextTermAfterAND = SplitedBitwiseQuery[SplitedBitwiseQuery.index('AND') + 1]
                        ThePreviousTermBeforAND = SplitedBitwiseQuery[SplitedBitwiseQuery.index('AND') - 1]
                        TermANDTerm = self.ANDGate(ThePreviousTermBeforAND, TheNextTermAfterAND)
                        SplitedBitwiseQuery[SplitedBitwiseQuery.index('AND') - 1] = ThePreviousTermBeforAND.replace(
                            ThePreviousTermBeforAND, TermANDTerm)
                        SplitedBitwiseQuery.remove(TheNextTermAfterAND)
                        SplitedBitwiseQuery.remove('AND')
                    elif 'OR' in SplitedBitwiseQuery:
                        TheNextTermAfterOR = SplitedBitwiseQuery[SplitedBitwiseQuery.index('OR') + 1]
                        ThePreviousTermBeforOR = SplitedBitwiseQuery[SplitedBitwiseQuery.index('OR') - 1]
                        TermORTerm = self.ORGate(ThePreviousTermBeforOR, TheNextTermAfterOR)
                        SplitedBitwiseQuery[SplitedBitwiseQuery.index('OR') - 1] = ThePreviousTermBeforOR.replace(
                            ThePreviousTermBeforOR, TermORTerm)
                        SplitedBitwiseQuery.remove(TheNextTermAfterOR)
                        SplitedBitwiseQuery.remove('OR')
                    else:
                        Word = ''
                        MatchedDocuments = []
                        for Term in SplitedBitwiseQuery:
                            Word = Term + ' '
                        Word = Word[:-1]
                        Files = self.AllocateAllFiles('data')
                        for File in Files:
                            with open('data/' + File) as Lines:
                                for Line in Lines:
                                    if Word in Line:
                                        MatchedDocuments.append(File)
                                        break
                        return MatchedDocuments
                MatchedDocuments = []
                Files = self.AllocateAllFiles('data')
                for Index, Value in enumerate(SplitedBitwiseQuery[0]):
                    if Value is '1':
                        MatchedDocuments.append(Files[Index])
                return MatchedDocuments