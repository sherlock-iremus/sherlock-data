<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Désactive la déclaration XML dans le résultat -->
  <xsl:output method="text" encoding="UTF-8" />

  <!-- Template pour capturer tout le texte -->
  <xsl:template match="/">
    <xsl:apply-templates />
  </xsl:template>

  <!-- Ignore tous les éléments, mais récupère leur texte -->
  <xsl:template match="*">
    <xsl:apply-templates select="text() | *" />
  </xsl:template>

  <!-- Conserve le texte brut et ajoute des espaces entre -->
  <xsl:template match="text()">
    <xsl:value-of select="normalize-space()" />
    <xsl:text> </xsl:text>
  </xsl:template>

</xsl:stylesheet>
