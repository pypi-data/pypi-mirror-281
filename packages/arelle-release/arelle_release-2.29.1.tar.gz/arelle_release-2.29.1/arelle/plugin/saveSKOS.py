'''
Save SKOS is an example of a plug-in to both GUI menu and command line/web service
that will save the concepts a DTS into an RDF file.

See COPYRIGHT.md for copyright information.
'''
from arelle.Version import authorLabel, copyrightLabel

def generateSkos(dts, skosFile):
    try:
        import os, io
        from arelle import XmlUtil, XbrlConst
        from arelle.ViewUtil import viewReferences, referenceURI
        skosNs = "http://www.w3.org/2004/02/skos/core#"
        rdfNs = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        dts.modelManager.showStatus("initializing SKOS document")
        file = io.StringIO('''
  <!DOCTYPE rdf:RDF>
  <nsmap>
  <rdf:RDF xmlns="urn:cgi:classifier:CGI:XBRL:201204#" xml:base="urn:cgi:classifierScheme:CGI:XBRL:201204" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:owl2xml="http://www.w3.org/2006/12/owl2-xml#" xmlns:p1="#" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:xsd="http://www.w3.org/2001/XMLSchema#" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xbrl-201204="urn:cgi:classifier:CGI:XBRL:201204#" xmlns:skos="http://www.w3.org/2004/02/skos/core#">
  <owl:Ontology rdf:about="" />
  <!-- Annotation properties -->
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/date" />
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/source" />
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/title" />
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/description" />
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/contributor" />
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/creator" />
  <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/format" />
  <owl:AnnotationProperty rdf:about="http://www.w3.org/2002/07/owl#versionInfo" />
  <!-- Object Properties -->
  <!--  http://www.w3.org/2004/02/skos/core#broader -->
  <owl:ObjectProperty rdf:about="http://www.w3.org/2004/02/skos/core#broader" />
  <!--  http://www.w3.org/2004/02/skos/core#changeNote -->
  <owl:ObjectProperty rdf:about="http://www.w3.org/2004/02/skos/core#changeNote" />
  <!--  http://www.w3.org/2004/02/skos/core#hasTopConcept -->
  <owl:ObjectProperty rdf:about="http://www.w3.org/2004/02/skos/core#hasTopConcept" />
  <!--  http://www.w3.org/2004/02/skos/core#inScheme  -->
  <owl:ObjectProperty rdf:about="http://www.w3.org/2004/02/skos/core#inScheme" />
  <!--  http://www.w3.org/2004/02/skos/core#topConceptOf  -->
  <owl:ObjectProperty rdf:about="http://www.w3.org/2004/02/skos/core#topConceptOf" />
  <!-- Data properties -->
  <!--  http://www.w3.org/2004/02/skos/core#definition -->
  <owl:DatatypeProperty rdf:about="http://www.w3.org/2004/02/skos/core#definition" />
  <!--  http://www.w3.org/2004/02/skos/core#editorialNote -->
  <owl:DatatypeProperty rdf:about="http://www.w3.org/2004/02/skos/core#editorialNote" />
  <!--  http://www.w3.org/2004/02/skos/core#historyNote -->
  <owl:DatatypeProperty rdf:about="http://www.w3.org/2004/02/skos/core#historyNote" />
  <!--  http://www.w3.org/2004/02/skos/core#notation -->
  <owl:DatatypeProperty rdf:about="http://www.w3.org/2004/02/skos/core#notation" />
  <!--  http://www.w3.org/2004/02/skos/core#prefLabel -->
  <owl:DatatypeProperty rdf:about="http://www.w3.org/2004/02/skos/core#prefLabel" />
  <!-- Classes -->
  <!--  http://www.w3.org/2002/07/owl#Thing -->
  <owl:Class rdf:about="http://www.w3.org/2002/07/owl#Thing" />
  <!--  http://www.w3.org/2004/02/skos/core#Concept -->
  <owl:Class rdf:about="http://www.w3.org/2004/02/skos/core#Concept" />
  <!--  http://www.w3.org/2004/02/skos/core#ConceptScheme -->
  <owl:Class rdf:about="http://www.w3.org/2004/02/skos/core#ConceptScheme" />
  <!-- Individuals -->
</rdf:RDF></nsmap>
 <!--  Generated by the Arelle(r) http://arelle.org -->
'''
         )
        from arelle.ModelObjectFactory import parser
        parser, parserLookupName, parserLookupClass = parser(dts,None)
        from lxml import etree
        xmlDocument = etree.parse(file,parser=parser,base_url=skosFile)
        file.close()
        xmlRootElement = xmlDocument.getroot()
        #xmlDocument.getroot().init(self)  ## is this needed ??
        for rdfElement in  xmlDocument.iter(tag="{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF"):
            break
        numSchemes = 0
        numConcepts = 0

        # use presentation relationships for broader and narrower concepts
        relationshipSet = dts.relationshipSet(XbrlConst.parentChild)

        def conceptUri(concept):
            return concept.qname.namespaceURI + "#" + concept.qname.localName

        def namespaceUri(qname):
            return qname.namespaceURI + "#" + qname.prefix

        priorSchemeSibling = None
        schemeNamespaces = set()

        dts.modelManager.showStatus("setting SKOS concepts from XBRL concepts")
        for qn, concept in sorted(dts.qnameConcepts.items(), key=lambda item:str(item[0])):
            if concept.modelDocument.targetNamespace not in (
                     XbrlConst.xbrli, XbrlConst.link, XbrlConst.xlink, XbrlConst.xl,
                     XbrlConst.xbrldt):
                if qn.namespaceURI not in schemeNamespaces:
                    # add conceptScheme
                    numSchemes += 1
                    skosElt = etree.Element("{http://www.w3.org/2004/02/skos/core#}ConceptScheme")
                    skosElt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", namespaceUri(qn))
                    elt = etree.SubElement(skosElt, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}type")
                    elt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource",
                            "http://www.w3.org/2002/07/owl#Thing")
                    elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}notation")
                    elt.text = str(qn.prefix)
                    schemeNamespaces.add(qn.namespaceURI)
                    if priorSchemeSibling is not None:
                        priorSchemeSibling.addnext(skosElt)
                    else:
                        rdfElement.append(skosElt)
                    priorSchemeSibling = skosElt

                numConcepts += 1
                skosElt = etree.SubElement(rdfElement, "{http://www.w3.org/2004/02/skos/core#}Concept")
                skosElt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", conceptUri(concept))
                elt = etree.SubElement(skosElt, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}type")
                elt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource",
                        "http://www.w3.org/2002/07/owl#Thing")
                elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}notation")
                elt.text = str(concept.qname)
                definition = concept.label(preferredLabel=XbrlConst.documentationLabel, lang="en", strip=True, fallbackToQname=False)
                if definition:
                    elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}definition")
                    elt.text = definition
                else:   # if no definition, look for any references
                    references = viewReferences(concept)
                    if references:
                        elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}definition")
                        elt.text = references
                    linkedReferenceURI = referenceURI(concept)
                    if linkedReferenceURI:    # link to reference
                        elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}definition")
                        elt.text = linkedReferenceURI
                labelsRelationshipSet = dts.relationshipSet(XbrlConst.conceptLabel)
                if labelsRelationshipSet:
                    for modelLabelRel in labelsRelationshipSet.fromModelObject(concept):
                        label = modelLabelRel.toModelObject
                        if label.role == XbrlConst.standardLabel:
                            elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}prefLabel")
                            elt.set("{http://www.w3.org/XML/1998/namespace}lang", label.xmlLang)
                            elt.text = label.text.strip()
                for rel in relationshipSet.fromModelObject(concept): # narrower
                    elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}narrower")
                    elt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", conceptUri(rel.toModelObject))
                for rel in relationshipSet.toModelObject(concept): # broader
                    elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}broader")
                    elt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", conceptUri(rel.fromModelObject))

                elt = etree.SubElement(skosElt, "{http://www.w3.org/2004/02/skos/core#}inScheme")
                elt.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource",
                        namespaceUri(qn))

        dts.modelManager.showStatus("saving SKOS file")
        fh = open(skosFile, "w", encoding="utf-8")
        XmlUtil.writexml(fh, xmlDocument, encoding="utf-8")
        fh.close()

        dts.info("info:saveSKOS",
                 _("SKOS of %(entryFile)s has %(numberOfConcepts)s concepts in SKOS RDF file %(skosOutputFile)s."),
                 modelObject=dts,
                 entryFile=dts.uri, numberOfConcepts=numConcepts, skosOutputFile=skosFile)
        dts.modelManager.showStatus("ready", 3000)
    except Exception as ex:
        dts.error("exception",
            _("SKOS generation exception: %(error)s"), error=ex,
            modelXbrl=dts,
            exc_info=True)

def saveSkosMenuEntender(cntlr, menu, *args, **kwargs):
    # Extend menu with an item for the savedts plugin
    menu.add_command(label="Save SKOS RDF",
                     underline=0,
                     command=lambda: saveSkosMenuCommand(cntlr) )

def saveSkosMenuCommand(cntlr):
    # save DTS menu item has been invoked
    if cntlr.modelManager is None or cntlr.modelManager.modelXbrl is None:
        cntlr.addToLog("No taxonomy loaded.")
        return

        # get file name into which to save log file while in foreground thread
    skosFile = cntlr.uiFileDialog("save",
            title=_("arelle - Save SKOS RDF file"),
            initialdir=cntlr.config.setdefault("skosFileDir","."),
            filetypes=[(_("SKOS file .rdf"), "*.rdf")],
            defaultextension=".rdf")
    if not skosFile:
        return False
    import os
    cntlr.config["skosFileDir"] = os.path.dirname(skosFile)
    cntlr.saveConfig()

    import threading
    thread = threading.Thread(target=lambda
                                  _dts=cntlr.modelManager.modelXbrl,
                                  _skosFile=skosFile:
                                        generateSkos(_dts, _skosFile))
    thread.daemon = True
    thread.start()

def saveSkosCommandLineOptionExtender(parser, *args, **kwargs):
    # extend command line options with a save DTS option
    parser.add_option("--save-skos",
                      action="store",
                      dest="skosFile",
                      help=_("Save SKOS semantic definition in specified RDF file."))

def saveSkosCommandLineXbrlRun(cntlr, options, modelXbrl, *args, **kwargs):
    # extend XBRL-loaded run processing for this option
    if getattr(options, "skosFile", False):
        if cntlr.modelManager is None or cntlr.modelManager.modelXbrl is None:
            cntlr.addToLog("No taxonomy loaded.")
            return
        generateSkos(cntlr.modelManager.modelXbrl, options.skosfile)


__pluginInfo__ = {
    'name': 'Save SKOS',
    'version': '0.9',
    'description': "This plug-in adds a feature to output the taxonomy in a SKOS OWL file. "
                   "This provides a semantic definition of taxonomy contents.",
    'license': 'Apache-2',
    'author': authorLabel,
    'copyright': copyrightLabel,
    # classes of mount points (required)
    'CntlrWinMain.Menu.Tools': saveSkosMenuEntender,
    'CntlrCmdLine.Options': saveSkosCommandLineOptionExtender,
    'CntlrCmdLine.Xbrl.Run': saveSkosCommandLineXbrlRun,
}
