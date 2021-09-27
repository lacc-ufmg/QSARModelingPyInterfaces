.PHONY:
mypy:
	@mypy ./GUI --pretty --disable-error-code import || true