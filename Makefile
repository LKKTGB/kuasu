env ?= stage

SERVICES = $(shell ls services)
FORMAT_SERVICES = $(SERVICES:%=fmt/%)

deploy/backend:
	git archive -o kuasu.zip HEAD:services/backend && \
	az webapp deployment source config-zip --resource-group kuasu --name kuasu-$(env) --src kuasu.zip && \
	rm kuasu.zip
azure/login:
	az login
azure/logout:
	az logout
azure/view:
	open https://kuasu-$(env).azurewebsites.net

$(FORMAT_SERVICES): fmt/%:
	cd services/$(@F) && $(MAKE) fmt
fmt: $(addprefix fmt/, $(SERVICES))
