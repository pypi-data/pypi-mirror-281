from tortoise import models, fields
from datetime import datetime

class FatherModel(models.Model):
    class Meta:
        abstract = True
    
    async def get_children(
        self, 
        children: list
    ) -> list:
        """Gets lists of children from a list of children related_names

        Args:
            children (_type_): list of related_names
        Returns:
            list[list], list: List of children lists and list with exceptions
        """
        exceptions = []
        children_list = []
        for child in children:
            attr = await getattr(self, child, None)
            if not attr:
                exceptions.append(child)
                continue
            children_list.append(attr)
            
        return children_list, exceptions
