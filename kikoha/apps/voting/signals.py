import django.dispatch as dispatch

#####################
vote_recorded = dispatch.Signal(providing_args=["object", "update_type", "vote"])
