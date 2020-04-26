env ?= testing

azure/deploy:
	git archive -o kuasu.zip HEAD && \
	az webapp deployment source config-zip --resource-group kuasu --name kuasu-$(env) --src kuasu.zip && \
	rm kuasu.zip
azure/login:
	az login
azure/view:
	open https://kuasu-$(env).azurewebsites.net
fmt:
	isort -rc . && black .
