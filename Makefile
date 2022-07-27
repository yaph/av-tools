test_default:
#./videowatermark.py tests/data/landscape.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark-100.png
	./videowatermark.py tests/data/portrait.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark-100.png


test_margin:
	./videowatermark.py -p tr tests/data/landscape.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark-100.png


test_postion:
	./videowatermark.py -p br -m 100 tests/data/landscape.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark-100.png