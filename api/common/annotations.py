from decimal import Decimal
from typing_extensions import Annotated
from pydantic import PlainSerializer

DecimalField = Annotated[
    Decimal,
    PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
]
