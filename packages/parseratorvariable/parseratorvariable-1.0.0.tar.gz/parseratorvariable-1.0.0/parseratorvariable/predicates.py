from dedupe import predicates
from probableparsing import RepeatedLabelError


class PartialIndex:
    def __init__(self, *args, **kwargs):
        self.part = kwargs.pop("part")
        self.tag = kwargs.pop("tag")
        super().__init__(*args, **kwargs)
        self.__name__ = "({}, {}, {})".format(self.threshold, self.field, self.part)

    def preprocess(self, doc):
        try:
            tags, _ = self.tag(doc)
        except TypeError:
            part = ""
        else:
            part = tags.get(self.part, "")
        return super().preprocess(part)


class PLCPredicate(PartialIndex, predicates.LevenshteinCanopyPredicate):
    type = "PartialIndexLevenshteinCanopyPredicate"


class PLSPredicate(PartialIndex, predicates.LevenshteinSearchPredicate):
    type = "PartialIndexLevenshteinSearchPredicate"


class PTNCPredicate(PartialIndex, predicates.TfidfNGramCanopyPredicate):
    type = "PartialIndexTfidfNGramCanopyPredicate"


class PTNSPredicate(PartialIndex, predicates.TfidfNGramSearchPredicate):
    type = "PartialIndexTfidfNGramSearchPredicate"


class PTTCPredicate(PartialIndex, predicates.TfidfTextCanopyPredicate):
    type = "PartialIndexTfidfTextCanopyPredicate"


class PTTSPredicate(PartialIndex, predicates.TfidfTextSearchPredicate):
    type = "PartialIndexTfidfTextSearchPredicate"


class PartialString(predicates.StringPredicate):
    type = "PartialPredicate"

    def __init__(self, func, field, part, tag):
        self.func = func
        self.__name__ = "({}, {}, {})".format(func.__name__, field, part)
        self.field = field
        self.part = part
        self.tag = tag

    def __call__(self, record, **kwargs):
        column = record[self.field]
        if not column:
            return ()

        try:
            tags, _ = self.tag(column)
        except TypeError:
            return ()
        else:
            part = tags.get(self.part, "")

        return super().__call__({self.field: part})
