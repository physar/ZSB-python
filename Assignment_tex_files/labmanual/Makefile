################################ MACROS ################################
#
# DOC: the document
# FIG: directory for figures
# BIB: bibliography database
# BST: bibliography style
# SEL: selected pages; e.g., "odd", "even", "2\:5,6"
#
DOC = zsbmanual
FIG = images
BIB = 
BST =
SEL = ""
 
############################### PROGRAMS ###############################
#
TEX = latex
BIBTEX = bibtex
DVISELECT = dviselect
DVIPS = dvips -t a4 -Ppdf -G0
#changing prepress to screen produces much smaller files 
PS2PDF = ps2pdf -dPDFSETTINGS=/prepress -dEmbedAllFonts=true -dEncodeGrayImages=true -dEncodeMonoImages=true -dEncodeColorImages=true 
#PS2PDF = ps2pdf -dPDFSETTINGS=/screen -dEmbedAllFonts=true \
        -dEncodeGrayImages=true -dAutoFilterGrayImages=false \
        -dGrayImageFilter=/FlateEncode \
        -dEncodeMonoImages=true -dAutoFilterMonoImages=false \
        -dMonoImageFilter=/FlateEncode \
        -dEncodeColorImages=true -dAutoFilterColorImages=false \
        -dColorImageFilter=/FlateEncode
DVILJ4 = dvilj4
XDVI = xdvi -expert -hush -s 6 -geometry -0+0
XPS = ghostview -watch -geometry -0+0
XPDF = acroread 
PRINT = lpr -Plaser1
MAKE = make
RM = rm -f
 
############################ Inference Rules ###########################
#
.SUFFIXES: .tex .dvi .ps .lj .aux .bbl .pdf
.tex.dvi:
	$(TEX) $<
	$(TEX) $<
.dvi.ps:
	$(DVIPS) -o $@ $< 
.dvi.lj:
	$(DVILJ4) $<
.tex.aux:
	$(TEX) $<
.aux.bbl:
	$(BIBTEX) $*
.ps.pdf:
	$(PS2PDF) $<

################################# Rules ################################
#
all:    dvi
 
aux:    $(DOC).aux
bib:    $(DOC).bbl
 
dvi:    $(DOC).dvi
dvisel: $(DOC)-$(SEL).dvi
ps: $(DOC).ps
pssel:  $(DOC)-$(SEL).ps
lj: $(DOC).lj
ljsel:  $(DOC)-$(SEL).lj

pdf:	$(DOC).pdf

xdvi:   $(DOC).dvi
	$(XDVI) $<
xsel:   $(DOC)-$(SEL).dvi
	$(XDVI) $<
xps:    $(DOC).ps
	$(XPS) $<
xpdf:    $(DOC).pdf
	$(XPDF) $<
xpssel: $(DOC)-$(SEL).ps
	$(XPS) $<
 
print:  $(DOC).ps
	$(PRINT) $<
prsel:  $(DOC)-$(SEL).ps
	$(PRINT) $<
 
$(DOC)-$(SEL).dvi: $(DOC).dvi
	$(DVISELECT) $(SEL) $< $@
 
fig:
	@cd $(FIG); $(MAKE) DIR=$(FIG)
 
new:
	$(RM) $(DOC).dvi
 
clean:
	$(RM) $(DOC).aux $(DOC).log
	$(RM) $(DOC).toc $(DOC).lot $(DOC).lof
	$(RM) $(DOC).ttt $(DOC).lot $(DOC).fff
	$(RM) $(DOC).blg $(DOC).out
	$(RM) $(DOC).dvi $(DOC)-*.dvi
	$(RM) $(DOC).ps $(DOC)-*.ps
	$(RM) $(DOC).pdf
	$(RM) texput.log core
 
distclean: clean
	cd $(FIG); $(MAKE) clean
 
bak:
	bakdir="./BAK/`date | awk '{print $$2"-"$$3}'`"; \
	test ! -d $$bakdir && mkdir -p $$bakdir; \
	cp -f *.tex $$bakdir
