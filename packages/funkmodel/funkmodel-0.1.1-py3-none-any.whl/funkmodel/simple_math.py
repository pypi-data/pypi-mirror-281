from tortoise import models

class SimpleMathModel(models.Model):
    class Meta:
        abstract = True
        
    
    async def add_int(
        self, 
        attribute: str, 
        value: int
    ):
        """Adds value to self.attribute.

        Args:
            attribute (str): class attr (IntField)
            value (int): value_to_add

        Returns:
            bool, str, self: completed, status, self
        """
        exceptions = []
    
        attr = getattr(self, attribute, None)
        if not attr:
            exceptions.append(attribute)
        else:
            result = attr + value
            setattr(self, attribute, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self
    
    async def deduct_int(
        self, 
        attribute: str, 
        value: int
    ):
        """deducts value from self.attribute.

        Args:
            attribute (str): class attr (IntField)
            value (int): value_to_deduct

        Returns:
            bool, str, self: completed, status, self
        """
        exceptions = []
    
        attr = getattr(self, attribute, None)
        if not attr:
            exceptions.append(attribute)
        else:
            
            result = attr - value
            setattr(self, attribute, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self

    async def mass_add_int(
        self, 
        payload: dict
    ):
        """Adds all v to attr(k)

        Args:
            payload (dict): dict of attr: int_to_add

        Returns:
            bool, string, self: First output is == Success, second for bug solving, third is updated self
        """
        exceptions = []
        for k, v in payload.items():
            attr = getattr(self, k, None)
            if not attr:
                exceptions.append(k)
            else:
                
                result = attr + v
                setattr(self, k, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self
    
    async def mass_deduct_int(
        self, 
        payload: dict, 
    ):
        """Deducts all v from attr(k)

        Args:
            payload (dict): dict of attr: int_to_deduct

        Returns:
            bool, string, self: First output is == Success, second for bug solving, third is updated self
        """
        exceptions = []
        for k, v in payload.items():
            attr = getattr(self, k, None)
            if not attr:
                exceptions.append(k)
            else:
                result = attr + v
                setattr(self, k, result)
        if not exceptions:
            await self.save()
            return True, "All Good", self
        
        return False, f"Attribute Error: {exceptions}", self
