FROM alpine
MAINTAINER Rob Cakebread <rob@cakebread.io>

RUN apk --update upgrade && apk add --no-cache mpd mpc && setcap -r /usr/bin/mpd

VOLUME /var/lib/mpd

EXPOSE 6600
CMD ["mpd", "--stdout", "--no-daemon"]
