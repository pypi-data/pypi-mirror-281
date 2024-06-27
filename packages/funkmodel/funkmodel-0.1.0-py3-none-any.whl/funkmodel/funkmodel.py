from tortoise import models, fields, transactions, Tortoise
from datetime import datetime
from .precision_model import PrecisionModel
from .time_model import TimeModel
from .father_model import FatherModel
from .simple_math import SimpleMathModel
from .string_model import StringModel
from .wallet_model import WalletModel

def package_info(self):
    return """ FunkModel:
Includes all functionality from Models Below

FatherModel:
    .get_children()
        Get children classes based on a list of related_names

SimpleMathModel:
    .add_int 
    .mass_add_int
    .deduct_int
    .mass_deduct_int

PrecisionModel:
    .add_float
    .mass_add_float
    .deduct_float
    .mass_deduct_float

StringModel:
    .change_string
    
WalletModel: (inherits from StringModel)
    .is_valid_wax_wallet
    .change_wallet_address

TimeModel:
    .when
    .is_time
"""
class FunkModel(
    PrecisionModel, 
    TimeModel,
    FatherModel,
    SimpleMathModel,
    WalletModel
):
    class Meta:
        
        abstract = True

    created_at = fields.FloatField(default=datetime.now().timestamp())


