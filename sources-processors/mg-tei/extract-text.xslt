<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0">
    <xsl:template match="/TEI/text">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Untitled Document</title>
                    </titleStmt>
                    <publicationStmt>
                        <p>Unpublished</p>
                    </publicationStmt>
                    <sourceDesc>
                        <p>No source</p>
                    </sourceDesc>
                </fileDesc>
            </teiHeader>
            <xsl:copy-of select="." />
        </TEI>
    </xsl:template>
    <xsl:template match="text()"/>
</xsl:stylesheet>