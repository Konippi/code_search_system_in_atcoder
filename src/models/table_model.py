from sqlalchemy.ext.automap import automap_base


Base = automap_base()

Problem = Base.classes.problems  # problems TBL
User = Base.classes.users  # users TBL
Submission = Base.classes.submissions  # submissions TBL
