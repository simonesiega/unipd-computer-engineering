.DEFAULT_GOAL := help

DOCKER := docker compose run --rm --no-deps texlive
BUILD := $(DOCKER) python3 latex/tools/build.py

.PHONY: help course build check all clean

help:
	@echo "Daily repository commands:"
	@echo "  make build COURSE=1/calculus-1"
	@echo "  make all"
	@echo "  make check"
	@echo "  make clean"
	@echo "  make course YEAR=1 COURSE='Calculus 1' SHORT='Calculus' \\"
	@echo "  COURSE_CODE=IN0000225 CHANNEL=B PROFESSOR='Name' SEMESTER=1 \\"
	@echo "  AUTHOR='Ada Lovelace' DATE=2026-08-06 LANGUAGE=english"

course:
	@test -n "$(YEAR)" || (echo "YEAR is required" >&2; exit 2)
	@test -n "$(COURSE)" || (echo "COURSE is required" >&2; exit 2)
	@test -n "$(SHORT)" || (echo "SHORT is required" >&2; exit 2)
	@test -n "$(PROFESSOR)" || (echo "PROFESSOR is required" >&2; exit 2)
	@test -n "$(SEMESTER)" || (echo "SEMESTER is required" >&2; exit 2)
	@test -n "$(AUTHOR)" || (echo "AUTHOR is required" >&2; exit 2)
	@test -n "$(DATE)" || (echo "DATE is required" >&2; exit 2)
	@test -n "$(LANGUAGE)" || (echo "LANGUAGE is required" >&2; exit 2)
	$(DOCKER) python3 latex/tools/create_course.py \
		--year "$(YEAR)" \
		--course "$(COURSE)" \
		--short-course "$(SHORT)" \
		--professor "$(PROFESSOR)" \
		$(if $(strip $(COURSE_CODE)),--course-code "$(COURSE_CODE)" )$(if $(strip $(CHANNEL)),--channel "$(CHANNEL)" )--semester "$(SEMESTER)" \
		--author "$(AUTHOR)" \
		--date "$(DATE)" \
		--language "$(LANGUAGE)"

build:
	@test -n "$(COURSE)" || (echo "COURSE is required, for example COURSE=1/calculus-1" >&2; exit 2)
	$(BUILD) "$(COURSE)"

check:
	pre-commit run --all-files --show-diff-on-failure

all:
	$(BUILD) --all --keep-going

clean:
	$(DOCKER) python3 -c "import shutil; shutil.rmtree('.build', ignore_errors=True)"
