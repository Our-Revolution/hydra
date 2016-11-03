from .models import EventPromotionRequest
import espresso


class EventPromotionRequestDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'event_promotion_request': item,
            'event': item.event
        }

    class Meta:
        model = EventPromotionRequest
        verbose_name = 'Event Promotion Request'