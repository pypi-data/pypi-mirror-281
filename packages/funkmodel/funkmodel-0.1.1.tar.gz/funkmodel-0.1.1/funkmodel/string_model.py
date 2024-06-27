from tortoise import models


class StringModel(models.Model):
    class Meta:
        abstract = True
        
    async def change_string(
        self, 
        attribute: str, 
        string: str
    ):
        exception = []
        attr = getattr(self, attribute)
        if not attr:
            exception.append(attribute)
        setattr(self, attribute, string)
        await self.save()
        return self, exception
    
    
        