Naming format, After Effects projects:

sloeae,V=cs55,I=1920x1080_59.94p_mp4,O=1280x720_30p_flv_3M,A=aac_2_48,S=4,E=sharpen.aepx


sloeae:magic string, sloeae -> After Effects
V:version, cs55 -> Creative Suite 5.5
I:input, 1920x1080_59.94p_mp4 -> Input video size, frame rate and format
O:output, 1280x720_30p_flv_3M -> Output video size, frame rate, format, bit rate in Mbps
A:audio, optional (no audio if missing), aac_2_48 -> AAC Stereo 48kHz
S:slowdown, optional, 4 -> 25% speed
F:speedup, optional, 1.75 -> 175% speed
E:effects, optional, free form

The order of elements is fixed and as above and case is significant.  Video formats can be abbreviated to 1080p50_mp4, etc.

Naming format, Output Module:

sloeae,V=cs55,O=640x360_30p_f4v_2.2M,C=baseline3

V:version, cs55 -> Creative Suite 5.5
O:output, 640x360_30p_f4v_2.2M -> Output video size, frame rate, format, bit rate in Mbps
D:details, baseline3 -> Baseline level 3
