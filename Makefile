make: Makefile
	cat Makefile
git-all:
	git add --all
git-commit:
	git commit --allow-empty --allow-empty-message -m ''
git-commit-amend:
	git commit --allow-empty --allow-empty-message -m '' --amend
git-push-origin:
	git push origin master
git-push-heroku:
	git push heroku master
git-push-github:
	git push github master
heroku-ps:
	heroku ps
heroku-open:
	heroku open
heroku-local:
	heroku local
heroku-local-web:
	heroku local web
heroku-local-worker:
	heroku local worker
heroku-logs:
	heroku logs
heroku-logs-app:
	heroku logs --source app
heroku-logs-heroku:
	heroku logs --source heroku
heroku-run-bash:
	heroku run bash
heroku-run-upgrade:
	heroku run upgrade
heroku-config:
	heroku config:add key=
pipenv-run:
	pipenv run
pipenv-shell:
	pipenv shell
pipenv-install:
	pipenv install
pipenv-install-requests:
	pipenv install requests
pipenv-install-telepot:
	pipenv install telepot
