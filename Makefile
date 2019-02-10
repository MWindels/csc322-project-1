vcheck1:
	@python3 vcheck1.py

vcheck3:
	@python3 vcheck3.py

.PHONY: clean
clean:
	@rm -r __pycache__
