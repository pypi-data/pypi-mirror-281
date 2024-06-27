from tortoise import models
import re
from .string_model import StringModel

class WalletModel(StringModel):
    class Meta:
        abstract = True
        
    async def is_valid_wax_wallet(
        self,
        wallet: str
    ) -> bool:
        pattern = r"^[\.a-z1-5]{1,13}$"
    
        # Use re.fullmatch to check if the address matches the pattern
        return re.fullmatch(pattern, wallet) is not None
        
    async def change_wallet_address(
        self, 
        new_address: str
    ):
        if not await self.is_valid_wax_wallet(new_address):
            return False, self ["Invalid Account Name"]
        self, exception = await self.change_string("wallet", new_address)
        return True, self, exception
    