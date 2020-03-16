from utils.database import Users, Albums
from utils.base import session_factory, engine, Base
from datetime import time, datetime

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# populate database
amy = Users(net_id='jyxu')
lrrh = Albums(name='little red', user=amy)
aiwl = Albums(name='alice wonderland', user=amy)

sess = session_factory()
sess.add(amy)
sess.add(lrrh)
sess.add(aiwl)

sess.commit()
sess.close()
