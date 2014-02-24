
TEX_NAME=flickr

TEX_BUILD_FLAGS= -interaction=nonstopmode -file-line-error

CLEAN_CMD=rm -f
CLEAN_CMD+= *.backup *.aux *.toc *.ind *.idx *.ilg *.blg *.log *.out *.bbl *.dvi
CLEAN_CMD+= *.nav *.pyg *.snm *.lof *.glg *.glo *.gls *.acn *.acr *.alg *.ist
CLEAN_CMD+= 2> /dev/null

#AUTOMATIC OS DETECTION
OS=$(shell uname -s)
ifeq ($(OS),Darwin)
PDFVIEWER=open
else
ifeq ($(OS),Linux)
PDFVIEWER=evince
endif
endif

.PHONY: build clean

build: $(TEX_NAME).pdf
	@$(CLEAN_CMD)

clean:
	@$(CLEAN_CMD)
	@rm -f $(TEX_NAME).pdf
	@echo "# cleaned" ;

view:
	@$(PDFVIEWER) $(TEX_NAME).pdf > /dev/null 2>&1 &

%.pdf: %.tex $(wildcard *.tex)
	@$(CLEAN_CMD)
	@echo "# building <$@> stage 1" ;										\
	pdflatex $(TEX_BUILD_FLAGS) "$<" > $@.stdout 2> $@.stderr ;				\
	OK=$$? ;																\
	if [ $$OK -eq 0 ]; then													\
		echo "# building <$@> stage 2" ;									\
		pdflatex $(TEX_BUILD_FLAGS) "$<" > $@.stdout 2> $@.stderr ;			\
		OK=$$? ;															\
	fi;																		\
	if [ $$OK -eq 0 ]; then													\
		echo "# building <$@> stage 3" ;									\
		pdflatex $(TEX_BUILD_FLAGS) "$<" > $@.stdout 2> $@.stderr ;			\
		OK=$$? ;															\
	fi;																		\
	if [ $$OK -eq 0 ]; then													\
		echo "# build <$@> finished" ;										\
	else																	\
		cat $@.stdout ;														\
		rm -f $@ ;															\
	fi;																		\
	rm -f $@.stdout $@.stderr ;
	@$(CLEAN_CMD)
