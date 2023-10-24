import streamlink

streams = streamlink.streams("https://pull.bsy.hw.ourpow.com/live/6135002/playlist.m3u8?sign=b98a36708525090b28f9645d65046325&t=65fc1042")


# print(streams)
#
# x = streams["best"]
#
# print()
# print(x)

fd = streams["best"].open()
data = fd.read(1024)
fd.close()

print(data)


# https://instagram.ftrd4-1.fna.fbcdn.net/hvideo-pnb-frc/_nc_cat-104/v/rAScaVOAHsWu4z626jjtehTcIa4cjbK_BX7pzUiXFBR4pBw/_nc_ohc-DfzKYhMScasAX-fImcM/live-dash/dash-abr/17999825777502188.mpd?ccb=2-4&ms=m_CN&oh=00_AfDXeF0EObAQhtf6c0RaKrpEnhXVjM5fhfI1_xkNfUnqkw&oe=6536D7D2