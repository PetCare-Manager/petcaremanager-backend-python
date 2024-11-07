help:
	@echo ""
	@echo "Usage:"
	@echo "   make                 Print the help"
	@echo "   make build           Install the pip packages from requirements.txt"
	@echo "   make start           Start the project"
	@echo ""

build:
	@if [ -z "$(VIRTUAL_ENV)" ]; then \
		echo "\033[0;31mError: Virtual environment is not activated.\033[0m"; \
		exit 1; \
	fi
	pip install -r requirements.txt

start:
	@if [ -z "$(VIRTUAL_ENV)" ]; then \
		echo "\033[0;31mError: Virtual environment is not activated.\033[0m"; \
		exit 1; \
	fi
	uvicorn main:app --reload
