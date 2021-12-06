

#liquidsoap script to connect to Icecast server and stream input harbor. 
#
set("harbor.bind_addr","0.0.0.0")


# The port and password here goes in your /etc/mpd.conf 
live = input.harbor("stream", user="source", port=9000,password="YOUR_PASSWD")

# Song that gets played when a source drops or there is 20 seconds of silence
files = single("/etc/liquidsoap/tech_prob.mp3")
radio = fallback(track_sensitive=false,
                 [strip_blank(max_blank=20.,live),files])

# Your icecast info
output.icecast(%mp3,id="source",
               mount="/stream",
               port=8000,
               host="localhost", password="YOUR_PASSWD",
               icy_metadata="true",description="SL Radio Station",
               url="http://your_server.org",
               radio)

