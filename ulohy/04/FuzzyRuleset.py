from Fuzzy import FuzzyUniverse, FuzzyRule, FuzzySystem
import Fuzzy.Function as Function
from Fuzzy.Term import Term


class FuzzyRuleset:
    def __init__(self):
        """ Initialise the fuzzy universe """
        trate = FuzzyUniverse(0, 10, 'Stavba tratí')
        trate['Nevhodné pro typ závodu'] = Term(Function.TrapMF(0, 0, 2, 4))
        trate['Dobré'] = Term(Function.TrapMF(2, 3, 6, 7))
        trate['Výborné'] = Term(Function.TrapMF(6, 7, 10, 10))

        mapa = FuzzyUniverse(0, 10, 'Kvalita mapy')
        mapa["Špatná"] = Term(Function.TrapMF(0, 0, 3, 4))
        mapa["Mírné nedostatky"] = Term(Function.TrapMF(3, 4, 5, 7))
        mapa["Výborná"] = Term(Function.TrapMF(5, 6, 10, 10))

        prostor = FuzzyUniverse(0, 10, 'Prostor závodu')
        prostor["Nevhodný"] = Term(Function.TrapMF(0, 0, 3, 5))
        prostor["Vhodný"] = Term(Function.TrapMF(4, 6, 10, 10))

        shromazdiste = FuzzyUniverse(0, 10, 'Shromaždiště')
        shromazdiste["Špatné"] = Term(Function.TrapMF(0, 0, 1, 3))
        shromazdiste["Mírné nedostatky"] = Term(Function.TrapMF(2, 3, 6, 7))
        shromazdiste["Dobré"] = Term(Function.TrapMF(6, 7, 8, 9))
        shromazdiste["Výborné"] = Term(Function.TrapMF(8, 9, 10, 10))

        organizace = FuzzyUniverse(0, 10, 'Organizace')
        organizace["Špatná"] = Term(Function.TrapMF(0, 0, 3, 4))
        organizace["Průměrná"] = Term(Function.TrapMF(3, 4, 6, 8))
        organizace["Výborná"] = Term(Function.TrapMF(7, 8, 10, 10))

        self.celkove = celkove = FuzzyUniverse(0, 10, 'Celkové hodnocení závodu')
        self.celkove["Špatné"] = Term(Function.TrapMF(0, 0, 3, 4))
        self.celkove["Mírné nedostatky"] = Term(Function.TrapMF(3, 4, 5, 6))
        self.celkove["Výborné"] = Term(Function.TrapMF(5, 6, 7, 8))
        self.celkove["Excelentní"] = Term(Function.TrapMF(7, 8, 10, 10))

        r = list()
        r.append(FuzzyRule((trate["Nevhodné pro typ závodu"] | mapa["Špatná"]) & ~prostor["Vhodný"], celkove["Špatné"]))
        r.append(FuzzyRule(~trate["Výborné"] & ~mapa["Výborná"] & shromazdiste["Špatné"] & organizace["Špatná"], celkove["Špatné"]))
        r.append(FuzzyRule(~trate["Výborné"] & mapa["Špatná"] & prostor["Nevhodný"], celkove["Špatné"]))
        r.append(FuzzyRule(prostor["Nevhodný"] & shromazdiste["Špatné"] & organizace["Špatná"], celkove["Špatné"]))
        r.append(FuzzyRule(~trate["Nevhodné pro typ závodu"] & ~mapa["Špatná"] & (shromazdiste["Mírné nedostatky"] | shromazdiste["Dobré"]), celkove["Mírné nedostatky"]))
        r.append(FuzzyRule((trate["Výborné"] | mapa["Výborná"]) & ~prostor["Vhodný"], celkove["Mírné nedostatky"]))
        r.append(FuzzyRule((~trate["Nevhodné pro typ závodu"] & ~mapa["Špatná"]) & (organizace["Špatná"] | organizace["Průměrná"]), celkove["Mírné nedostatky"]))
        r.append(FuzzyRule(trate["Dobré"] & mapa["Výborná"] & prostor["Vhodný"] & ~shromazdiste["Výborné"] & ~organizace["Špatná"], celkove["Mírné nedostatky"]))
        r.append(FuzzyRule(trate["Výborné"] & mapa["Výborná"] & prostor["Nevhodný"], celkove["Výborné"]))
        r.append(FuzzyRule(trate["Výborné"] & mapa["Mírné nedostatky"] & prostor["Vhodný"] & ~shromazdiste["Špatné"] & organizace["Výborná"], celkove["Výborné"]))
        r.append(FuzzyRule((trate["Výborné"] | trate["Dobré"]) & (mapa["Výborná"] | mapa["Mírné nedostatky"]) & ~prostor["Vhodný"] & ~shromazdiste["Špatné"] & organizace["Průměrná"], celkove["Výborné"]))
        r.append(FuzzyRule(~trate["Nevhodné pro typ závodu"] & ~mapa["Špatná"] & shromazdiste["Výborné"] & organizace["Průměrná"], celkove["Výborné"]))
        r.append(FuzzyRule(~trate["Nevhodné pro typ závodu"] & ~mapa["Špatná"] & ~shromazdiste["Špatné"] & organizace["Výborná"], celkove["Excelentní"]))
        r.append(FuzzyRule(trate["Výborné"] & (mapa["Výborná"] | mapa["Mírné nedostatky"]) & prostor["Vhodný"] & (shromazdiste["Mírné nedostatky"] | shromazdiste["Dobré"]) & ~organizace["Špatná"], celkove["Excelentní"]))
        r.append(FuzzyRule(trate["Výborné"] & mapa["Výborná"] & prostor["Vhodný"] & shromazdiste["Výborné"] & ~organizace["Špatná"], celkove["Excelentní"]))

        self.fuzzy_system = FuzzySystem(
            fuzzy_universe_list=[trate, mapa, prostor, shromazdiste, organizace, self.celkove], rule_list=r)

    def evaluate(self, show_graph=True):
        """Evaluate the system with user inputs"""
        return self.fuzzy_system.generate_centroid(self.celkove, show_graph=show_graph)
