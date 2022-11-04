test_default:
#./videowatermark.py tests/data/landscape.mp4 ~/repos/priv/pankeisnotdead/images/watermark-100.png
	./videowatermark.py tests/data/portrait.mp4 ~/repos/priv/pankeisnotdead/images/watermark-100.png


test_margin:
	./videowatermark.py -p tr tests/data/landscape.mp4 ~/repos/priv/pankeisnotdead/images/watermark-100.png


test_postion:
	./videowatermark.py -p br -m 100 tests/data/landscape.mp4 ~/repos/priv/pankeisnotdead/images/watermark-100.png


test_addscreens:
	./addscreens.py tests/data/portrait.mp4 \
		--start ~/Videos/ukealong/previews/rumba-picking-pattern-pmipmipm-41231231.png \
		--end ~/repos/priv/ukealong/images/slides/video-endscreen-portrait.png \
