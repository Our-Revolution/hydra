from .models import Event, EventAttendee
from .auth import Constituent
import espresso


class ConstituentDripType(espresso.DripBase):
    
    @classmethod
    def get_email_context(cls, item):
        return {
            'person': item,
            'email_address': item.email_address
        }

    class Meta:
        model = Constituent
        verbose_name = 'Constituents'


class EventHostDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'host': item.creator_cons,
            'email_address': item.creator_cons.email_address,
            'event': item
        }

    class Meta:
        model = Event
        verbose_name = 'Event (Send to Event Host)'


class EventEveryoneDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        email_addresses = map(lambda x: x.attendee_cons.email_address, item.attendees.all())
        email_addresses.append(item.creator_cons.email_address)

        return {
            'email_address': email_addresses,
            'event': item
        }

    class Meta:
        model = Event
        verbose_name = 'Event (Send to Event Host AND Attendees)'


class EventAttendeesDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'attendee': item.attendee_cons,
            'email_address': item.attendee_cons.email_address,
            'event': item.event,
            'rsvp': item
        }

    class Meta:
        model = EventAttendee
        verbose_name = 'Event Attendees'


class EventAttendeesToHostType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'attendee': item.attendee_cons,
            'email_address': item.event.creator_cons.email_address,
            'event': item.event,
            'rsvp': item
        }

    class Meta:
        model = EventAttendee
        verbose_name = 'Event Attendees (Send to Host)'
