import pandas as pd
import os

from aviator_math.cutting_methods import CuttingMethod
from decimal import Decimal


data_dir = os.path.join(os.path.dirname(__file__), 'data')
cdf_path = os.path.join(data_dir, 'cdf.csv')
cdf = pd.read_csv(cdf_path)
cdf.index = cdf['Coef']
cdf.index.name = None
cdf.drop(['Coef'], axis=1, inplace=True)


def generate_coefficient(
    trng: object,
    max_coef: int = 100,
    cutting_method: CuttingMethod = CuttingMethod.MIN
) -> Decimal:
    p = trng.generate_random_decimal(7)
    value = cdf.index[cdf.proportion.searchsorted(p)]
    if value > max_coef:
        if cutting_method == CuttingMethod.MAX:
            return Decimal(max_coef)
        elif cutting_method == CuttingMethod.MIN:
            return Decimal(1)
        elif cutting_method == CuttingMethod.REPEAT:
            return generate_coefficient(trng, max_coef, cutting_method)
        else:
            raise ValueError('Such cutting method doesn\'t exist')
    return value
