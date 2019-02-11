vcheck1:
	@python3 vcheck1.py

vcheck2:
	@python3 vcheck2.py

vcheck3:
	@python3 vcheck3.py

vcheck4:
	@python3 vcheck4.py

.PHONY: clean
clean:
	@rm -r __pycache__
	@truncate -s 0 minisat_in.txt
	@truncate -s 0 minisat_out.txt
