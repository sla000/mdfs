from conserv import *

#s = ConnectionServerClient()
#s.main()

c1 = TopServer(getSelfIP(), getSelfIP(), 8000)
c1.main()

time.sleep(1000)
