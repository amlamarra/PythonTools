#!/usr/bin/python3

with open("cap.txt", "r") as f:
	data = f.read()

lst = data.split("\n")
newlst = data.split("\n")

num_pkts = 0

for i in lst:
	if i[0] != "\t":
		num_pkts += 1
packets = [None]*num_pkts

for pkt in range(num_pkts):
	for i in range(len(lst)):
		packets[pkt].append(lst[i])
		lst.remove(lst[i])
		if lst[i+1] != "\t":
			break
		
		
	
#newlst.remove(lst[i])

chunk = []
for line in newlst:
	line = line.split(" ")
	line = list(filter(None, line))
	line = line[1:-1]
	line = "".join(line)
	chunk.append(line)

chunk = "".join(chunk)

final = []
while len(chunk) > 0:
	final.append(chunk[:2])
	chunk = chunk[2:]

msg = ""
for char in final:
	msg += chr(int(char, 16))

print(msg)

#with open("cap_modified.txt", "w") as f:
#	f.write(msg)


'''
SAMPLE:
11:17:55.000000 fc:fb:fb:31:99:c0 > 00:e0:ed:1f:15:a9, ethertype IPv4 (0x0800), length 89: (tos 0x0, ttl  64, id 25961, offset 0, flags [none], proto: TCP (6), length: 75, bad cksum 0 (->d0dd)!) 10.75.43.55.56890 > 74.125.196.103.443: P, cksum 0x0000 (incorrect (-> 0x2c18), 5430:5465(35) ack 64478 win 65535
	0x0000:  00e0 ed1f 15a9 fcfb fb31 99c0 0800 4500  .........1....E.
	0x0010:  004b 6569 0000 4006 0000 0a4b 2b37 4a7d  .Kei..@....K+7J}
	0x0020:  c467 de3a 01bb 0000 1536 0000 fbde 5018  .g.:.....6....P.
	0x0030:  ffff 0000 0000 3530 3632 3138 332d 343a  ......5062183-4:
	0x0040:  3530 3632 3139 342d 3133 3a35 3036 3232  5062194-13:50622
	0x0050:  3032 2d38 3a0d 0a0d 0a                   02-8:....
11:17:55.000000 00:e0:ed:1f:15:a9 > fc:fb:fb:31:99:c0, ethertype IPv4 (0x0800), length 89: (tos 0x0, ttl  64, id 25961, offset 0, flags [none], proto: TCP (6), length: 75, bad cksum 0 (->d0dd)!) 74.125.196.103.443 > 10.75.43.55.56890: P, cksum 0x0000 (incorrect (-> 0x3ead), 4294967262:1(35) ack 35 win 65535
	0x0000:  fcfb fb31 99c0 00e0 ed1f 15a9 0800 4500  ...1..........E.
	0x0010:  004b 6569 0000 4006 0000 4a7d c467 0a4b  .Kei..@...J}.g.K
	0x0020:  2b37 01bb de3a 0000 fbbb 0000 1559 5018  +7...:.......YP.
	0x0030:  ffff 0000 0000 206d 613d 3235 3932 3030  .......ma=259200
	0x0040:  303b 2076 3d22 3336 2c33 352c 3334 2c33  0;.v="36,35,34,3
	0x0050:  332c 3332 220d 0a0d 0a                   3,32"....
11:17:55.000000 fc:fb:fb:31:99:c0 > 00:e0:ed:1f:15:a9, ethertype IPv4 (0x0800), length 946: truncated-ip - 20 bytes missing! (tos 0x0, ttl  64, id 25961, offset 0, flags [none], proto: TCP (6), length: 952, bad cksum 0 (->cd70)!) 10.75.43.55.56890 > 74.125.196.103.443: P 35:947(912) ack 1 win 65535
	0x0000:  00e0 ed1f 15a9 fcfb fb31 99c0 0800 4500  .........1....E.
	0x0010:  03b8 6569 0000 4006 0000 0a4b 2b37 4a7d  ..ei..@....K+7J}
	0x0020:  c467 de3a 01bb 0000 1559 0000 fbde 5018  .g.:.....Y....P.
	0x0030:  ffff 0000 0000 4745 5420 2f73 6561 7263  ......GET./searc
	0x0040:  683f 7363 6c69 656e 743d 7073 792d 6162  h?sclient=psy-ab
	0x0050:  2673 6974 653d 2673 6f75 7263 653d 6870  &site=&source=hp
	0x0060:  2671 3d6d 6173 7465 722e 6462 6f2e 7870  &q=master.dbo.xp
	0x0070:  5f66 6978 6564 6472 6976 6573 2b73 716c  _fixeddrives+sql
	0x0080:  2b73 6572 7665 722b 3230 3038 266f 713d  +server+2008&oq=
	0x0090:  6578 6563 2b6d 6173 7465 722e 6462 6f2e  exec+master.dbo.
	0x00a0:  7870 5f66 6978 6564 6472 6976 6573 2667  xp_fixeddrives&g
	0x00b0:  735f 6c3d 6870 2e31 2e32 2e30 6a30 6932  s_l=hp.1.2.0j0i2
	0x00c0:  3269 3330 6b31 6c32 2e32 3735 382e 3237  2i30k1l2.2758.27
	0x00d0:  3538 2e30 2e35 3334 382e 312e 312e 302e  58.0.5348.1.1.0.
	0x00e0:  302e 302e 302e 3135 382e 3135 382e 306a  0.0.0.158.158.0j
	0x00f0:  312e 312e 302e 666f 6f2c 6272 7561 733d  1.1.0.foo,bruas=
	0x0100:  312c 6272 7561 3d31 2e2e 2e30 2e2e 2e31  1,brua=1...0...1
	0x0110:  632e 312e 3634 2e70 7379 2d61 622e 2e30  c.1.64.psy-ab..0
	0x0120:  2e31 2e31 3434 2e56 6971 4942 5976 495f  .1.144.ViqIBYvI_
	0x0130:  6963 2670 6278 3d31 2662 6176 3d6f 6e2e  ic&pbx=1&bav=on.
	0x0140:  322c 6f72 2e26 6276 6d3d 6276 2e31 3333  2,or.&bvm=bv.133
	0x0150:  3338 3737 3535 2c64 2e65 5745 2666 703d  387755,d.eWE&fp=
	0x0160:  3126 6269 773d 3136 3830 2662 6968 3d39  1&biw=1680&bih=9
	0x0170:  3535 2664 7072 3d31 2674 6368 3d31 2665  55&dpr=1&tch=1&e
	0x0180:  6368 3d31 2670 7369 3d48 6662 6a56 376d  ch=1&psi=HfbjV7m
	0x0190:  3749 4966 4d6d 4148 5a71 6f6d 6744 512e  7IIfMmAHZqomgDQ.
	0x01a0:  3134 3734 3535 3734 3730 3034 352e 3320  1474557470045.3.
	0x01b0:  4854 5450 2f31 2e31 0d0a 4163 6365 7074  HTTP/1.1..Accept
	0x01c0:  3a20 2a2f 2a0d 0a52 6566 6572 6572 3a20  :.*/*..Referer:.
	0x01d0:  6874 7470 733a 2f2f 7777 772e 676f 6f67  https://www.goog
	0x01e0:  6c65 2e63 6f6d 2f3f 6777 735f 7264 3d73  le.com/?gws_rd=s
	0x01f0:  736c 0d0a 4163 6365 7074 2d4c 616e 6775  sl..Accept-Langu
	0x0200:  6167 653a 2065 6e2d 5553 0d0a 4163 6365  age:.en-US..Acce
	0x0210:  7074 2d45 6e63 6f64 696e 673a 2067 7a69  pt-Encoding:.gzi
	0x0220:  702c 2064 6566 6c61 7465 0d0a 5573 6572  p,.deflate..User
	0x0230:  2d41 6765 6e74 3a20 4d6f 7a69 6c6c 612f  -Agent:.Mozilla/
	0x0240:  352e 3020 2857 696e 646f 7773 204e 5420  5.0.(Windows.NT.
	0x0250:  362e 333b 2057 4f57 3634 3b20 5472 6964  6.3;.WOW64;.Trid
	0x0260:  656e 742f 372e 303b 2054 6f75 6368 3b20  ent/7.0;.Touch;.
	0x0270:  7276 3a31 312e 3029 206c 696b 6520 4765  rv:11.0).like.Ge
	0x0280:  636b 6f0d 0a48 6f73 743a 2077 7777 2e67  cko..Host:.www.g
	0x0290:  6f6f 676c 652e 636f 6d0d 0a44 4e54 3a20  oogle.com..DNT:.
	0x02a0:  310d 0a43 6f6e 6e65 6374 696f 6e3a 204b  1..Connection:.K
	0x02b0:  6565 702d 416c 6976 650d 0a43 6f6f 6b69  eep-Alive..Cooki
	0x02c0:  653a 204e 4944 3d38 373d 506c 5267 4959  e:.NID=87=PlRgIY
	0x02d0:  6a52 5431 6a67 6146 724b 7567 425f 4769  jRT1jgaFrKugB_Gi
	0x02e0:  7948 4374 4e76 4b51 6d4e 3262 3636 3554  yHCtNvKQmN2b665T
	0x02f0:  335f 6b7a 3341 6d37 2d6e 7964 5f6a 3531  3_kz3Am7-nyd_j51
	0x0300:  4176 4d6e 7954 5154 4743 6b79 5359 4149  AvMnyTQTGCkySYAI
	0x0310:  4d49 3348 6e51 4875 7946 3655 386b 2d32  MI3HnQHuyF6U8k-2
	0x0320:  3257 6b49 7349 4336 455f 7157 4830 706f  2WkIsIC6E_qWH0po
	0x0330:  6b58 6241 7a66 4a62 326d 5277 616e 4e49  kXbAzfJb2mRwanNI
	0x0340:  3036 4161 5767 2d66 7673 494e 4a63 4143  06AaWg-fvsINJcAC
	0x0350:  3752 6477 4353 324d 386e 714f 717a 6241  7RdwCS2M8nqOqzbA
	0x0360:  3b20 4f47 5043 3d38 3833 3836 3435 3736  ;.OGPC=883864576
	0x0370:  2d33 303a 3831 3235 3632 3433 322d 3133  -30:812562432-13
	0x0380:  3a32 3635 3338 3239 3132 2d31 353a 3231  :265382912-15:21
	0x0390:  3438 3637 3936 382d 3135 3a35 3036 3231  4867968-15:50621
	0x03a0:  3833 2d34 3a35 3036 3231 3934 2d31 333a  83-4:5062194-13:
	0x03b0:  3530                                     50
11:17:55.000000 fc:fb:fb:31:99:c0 > 00:e0:ed:1f:15:a9, ethertype IPv4 (0x0800), length 66: truncated-ip - 900 bytes missing! (tos 0x0, ttl  64, id 25961, offset 0, flags [none], proto: TCP (6), length: 952, bad cksum 0 (->cd70)!) 10.75.43.55.56890 > 74.125.196.103.443: P 927:1839(912) ack 1 win 65535
	0x0000:  00e0 ed1f 15a9 fcfb fb31 99c0 0800 4500  .........1....E.
	0x0010:  03b8 6569 0000 4006 0000 0a4b 2b37 4a7d  ..ei..@....K+7J}
	0x0020:  c467 de3a 01bb 0000 18d5 0000 fbde 5018  .g.:..........P.
	0x0030:  ffff 0000 0000 3632 3230 322d 383a 0d0a  ......62202-8:..
	0x0040:  0d0a                                     ..
'''
