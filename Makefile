test_default:
	./videowatermark.py tests/data/1s.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark.png


test_margin:
	./videowatermark.py -p tr tests/data/1s.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark.png


test_postion:
	./videowatermark.py -p br -m 100 tests/data/1s.mp4 /home/rg/repos/priv/pankeisnotdead/images/watermark.png