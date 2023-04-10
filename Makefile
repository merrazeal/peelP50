.PHONY: venv

venv: ver := 3.11.2
venv: msg1 := "Вирутальное окружение существует."
venv: msg2 := "Виртуальное окружение установлено, активируйте его."
venv:
	@if [ -d "./venv/" ]; \
		then echo "$(msg1)"; \
		else \
			python$(ver) -m venv venv; \
			echo "$(msg2)"; \
	fi;

install:
		pip3 install -r requirements.txt;

run:
		gunicorn main:app;
