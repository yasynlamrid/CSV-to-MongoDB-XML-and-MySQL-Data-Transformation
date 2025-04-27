<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<head>
  <title>Nuclear Explosions</title>
  <xsl:processing-instruction name="xml-stylesheet">type="text/css" href="CSS_nuclear_explosions.css"</xsl:processing-instruction>
</head>
<body>
  <h1>Nuclear Explosions</h1>
  <table border="1">
    <tr>

      <th>Source Country</th>
      <th>Deployment Location</th>
      <th>Source</th>
      <th>Magnitude (Body)</th>
      <th>Magnitude (Surface)</th>
      <th>Yield (Lower)</th>
      <th>Yield (Upper)</th>
      <th>Purpose</th>
      <th>Name</th>
      <th>Type</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Depth</th>
      <th>Date</th>
    </tr>
    <xsl:for-each select="nuclear_explosions/nuclear_explosion">
      <tr>

        <td><xsl:value-of select="weapon_source_country"/></td>
        <td><xsl:value-of select="weapon_deployment_location"/></td>
        <td><xsl:value-of select="data/source"/></td>
        <td><xsl:value-of select="data/magnitude/body"/></td>
        <td><xsl:value-of select="data/magnitude/surface"/></td>
        <td><xsl:value-of select="data/yeild/lower"/></td>
        <td><xsl:value-of select="data/yeild/upper"/></td>
        <td><xsl:value-of select="data/purpose"/></td>
        <td><xsl:value-of select="data/name"/></td>
        <td><xsl:value-of select="data/type"/></td>
        <td><xsl:value-of select="location/coordinates/latitude"/></td>
        <td><xsl:value-of select="location/coordinates/longitude"/></td>
        <td><xsl:value-of select="location/coordinates/depth"/></td>
        <td>
        <xsl:value-of select="date/day" />/
        <xsl:value-of select="date/month" />/
        <xsl:value-of select="date/year" />
        </td>
      </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>