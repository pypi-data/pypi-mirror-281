from tortoise import models, fields
from datetime import datetime

class TimeModel(models.Model):
    class Meta:
        abstract = True
        
    async def is_time(
        self, 
        now, 
        attr, 
        action
    ):
        """Used to determine if action is allowed to happen, and outputs a bool and the amount of time until next action based on current timestamp (if applicable) 

        Args:
            now (float): timestamp
            attr (str): class attr that stores cooldown finish time
            action (str): action name to insert in the output string

        Returns:
            bool, str: Action can occur and when (if applicable) 
        """
        myattr = getattr(self, attr)
        if now >= myattr:
            return True, f"can {action}"
        
        when = await self.when(now, attr, action)
        return False, when
    
    async def when(
        self, 
        now: float, 
        attr: str, 
        action: str
    ) -> str:
        """Used to get amount of time until next action based on current timestamp 

        Args:
            now (float): timestamp
            attr (str): class attr that stores cooldown finish time
            action (str): action name to insert in the output string

        Returns:
            str: Parsed time formated with action into a string
        """
        myattr = getattr(self, attr)
        remaining_seconds = int(myattr - now)  # Make sure it's an integer

        # If there's no time remaining or it's negative (shouldn't happen normally), can claim now
    
        hours, remainder = divmod(remaining_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Build the time string based on the values
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s until you can {action} again."
        elif minutes > 0:
            return f"{minutes}m {seconds}s until you can {action} again."
        else:  # Less than a minute remaining
            return f"{seconds}s until you can {action} again."