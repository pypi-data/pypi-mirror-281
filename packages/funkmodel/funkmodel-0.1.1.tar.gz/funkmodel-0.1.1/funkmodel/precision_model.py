from tortoise import models, fields
from datetime import datetime

class PrecisionModel(models.Model):
    class Meta:
        abstract = True
    
    async def add_float(
        self, 
        attribute: str, 
        value: float,
        precision: int = 100000000
    ):
        """Uses precision to add float to float.

        Args:
            attribute (str): class attr (BoolenField)
            value (float): value_to_add
            precision (int, optional): 10, 100, 1000, etc. Defaults to 100000000.

        Returns:
            bool, str, self: completed, status, self
        """
        exceptions = []
    
        attr = getattr(self, attribute, None)
        if not attr:
            exceptions.append(attribute)
        else:
            current = attr * precision
            to_add = value * precision
            result = (current + to_add) / precision
            setattr(self, attribute, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self
    
    async def deduct_float(
        self, 
        attribute: str, 
        value: float,
        precision: int = 100000000
    ):
        """Uses precision to add float to float.

        Args:
            attribute (str): class attr (BoolenField)
            value (float): value_to_add
            precision (int, optional): 10, 100, 1000, etc. Defaults to 100000000.

        Returns:
            bool, str, self: completed, status, self
        """
        exceptions = []
    
        attr = getattr(self, attribute, None)
        if not attr:
            exceptions.append(attribute)
        else:
            current = attr * precision
            to_deduct = value * precision
            result = (current - to_deduct) / precision
            setattr(self, attribute, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self

    async def mass_add_float(
        self, 
        payload: dict, 
        precision: int = 100000000
    ):
        """Uses precision to get accurate addition between float class attrs

        Args:
            payload (dict): dict of attr: float_to_add
            precision (int, optional): 10, 100, 1000, etc. Defaults to 100000000.

        Returns:
            bool, string, self: First output is == Success, second for bug solving, third is updated self
        """
        exceptions = []
        for k, v in payload.items():
            attr = getattr(self, k, None)
            if not attr:
                exceptions.append(k)
            else:
                current = attr * precision
                to_add = v * precision
                result = (current + to_add) / precision
                setattr(self, k, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self
    
    async def mass_deduct_float(
        self, 
        payload: dict, 
        precision: int = 100000000
    ):
        """Uses precision to get accurate deduction between float class attrs

        Args:
            payload (dict): dict of attr: float_to_deduct
            precision (int, optional): 10, 100, 1000, etc. Defaults to 100000000.

        Returns:
            bool, string, self: First output is == Success, second for bug solving, third is updated self
        """
        exceptions = []
        for k, v in payload.items():
            attr = getattr(self, k, None)
            if not attr:
                exceptions.append(k)
            else:
                current = attr * precision
                to_deduct = v * precision
                result = (current - to_deduct) / precision
                setattr(self, k, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self
