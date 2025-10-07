from .models import Group, Membership

def get_user_space(user):   
    mem = Membership.objects.filter(type='priv', member=user).first()
    return mem.group