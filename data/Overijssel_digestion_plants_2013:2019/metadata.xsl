<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  	xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xmlns:gmx="http://www.isotc211.org/2005/gmx"
  	xmlns:srv="http://www.isotc211.org/2005/srv"
  	xmlns:gco="http://www.isotc211.org/2005/gco"
  	xmlns:gml="http://www.opengis.net/gml"
  	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  	xmlns:xlink="http://www.w3.org/1999/xlink"
    version="2.0">

  	<xsl:output method="html" version="4.0" encoding="iso-8859-1" indent="yes" omit-xml-declaration="yes"/>

	<xsl:template match="/">
	  	<html>
	  		<head>
				<title>
					<xsl:apply-templates select="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title"/>
				</title>
				<style>
				 	html {
	    				overflow-y:scroll;
	    				overflow-x:hidden;
					}
					body {
					    background-color:#FFFFFF;
					    margin:0px auto 20px auto;
					    font-family:Verdana;
						border-left:1px solid #AAAAAA;
						border-right:1px solid #AAAAAA;
						width: 1100px;
						padding:0px 20px;
					}

					body.background-acceptance {
						background-color:#f3f7d4;
					}

					p {
						font-family:Verdana;
						font-size:16px;
						color:#000000;
						line-height:25px;
						margin-top:0;
						margin-bottom:0;
					}

					a.link {
						text-decoration:underline;
					}

					a.link:hover {
						color:#FF0000;
					}

					p.titel {
						color:#A50821;
						font-weight:bold;
					}

					p.bestandsnaam {
						font-family:Verdana;
						font-size:21px;
						color:#000000;
						line-height:25px;
					}

					p.contacttitel {
						color:#A50821;
					}

					div.logo {
						margin-top:20px;margin-bottom:20px;
					}

					div.titelbalk {
						margin-top:20px;margin-bottom:20px;
					}

					h1.titel {
						padding:.3em .5em;
						border-radius:0 12px 0 0;
						background-color:#831625;
						margin-left:0;
						margin-right:0;
						color:#ffffff;
						font-size:1.625em;
						font-weight:bold;
						font-style:normal;
						line-height:47px;
					}

					a.titel-url {
						font-size: 15px;
						color: white;
					}

					.deel {
						margin-top:20px;
						margin-bottom:20px;
					}

					.blok {
						margin-bottom:20px;
					}

					.proclaimer {
						margin-top:40px;
					}


					.inspringen {
						padding-left:25px;
					}

					.spatie {
						margin-right:5px;
					}

					#wie { display:none; }
					#waar { display:none; }
					#wanneer { display:none; }
					#details { display:none; }

					div.tabs:after {content:'';display:block;clear: both;}
					a.tabs {height:100%;width:100%;display:block;}
					.grid {background-repeat:repeat;margin-left: -100%;margin-right: -100%;padding-left: 100%;padding-right: 100%;margin-top:20px;margin-bottom:20px;padding-top:5px;padding-bottom:5px;}
					.grid:after {content:'';display:block;clear: both;}


					.toptaak-element {float:left;width:19.95%;height:85px;display:block;}
					.toptaak-outer {height:100%;padding:1px;}
					.toptaak-inner {height:100%;background-color:#255c9f;}
					.toptaak-inner-active {height:100%;background-color:#0096D2;}
					.toptaak-inner:hover {background-color:#0096D2;cursor:pointer;}
					.toptaak-titel {color:#ffffff;display:inline-block;text-align:left;margin-top:13px;margin-left:57px;line-height:1.2em;font-size:18px;padding-right:20px;}

					#tabs-beheer {margin-left:auto;margin-right:auto;width:40%;}
					.toptaak-element-beheer {float:left;width:50%;height:85px;display:block;}

					.row {margin-right: -15px;margin-left: -15px;}
					.row:before {display: table;content: " ";}
					.row:after {display: table;content: " ";clear: both;}
					.col-md-7 {width: 58.33333333%;position: relative;float: left;min-height: 1px;padding-right: 15px;padding-left: 15px;}
					.pull-right {float: right !important;}

					.watIcon {background-image:url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAABlCAYAAADd5LqmAAAAB3RJTUUH3woGDwAqkIDNzAAAAAlwSFlzAAALEQAACxEBf2RfkQAAAARnQU1BAACxjwv8YQUAAASSSURBVHja7Vy/MytRFN68UaiUGko6Ggoz0WgoNQyFlFJq/AP8D0qFgiYzFJQ0GoWCJjpKDaWG7r791r2xNmvvOXfP2U1m8s3cJ57k+nL32/M7GsaYqC68vLyYq6ur6OPjI/n+5uYmWl1dTR6vra1FzWazUbgByFe5Pj8/zcHBgaFid3fX4DV5e1VK/PLykkw6i+fn5743UBnxVqsVTPyvNzA0xB3SElInfnx8LEYcsPdLsnfDKFqb9/d3Mzk5qbF1YoX+qTGPsbe3p7IvTKwqeZx6p9NR2Ru+QZX82dmZ1tY9p6ZG/uTkRI28gxr5brc7vOQ1sbm5mXzVNJWaEZ++qdTA9vb2zzdannVubk7Uszq8vb31PKzaySMel0a73Y5ij/0T42udvI0AxTAzM9MX16sGZevr6ypyqYS8PanSJ55HXJ28sfIBgRAUpYCVkHdXgJO3bm1t/Xna6aUaz+fh6enJnJ+fJ48vLi6iiYmJXsUAnjM2sQ3qXpWTl8TQedgR+UHAiPyI/Ij8EGFEfkQ+AGN1/WKUA+MVuSANQJDWarV+p3pFqCIkduvu7s7s7+97Q+LT01NvOFxZMoL4nIuHhwfvG1Aj3el0gjMooNlsVkuemzERoE9egXSCvA6gGHkt0g7dbleHPDStDR95tpNCP2hxcREWpC4X0QOZ/NfXl2m327AgUWzG6ub9DYpErM2tHEUFJ6/m8WLJ7nUAwkxlXaftYOv7heRzNX94eGgWFhZqlTOlvv8rqsRNOT8/j3ikVuLA0tKS/0mDIpMsKIXW5J+QyQxoUrJ5kAN/SIwaOBXxfYB5gqwJE4cNob3kx6amprzSQvvw6OgI0iKXn8tgY2OD9sSi00PQVaQ9+zNx+JyTSWs+e7NSOxNI66RhExiS5+89wM2HF/pi6PSi5KNc2D155KmXKr3KpHl/wV5N0u8PbuvAoY2Pj4vfrPG+UbwvyTAEF50eHx/Fic/OzpKJlyKPTp40dnZ2eC/g6lxT7760T0zzkc4wEMsJBskGjWBp1ohmuQginy6OSoEcEqQRoneNKSau3stovna9A2zZaOh9eXk56HVs8tfX19Lcw/QOcHVmS8+i4ASDZTU/EHoHWLJxc+uSCNU7m7ybW5dEsN655O/v78XJo/sXCq7mB0bvAPnk0TeVZv1rqFmT/O3trTT3UnpnkddIPlZWVqohr5H2kdv00XfO3CddiieTmAnOglrSw0qP9KarHKST1zh1Ugk7+u4VoA/myu7sTy5oFJd88TuqeH/lybaqTSNfZbKNMiNl0ALPq0XvQLYyhpOmTofYJp//5O0JiQNXE5efK0nbTyjuBrqlOVvARXaIqJZkW4K4ISYjtQ/Yx3kEjEafQxvo6T4UXjFEl0c8QZFkpD/rxAEsSqnZAy1L4wN1um+gZONkEp86KWCrbSg0iziGgUx5WVXdskFjmtJ5zFuFJ6/Rc0oD1YhSjWnCOxQHvHZI99FwrA1WyCitNmkyeQlbnzNsUQ15LGt3WcAVowwzq5PH8v1hHYS4CG85Heyyi10ldkP7r6+v0fT0dPJ/nE9SSuI/SsPzc1L2GJ4AAAAASUVORK5CYII=");background-position:25px 15px;width:60px !important;height:80px !important;background-repeat:no-repeat;background-size:14px;}
					.wieIcon {background-image:url("data:image/png;base64,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");background-position:15px 15px;width:60px !important;height:80px !important;background-repeat:no-repeat;background-size:35px;}
					.waarIcon {background-image:url("data:image/png;base64,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");background-position:10px 15px;width:60px !important;height:80px !important;background-repeat:no-repeat;background-size:35px;}
					.wanneerIcon {background-image:url("data:image/png;base64,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");background-position:10px 15px;width:60px !important;height:80px !important;background-repeat:no-repeat;background-size:35px;}
					.detailsIcon {background-image:url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEMAAABGCAYAAACXBynAAAAAB3RJTUUH3woGDwA2hIGRgwAAAAlwSFlzAAALEQAACxEBf2RfkQAAAARnQU1BAACxjwv8YQUAAAOZSURBVHja3VyhsuowEG2fQiH7BdQwgykOz5VIMMxgUMzwDfAf4MCAA4NAg6OGGQz8APwAuNwuE95wIZQku2nanpm9hjakp7ubk91wXcaYk2fcbje2XC6dw+HgrNdrp16vO8Vi0en1ek6hUHD/XAxk5NVGoxGLw2AwYM/XW5+wKWu320wG/Lr8krFYLKSIePUQl+UsZ0COiHKB8n2Xy8X5Z3vy1Oh0Olr3TafTfHlGGIYsCAKte1utVr7IiKD9MJVKJT9hMhwOUW/15+cnH54RJT/meR5qjO12mw8yqtUq2+122GHczIfJfD5HEwFy/Q7bAglj1+tVSVyJ0Gg08qFAu90umozz+Zx9MqLQQBPBN3LZ36iVSiUUEfz+P2Nafygd4xsrFI7HY/bJ4DGOAs81b2NnTmdQaIpoZ/te5YqQKZ0R6QESTSEiApAZz9CtUzwj8ipYhdxPn2fGM/r9PnqM1WoVf4HthChjFJritfgrMusPKmMmNEUmyaDQFNyzsk2GSU0hslSvJiY1hQipXU1MawoRUukZSWgKEVLpGYloChFsJ8lX47tJFGQ0RSZWk6Q0hTQZUFvc7/fCPb9J+3aEQAaymuIrGbPZjIneTK1WM04MhaZoNpuoOf73BBn3nEwmxgjhVWoUeLUcR4ZKnJogRPU8hQjg1dh5aGl/ypCh6H0EQUAyH0d3AliXfBh178MKGc+dKF2zqSlIyQC8NmFUDaspOMhyF4oMgG7+sK0pjJABUM0fFEkTqymEZPBMjIJqNk+DphCSQVFsBcgmMorvo9AUQjLgD0WdEfAthtOkKT6SAUYRLoA496UgnUpTxJJB8dbi3lzaNEUsGYwonj9NmsjzjBHxRgYzlD/SqCmkyGBESx8AQo/6EJpJE1bHKarTAN/3nXK5DFt01DgqvQ8UPrFEkfAogN3/qFjshxSxjoFJTaFMBiPMHzpIuiD99QIq/aEK05pCZFLtxdPpBAVj4/nLStJ8glR7MSLCHY/HiU0qDMPEibhDxY1kfx6JQVKaQjtMHgD9AT9fihKbsZdjIzweUOrCwyS1utuSgFC0RcQdOu7EG0mkSFpTiEz7Rur8kbSmICVDtj8rA5VDaCYNdYyJSn/YTJrPQB1jAv0BP5vGQPUQmlFQuJdu/rCpKcjD5Bm+7zNV/QH/mcDzvHR4hUN42m+z2ShdD+GVJiLuoHQz2YJQWlaPVyMfEPoavA/6BhBWSRR2de0X4DjnaMCwjkwAAAAASUVORK5CYII=");background-position:10px 15px;width:60px !important;height:80px !important;background-repeat:no-repeat;background-size:35px;}
				</style>
				 <script>
				 	function tabs(e) {
						var a = e.currentTarget;

						document.getElementById("wat").style.display = "none";
						document.getElementById("tabWat").className = "toptaak-inner";

						document.getElementById("wie").style.display = "none";
						document.getElementById("tabWie").className = "toptaak-inner";

						document.getElementById("waar").style.display = "none";
						document.getElementById("tabWaar").className = "toptaak-inner";

						document.getElementById("wanneer").style.display = "none";
						document.getElementById("tabWanneer").className = "toptaak-inner";

						document.getElementById("details").style.display = "none";
						document.getElementById("tabDetails").className = "toptaak-inner";

						if(a.id == "tabWat") {
							document.getElementById("wat").style.display = "block";
							document.getElementById("tabWat").className = "toptaak-inner-active";
						}
						if(a.id == "tabWie") {
							document.getElementById("wie").style.display = "block";
							document.getElementById("tabWie").className = "toptaak-inner-active";
						}
						if(a.id == "tabWaar") {
							document.getElementById("waar").style.display = "block";
							document.getElementById("tabWaar").className = "toptaak-inner-active";
						}
						if(a.id == "tabWanneer") {
							document.getElementById("wanneer").style.display = "block";
							document.getElementById("tabWanneer").className = "toptaak-inner-active";
						}
						if(a.id == "tabDetails") {
							document.getElementById("details").style.display = "block";
							document.getElementById("tabDetails").className = "toptaak-inner-active";
						}
					}
				 </script>
			</head>
			<body class="">
				<div class="logo">
					<a href="http://www.overijssel.nl">
						<img src="data:image/png;base64,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" class="img-responsive" alt="Responsive image"></img>
					</a>
				</div>
				<div class="titelbalk">
					<h1 class="titel">
						Bestandsbeschrijving Geoportaal
						<a class="titel-url pull-right"
							href="https://www.geoportaaloverijssel.nl"
							target="_blank">
							https://www.geoportaaloverijssel.nl
						</a>
					</h1>
				</div>
				<div class="grid">
					<div class="tabs">
						<div class="toptaak-element">
							<div class="toptaak-outer">
								<div class="toptaak-inner-active" id="tabWat" onclick="tabs(event);">
									<a class="tabs watIcon">
										<span class="toptaak-titel">
											Wat
										</span>
									</a>
								</div>
							</div>
						</div>
						<div class="toptaak-element">
							<div class="toptaak-outer">
								<div class="toptaak-inner" id="tabWie" onclick="tabs(event);">
									<a class="tabs wieIcon">
										<span class="toptaak-titel">
											Wie
										</span>
									</a>
								</div>
							</div>
						</div>
						<div class="toptaak-element">
							<div class="toptaak-outer">
								<div class="toptaak-inner" id="tabWaar" onclick="tabs(event);">
									<a class="tabs waarIcon">
										<span class="toptaak-titel">
											Waar
										</span>
									</a>
								</div>
							</div>
						</div>
						<div class="toptaak-element">
							<div class="toptaak-outer">
								<div class="toptaak-inner" id="tabWanneer" onclick="tabs(event);">
									<a class="tabs wanneerIcon">
										<span class="toptaak-titel">
											Wanneer
										</span>
									</a>
								</div>
							</div>
						</div>
						<div class="toptaak-element">
							<div class="toptaak-outer">
								<div class="toptaak-inner" id="tabDetails" onclick="tabs(event);">
									<a class="tabs detailsIcon">
										<span class="toptaak-titel">
											Details
										</span>
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div id="metadata"></div>
				<xsl:apply-templates/>
				<script async="async" src="https://www.googletagmanager.com/gtag/js?id=UA-132211138-1"></script>
				<script>
					window.dataLayer = window.dataLayer || [];
					function gtag(){dataLayer.push(arguments);}
					gtag('js', new Date());
					gtag('config', 'UA-132211138-1');
				</script>
				<script>
					if(location.href.indexOf('url=') !== -1) {
						document.getElementById("xmlLinkElement").style.display = 'none';
					} else {
						document.getElementById("xmlLink").href = location.href + '?noStyle=true';
						document.getElementById("xmlLink").innerHTML = location.href + '?noStyle=true';
					}
				</script>
			</body>
	  	</html>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata">
		<div id="titel">
			<div class="blok">
				<p class="bestandsnaam">
					<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"/>
				</p>
			</div>
		</div>
		<div id="wat">
			<div class="blok">
				<div id="abstract">
					<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString"/>
				</div>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic/gmd:fileName/gco:CharacterString"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[1]/gco:CharacterString"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/gco:CharacterString"/>
			</div>

		</div>
		<div id="wie">
      <xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty"/>
			<xsl:apply-templates select="gmd:contact/gmd:CI_ResponsibleParty"/>
			<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty"/>
		</div>
		<div id="waar">
			<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicDescription/gmd:geographicIdentifier/gmd:MD_Identifier/gmd:code"/>
			<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox"/>
			<xsl:apply-templates select="gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier"/>
      <xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent"/>
		</div>
		<div id="wanneer">
			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:dateOfNextUpdate/gco:DateTime"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/@codeListValue"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:dateStamp/gco:Date"/>
			</div>

      <div class="blok">
        <xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:description/gco:CharacterString"/>
      </div>

			<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod"/>

		</div>
		<div id="details">
			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode/@codeListValue"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[text() = 'tiff']"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[text() = 'tiff']"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[text() = 'landingpage']"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[text() = 'landingpage']"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL[starts-with(., 'https://www.geoportaaloverijssel.nl/metadata/') or starts-with(., 'https://intern.geoportaaloverijssel.nl/metadata/')]"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[starts-with(text(), 'OGC')]"/>
        <xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[starts-with(text(), 'OGC')]"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[text() != 'tiff' and text() != 'landingpage' and not(starts-with(text(), 'OGC')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://www.geoportaaloverijssel.nl/metadata/')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://intern.geoportaaloverijssel.nl/metadata/'))]"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[text() != 'tiff' and text() != 'landingpage' and not(starts-with(text(), 'OGC')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://www.geoportaaloverijssel.nl/metadata/')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://intern.geoportaaloverijssel.nl/metadata/'))]"/>
				<p id="xmlLinkElement"><strong>XML: </strong><a id="xmlLink" target="_blank"></a></p>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:edition/gco:CharacterString"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:specificUsage/gco:CharacterString"/>
			</div>
			<div class="blok">
				<xsl:apply-templates select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_CompletenessOmission/gmd:result/gmd:DQ_QuantitativeResult/gmd:value/gco:Record"/>
			</div>
			<div class="blok">
				<xsl:apply-templates select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_AbsoluteExternalPositionalAccuracy/gmd:result/gmd:DQ_QuantitativeResult/gmd:value/gco:Record"/>
			</div>

			<xsl:apply-templates select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep"/>

      <div class="blok">
        <xsl:apply-templates select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:source/gmd:LI_Source/gmd:description/gco:CharacterString"/>
      </div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode"/>
			</div>

      <xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords"/>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/@codeListValue"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:fileIdentifier/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:language/gmd:LanguageCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:metadataStandardName/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:metadataStandardVersion/gco:CharacterString"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation/gmd:aggregateDataSetName/gmd:CI_Citation"/>
				<xsl:apply-templates select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode/@codeListValue"/>
				<xsl:apply-templates select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:series/gmd:CI_Series/gmd:name/gco:CharacterString"/>
			</div>

			<div class="blok">
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:fees/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:orderingInstructions/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:turnaround/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString"/>
				<xsl:apply-templates select="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:offLine/gmd:MD_Medium/gmd:name/gmd:MD_MediumNameCode/@codeListValue"/>
			</div>

			<div class="proclaimer">
				<p class="proclaimer-optional">Deze gegevens worden beschikbaar gesteld door het Geoportaal van Overijssel: <a target="_blank" href="https://www.geoportaaloverijssel.nl">https://www.geoportaaloverijssel.nl</a></p>
				<p class="proclaimer-optional">In het Geoportaal staan actuele kaarten en beschrijvingen van die kaarten.</p>
				<p class="proclaimer-optional">Ter referentie zijn vaak ook nog oudere kaarten beschikbaar gesteld.</p>
				<p class="proclaimer-optional">De provincie Overijssel stelt zoveel mogelijk kaarten als "open data" voor iedereen beschikbaar.</p>
				<p class="proclaimer-optional">Heeft u suggesties of vragen? Stuur dan een email naar <a href="mailto:kennishub@overijssel.nl">kennishub@overijssel.nl</a></p>
				<p class="proclaimer-optional">Zie proclaimer: <a target="_blank" href="http://www.overijssel.nl/algemene-onderdelen/proclaimer">http://www.overijssel.nl/algemene-onderdelen/proclaimer</a></p>
			</div>
		</div>
 	</xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString">
  		<xsl:if test=". != ''">
  			<b><xsl:text>Bestandsnaam: </xsl:text></b>
  			<xsl:value-of select="."/>
  		</xsl:if>
  	</xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title">
  		<xsl:if test="gco:CharacterString/. != ''">
  			<xsl:value-of select="."/>
  		</xsl:if>
  	</xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Samenvatting: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource">
		<xsl:if test=". != ''">
			<xsl:if test="contains(gmd:linkage/gmd:URL, '/download/')">
				<xsl:if test="count(../../gmd:onLine/gmd:CI_OnlineResource/gmd:protocol[gco:CharacterString = 'OGC:WFS']) > 0">
					<p>
						<a href="{gmd:linkage/gmd:URL}" target="_blank">
							<xsl:text>Download het bestand naar je eigen omgeving</xsl:text>
						</a>
					</p>
				</xsl:if>
        <xsl:if test="count(../../gmd:onLine/gmd:CI_OnlineResource/gmd:protocol[gmx:Anchor = 'OGC:WFS']) > 0">
					<p>
						<a href="{gmd:linkage/gmd:URL}" target="_blank">
							<xsl:text>Download het bestand naar je eigen omgeving</xsl:text>
						</a>
					</p>
				</xsl:if>
			</xsl:if>
			<xsl:if test="contains(gmd:linkage/gmd:URL, '/viewer/')">
				<p>
					<a href="{gmd:linkage/gmd:URL}" target="_blank">
						<xsl:text>Bekijk de kaart in een viewer</xsl:text>
					</a>
				</p>
			</xsl:if>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic/gmd:fileName/gco:CharacterString">
  		<xsl:if test=". != ''">
  			<div class="blok">
 				<p>
			  		<b><xsl:text>Voorbeeld: </xsl:text></b>
			  		<div class="deel">
			  			<img src="{translate(., '\', '/')}"/>
			  		</div>
			  	</p>
			  </div>
	  	</xsl:if>
  	</xsl:template>
 	<xsl:template match="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Toepassingsschaal: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<xsl:choose>
		  		<xsl:when test=". = 'vector'">
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:text>Vector</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'grid'">
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:text>Grid</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'textTable'">
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:text>Tekst tabel</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'tin'">
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:text>Tin</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'stereoModel'">
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:text>Stereo model</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'video'">
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:text>Video</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:otherwise>
					<p>
		  				<b><xsl:text>Ruimtelijk schema: </xsl:text></b>
		  				<xsl:value-of select="."/>
		  			</p>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Doel van vervaardiging: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue">
 		<xsl:if test=". != ''">
	 		<xsl:choose>
	 			<xsl:when test=". = 'revision'">
	 				<p>
						<b><xsl:text>Laatste wijziging bestand: </xsl:text></b>
		  				<xsl:value-of select="substring(../../../gmd:date/gco:Date,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(../../../gmd:date/gco:Date,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(../../../gmd:date/gco:Date,1,4)"/>
		 			</p>
	 			</xsl:when>
	 		</xsl:choose>
 		</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation/gco:CharacterString">
 		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Gebruiksbeperkingen: </xsl:text></b>
		  		<xsl:value-of select="."/>
	  		</p>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Aanvullende informatie: </xsl:text></b>
		  		<xsl:choose>
					<xsl:when test="substring(substring-after(.,'http'),1,3) = '://'">
						<xsl:value-of select="substring-before(.,'http://')"/>
						<xsl:text> </xsl:text>
						<a href="http://{substring-after(.,'http://')}">
							http://<xsl:value-of select="substring-after(.,'http://')"/>
						</a>
					</xsl:when>
					<xsl:when test="substring(substring-after(.,'https'),1,3) = '://'">
						<xsl:value-of select="substring-before(.,'https://')"/>
						<xsl:text> </xsl:text>
						<a href="https://{substring-after(.,'https://')}">
							https://<xsl:value-of select="substring-after(.,'https://')"/>
						</a>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="."/>
					</xsl:otherwise>
				</xsl:choose>
	  		</p>
  		</xsl:if>
  	</xsl:template>
    <xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty">
   		<xsl:if test=". != ''">
  	 		<div class="blok">
  		 		<b>
  			 		<p>
  			 			<xsl:choose>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'resourceProvider'">
  		 						<xsl:text>Verstrekker</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'custodian'">
  		 						<xsl:text>Beheerder</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'owner'">
  		 						<xsl:text>Eigenaar</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'user'">
  		 						<xsl:text>Gebruiker</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'distributor'">
  		 						<xsl:text>Distributeur</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'originator'">
  		 						<xsl:text>Maker</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'pointOfContact'">
  		 						<xsl:text>Contactpunt</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'principalInvestigator'">
  		 						<xsl:text>Inwinner</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'processor'">
  		 						<xsl:text>Bewerker</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'publisher'">
  		 						<xsl:text>Uitgever</xsl:text>
  		 					</xsl:when>
  		 					<xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'author'">
  		 						<xsl:text>Auteur</xsl:text>
  		 					</xsl:when>
  			 				<xsl:otherwise>
  			 					<xsl:value-of select="gmd:role/gmd:CI_RoleCode/@codeListValue"/>
  			 				</xsl:otherwise>
  		 				</xsl:choose>
  			 			van het bestand
  			 		</p>
  		 		</b>
  		 		<xsl:if test="gmd:organisationName/gco:CharacterString != ''">
  		 			<p>
  		 				<b><xsl:text>Naam organisatie: </xsl:text></b>
  		 				<xsl:value-of select="gmd:organisationName/gco:CharacterString"/>
  		 			</p>
  		 		</xsl:if>
          <xsl:if test="gmd:role/gmd:CI_RoleCode/@codeListValue != ''">
            <p>
              <b><xsl:text>Rol organisatie: </xsl:text></b>
              <xsl:choose>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'resourceProvider'">
                  <xsl:text>verstrekker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'custodian'">
                  <xsl:text>beheerder</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'owner'">
                  <xsl:text>eigenaar</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'user'">
                  <xsl:text>gebruiker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'distributor'">
                  <xsl:text>distributeur</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'originator'">
                  <xsl:text>maker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'pointOfContact'">
                  <xsl:text>contactpunt</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'principalInvestigator'">
                  <xsl:text>inwinner</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'processor'">
                  <xsl:text>bewerker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'publisher'">
                  <xsl:text>uitgever</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'author'">
                  <xsl:text>auteur</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="gmd:role/gmd:CI_RoleCode/@codeListValue"/>
                </xsl:otherwise>
              </xsl:choose>
            </p>
          </xsl:if>
  		 		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL != ''">
  		 			<p>
  		 				<b><xsl:text>Website: </xsl:text></b>
  		 				<xsl:choose>
  							<xsl:when test="substring(substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http'),1,3) = '://'">
  								<xsl:value-of select="substring-before(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')"/>
  								<xsl:text> </xsl:text>
  								<a href="http://{substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')}">
  									http://<xsl:value-of select="substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')"/>
  								</a>
  							</xsl:when>
  							<xsl:when test="substring(substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https'),1,3) = '://'">
  								<xsl:value-of select="substring-before(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')"/>
  								<xsl:text> </xsl:text>
  								<a href="https://{substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')}">
  									https://<xsl:value-of select="substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')"/>
  								</a>
  							</xsl:when>
  							<xsl:otherwise>
  								<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL"/>
  							</xsl:otherwise>
  						</xsl:choose>
  		 			</p>
  		 		</xsl:if>
  			  	<xsl:if test="gmd:individualName/gco:CharacterString != ''">
  		 			<p>
  		 				<b><xsl:text>Naam contactpersoon: </xsl:text></b>
  		 				<xsl:value-of select="gmd:individualName/gco:CharacterString"/>
  		 			</p>
  		 		</xsl:if>
  			  	<xsl:if test="gmd:positionName/gco:CharacterString != ''">
  		 			<p>
  		 				<b><xsl:text>Rol contactpersoon: </xsl:text></b>
  		 				<xsl:value-of select="gmd:positionName/gco:CharacterString"/>
  		 			</p>
  		 		</xsl:if>
  			  	<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString != ''">
  		 			<p>
  		 				<b><xsl:text>E-mail: </xsl:text></b>
  		 				<a href="mailto:{gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString}">
  		 					<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString"/>
  		 				</a>
  		 			</p>
  		 		</xsl:if>
  			  	<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Adres: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  			  	<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Postcode: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  			  	<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Plaats: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  			  	<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Provincie: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  			  	<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Land: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Telefoonnummer: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString != ''">
  					<p>
  						<b><xsl:text>Faxnummer: </xsl:text></b>
  						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString"/>
  					</p>
  				</xsl:if>
  			</div>
  		</xsl:if>
    </xsl:template>
  	<xsl:template match="gmd:contact/gmd:CI_ResponsibleParty">
  		<xsl:if test=". != ''">
	  		<div class="blok">
		  		<b><p>Auteur bestandsbeschrijving</p></b>
		  		<xsl:if test="gmd:organisationName/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Naam organisatie: </xsl:text></b>
		  				<xsl:value-of select="gmd:organisationName/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
          <xsl:if test="gmd:role/gmd:CI_RoleCode/@codeListValue != ''">
            <p>
              <b><xsl:text>Rol organisatie: </xsl:text></b>
              <xsl:choose>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'resourceProvider'">
                  <xsl:text>verstrekker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'custodian'">
                  <xsl:text>beheerder</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'owner'">
                  <xsl:text>eigenaar</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'user'">
                  <xsl:text>gebruiker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'distributor'">
                  <xsl:text>distributeur</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'originator'">
                  <xsl:text>maker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'pointOfContact'">
                  <xsl:text>contactpunt</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'principalInvestigator'">
                  <xsl:text>inwinner</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'processor'">
                  <xsl:text>bewerker</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'publisher'">
                  <xsl:text>uitgever</xsl:text>
                </xsl:when>
                <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'author'">
                  <xsl:text>auteur</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="gmd:role/gmd:CI_RoleCode/@codeListValue"/>
                </xsl:otherwise>
              </xsl:choose>
            </p>
          </xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL != ''">
		  			<p>
	  					<b><xsl:text>Website: </xsl:text></b>
	  					<xsl:choose>
							<xsl:when test="substring(substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http'),1,3) = '://'">
								<xsl:value-of select="substring-before(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')"/>
								<xsl:text> </xsl:text>
								<a href="http://{substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')}">
									http://<xsl:value-of select="substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')"/>
								</a>
							</xsl:when>
							<xsl:when test="substring(substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https'),1,3) = '://'">
								<xsl:value-of select="substring-before(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')"/>
								<xsl:text> </xsl:text>
								<a href="https://{substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')}">
									https://<xsl:value-of select="substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')"/>
								</a>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL"/>
							</xsl:otherwise>
						</xsl:choose>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:individualName/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Naam contactpersoon: </xsl:text></b>
		  				<xsl:value-of select="gmd:individualName/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:positionName/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Rol contactpersoon: </xsl:text></b>
		  				<xsl:value-of select="gmd:positionName/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>E-mail: </xsl:text></b>
		  				<a href="mailto:{gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString}">
		  					<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString"/>
		  				</a>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Adres: </xsl:text></b>
		  				<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Postcode: </xsl:text></b>
		  				<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Plaats: </xsl:text></b>
		  				<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Provincie: </xsl:text></b>
		  				<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString != ''">
		  			<p>
		  				<b><xsl:text>Land: </xsl:text></b>
		  				<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
		  			</p>
		  		</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Telefoonnummer: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Faxnummer: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString"/>
					</p>
				</xsl:if>
			</div>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty">
		<xsl:if test=". != ''">
			<div class="blok">
				<b><p>Distributeur van het bestand</p></b>
				<xsl:if test="gmd:organisationName/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Naam organisatie: </xsl:text></b>
						<xsl:value-of select="gmd:organisationName/gco:CharacterString"/>
					</p>
				</xsl:if>
        <xsl:if test="gmd:role/gmd:CI_RoleCode/@codeListValue != ''">
          <p>
            <b><xsl:text>Rol organisatie: </xsl:text></b>
            <xsl:choose>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'resourceProvider'">
                <xsl:text>verstrekker</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'custodian'">
                <xsl:text>beheerder</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'owner'">
                <xsl:text>eigenaar</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'user'">
                <xsl:text>gebruiker</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'distributor'">
                <xsl:text>distributeur</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'originator'">
                <xsl:text>maker</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'pointOfContact'">
                <xsl:text>contactpunt</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'principalInvestigator'">
                <xsl:text>inwinner</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'processor'">
                <xsl:text>bewerker</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'publisher'">
                <xsl:text>uitgever</xsl:text>
              </xsl:when>
              <xsl:when test="gmd:role/gmd:CI_RoleCode/@codeListValue = 'author'">
                <xsl:text>auteur</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="gmd:role/gmd:CI_RoleCode/@codeListValue"/>
              </xsl:otherwise>
            </xsl:choose>
          </p>
        </xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL != ''">
					<p>
						<b><xsl:text>Website: </xsl:text></b>
						<xsl:choose>
							<xsl:when test="substring(substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http'),1,3) = '://'">
								<xsl:value-of select="substring-before(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')"/>
								<xsl:text> </xsl:text>
								<a href="http://{substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')}">
									http://<xsl:value-of select="substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'http://')"/>
								</a>
							</xsl:when>
							<xsl:when test="substring(substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https'),1,3) = '://'">
								<xsl:value-of select="substring-before(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')"/>
								<xsl:text> </xsl:text>
								<a href="https://{substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')}">
									https://<xsl:value-of select="substring-after(gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL,'https://')"/>
								</a>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL"/>
							</xsl:otherwise>
						</xsl:choose>
					</p>
				</xsl:if>
				<xsl:if test="gmd:individualName/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Naam contactpersoon: </xsl:text></b>
						<xsl:value-of select="gmd:individualName/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:positionName/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Rol contactpersoon: </xsl:text></b>
						<xsl:value-of select="gmd:positionName/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString != ''">
					<p>
						<b><xsl:text>E-mail: </xsl:text></b>
						<a href="mailto:{gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString}">
		  					<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString"/>
		  				</a>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Adres: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Postcode: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Plaats: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Provincie: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Land: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
					</p>
				</xsl:if>
		  		<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Telefoonnummer: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Faxnummer: </xsl:text></b>
						<xsl:value-of select="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString"/>
					</p>
				</xsl:if>
			</div>
		</xsl:if>
  	</xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicDescription/gmd:geographicIdentifier/gmd:MD_Identifier/gmd:code">
  		<xsl:if test="gco:CharacterString != ''">
	  		<div class="blok">
				<p>
					<b><xsl:text>Beschrijving geografisch gebied: </xsl:text></b>
					<xsl:value-of select="gco:CharacterString"/>
				</p>
			</div>
		</xsl:if>
    <xsl:if test="gmx:Anchor != ''">
      <div class="blok">
      <p>
        <b><xsl:text>Beschrijving geografisch gebied: </xsl:text></b>
        <xsl:value-of select="gmx:Anchor"/>
      </p>
    </div>
    </xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox">
  		<xsl:if test=". != ''">
	  		<div class="blok">
	  			<b><p>Omgrenzende rechthoek in decimale graden</p></b>
	  			<xsl:if test="gmd:westBoundLongitude/gco:Decimal != ''">
					<p>
						<b><xsl:text>Minimum x-coördinaat: </xsl:text></b>
						<xsl:value-of select="gmd:westBoundLongitude/gco:Decimal"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:eastBoundLongitude/gco:Decimal != ''">
					<p>
						<b><xsl:text>Maximum x-coördinaat: </xsl:text></b>
						<xsl:value-of select="gmd:eastBoundLongitude/gco:Decimal"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:southBoundLatitude/gco:Decimal != ''">
					<p>
						<b><xsl:text>Minimum y-coördinaat: </xsl:text></b>
						<xsl:value-of select="gmd:southBoundLatitude/gco:Decimal"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:northBoundLatitude/gco:Decimal != ''">
					<p>
						<b><xsl:text>Maximum y-coördinaat: </xsl:text></b>
						<xsl:value-of select="gmd:northBoundLatitude/gco:Decimal"/>
					</p>
				</xsl:if>
	  		</div>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier">
  		<xsl:if test=". != ''">
	  		<div class="blok">
	  			<xsl:if test="gmd:code/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Code referentiesysteem: </xsl:text></b>
						<xsl:value-of select="gmd:code/gco:CharacterString"/>
					</p>
				</xsl:if>
				<xsl:if test="gmd:codeSpace/gco:CharacterString != ''">
					<p>
						<b><xsl:text>Organisatie referentiesysteem: </xsl:text></b>
						<xsl:value-of select="gmd:codeSpace/gco:CharacterString"/>
					</p>
				</xsl:if>
	  		</div>
  		</xsl:if>
  	</xsl:template>
  <xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent">
    <xsl:if test=". != ''">
      <div class="blok">
        <xsl:if test="gmd:minimumValue/gco:Real != ''">
          <p>
            <b><xsl:text>Minimum z-coördinaat: </xsl:text></b>
            <xsl:value-of select="gmd:minimumValue/gco:Real"/>
          </p>
        </xsl:if>
        <xsl:if test="gmd:maximumValue/gco:Real != ''">
          <p>
            <b><xsl:text>Maximum z-coördinaat: </xsl:text></b>
            <xsl:value-of select="gmd:maximumValue/gco:Real"/>
          </p>
        </xsl:if>
      </div>
    </xsl:if>
  </xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:dateStamp/gco:Date">
  		<xsl:if test=". != ''">
			<div class="blok">
				<p>
					<b><xsl:text>Laatste wijziging bestandsbeschrijving: </xsl:text></b>
		  				<xsl:value-of select="substring(.,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(.,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(.,1,4)"/>
  				</p>
 			</div>
		</xsl:if>
  	</xsl:template>
 	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date">
 		<xsl:if test=". != ''">
	 		<xsl:choose>
	 			<xsl:when test="gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = 'creation'">
	 				<p>
						<b><xsl:text>Voltooiing bestand: </xsl:text></b>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,1,4)"/>
		 			</p>
	 			</xsl:when>
	 			<xsl:when test="gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = 'publication'">
	 				<p>
						<b><xsl:text>Publicatie bestand: </xsl:text></b>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,1,4)"/>
		 			</p>
	 			</xsl:when>
	 			<xsl:when test="gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = 'revision'">
	 				<p>
						<b><xsl:text>Laatste wijziging bestand: </xsl:text></b>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,1,4)"/>
		 			</p>
	 			</xsl:when>
	 			<xsl:otherwise>
	 				<p>
	 					<b><xsl:text>Datum: </xsl:text></b>
	 					<xsl:value-of select="substring(gmd:date/gco:Date,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:date/gco:Date,1,4)"/>
	 				</p>
	 			</xsl:otherwise>
	 		</xsl:choose>
 		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:dateOfNextUpdate/gco:DateTime">
  		<xsl:if test=". != ''">
			<div class="blok">
				<p>
					<b><xsl:text>Volgende herziening bestand: </xsl:text></b>
	  				<xsl:value-of select="substring(.,9,2)"/>
	  				<xsl:text>-</xsl:text>
	  				<xsl:value-of select="substring(.,6,2)"/>
	  				<xsl:text>-</xsl:text>
	  				<xsl:value-of select="substring(.,1,4)"/>
  				</p>
 			</div>
		</xsl:if>
  	</xsl:template>
  <xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:description/gco:CharacterString">
    <xsl:if test=". != ''">
      <p>
        <b><xsl:text>Beschrijving temporele dekking: </xsl:text></b>
        <xsl:value-of select="."/>
      </p>
    </xsl:if>
  </xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod">
		<xsl:if test=". != ''">
			<xsl:variable name="temporal-content">
				<div class="blok">
					<p><b>Temporele dekking</b></p>
					<xsl:if test="gml:begin/gml:TimeInstant/gml:timePosition != ''">
						<p>
							<b><xsl:text>Van datum: </xsl:text></b>
							<xsl:value-of select="substring(gml:begin/gml:TimeInstant/gml:timePosition,9,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:begin/gml:TimeInstant/gml:timePosition,6,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:begin/gml:TimeInstant/gml:timePosition,1,4)"/>
						</p>
					</xsl:if>
					<xsl:if test="gml:beginPosition != ''">
						<p>
							<b><xsl:text>Van datum: </xsl:text></b>
							<xsl:value-of select="substring(gml:beginPosition,9,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:beginPosition,6,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:beginPosition,1,4)"/>
						</p>
					</xsl:if>
					<xsl:if test="gml:end/gml:TimeInstant/gml:timePosition != ''">
						<p>
							<b><xsl:text>Tot datum: </xsl:text></b>
							<xsl:value-of select="substring(gml:end/gml:TimeInstant/gml:timePosition,9,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:end/gml:TimeInstant/gml:timePosition,6,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:end/gml:TimeInstant/gml:timePosition,1,4)"/>
						</p>
					</xsl:if>
					<xsl:if test="gml:endPosition != ''">
						<p>
							<b><xsl:text>Tot datum: </xsl:text></b>
							<xsl:value-of select="substring(gml:endPosition,9,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:endPosition,6,2)"/>
							<xsl:text>-</xsl:text>
							<xsl:value-of select="substring(gml:endPosition,1,4)"/>
						</p>
					</xsl:if>
				</div>
			</xsl:variable>
			<xsl:if test="gml:begin/gml:TimeInstant/gml:timePosition != '' and gml:end/gml:TimeInstant/gml:timePosition != ''">
				<xsl:choose>
					<xsl:when test="gml:begin/gml:TimeInstant/gml:timePosition != gml:end/gml:TimeInstant/gml:timePosition">
						<xsl:copy-of select="$temporal-content"/>
					</xsl:when>
					<xsl:otherwise>
						<p><b>Temporele dekking</b></p>
						<p>
							<b><xsl:text>Datum: </xsl:text></b>
							Niet van toepassing
						</p>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			<xsl:if test="gml:beginPosition != '' and gml:endPosition != ''">
				<xsl:choose>
					<xsl:when test="gml:beginPosition != gml:endPosition">
						<xsl:copy-of select="$temporal-content"/>
					</xsl:when>
					<xsl:otherwise>
						<p><b>Temporele dekking</b></p>
						<p>
							<b><xsl:text>Datum: </xsl:text></b>
							Niet van toepassing
						</p>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/@codeListValue">
		<xsl:if test=". != ''">
			<div class="blok">
	  			<xsl:choose>
		  			<xsl:when test=". = 'continual'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>continu</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'daily'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>Dagelijks</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'weekly'">
		 				<p>
		  					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		  					<xsl:text>Wekelijks</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'fortnightly'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>2-wekelijks</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'monthly'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>Maandelijks</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'quarterly'">
		 				<p>
		  					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		  					<xsl:text>1 x per kwartaal</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'annually'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>Jaarlijks</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'biannually'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>2 x per jaar</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'asNeeded'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>Indien nodig</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'irregular'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>Onregelmatig</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'notPlanned'">
		 				<p>
		  					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		  					<xsl:text>Niet gepland</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:when test=". = 'unknown'">
		 				<p>
		 					<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
		 					<xsl:text>Onbekend</xsl:text>
		 				</p>
		  			</xsl:when>
		  			<xsl:otherwise>
		  				<p>
			  				<b><xsl:text>Herzieningsfrequentie bestand: </xsl:text></b>
			  				<xsl:value-of select="."/>
		  				</p>
		  			</xsl:otherwise>
	  			</xsl:choose>
	  		</div>
	  	</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Alternatieve titel: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<xsl:choose>
		  		<xsl:when test=". = 'completed'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>Compleet</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'historicalArchive'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>Historisch archief</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'obsolete'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>Niet relevant</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'onGoing'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>Continu geactualiseerd</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'planned'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>Gepland</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'required'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>Actualisatie vereist</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'underDevelopment'">
					<p>
		  				<b><xsl:text>Status: </xsl:text></b>
		  				<xsl:text>In ontwikkeling</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:otherwise>
					<p>
						<b><xsl:text>Status: </xsl:text></b>
						<xsl:value-of select="."/>
					</p>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[text() = 'tiff']">
		<xsl:if test="contains(../../gmd:linkage/gmd:URL, '/download/')">
			<xsl:variable name="resource">
				<p>
					<b><xsl:text>Download: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
					<!-- do nothing -->
				</xsl:when>
				<xsl:otherwise>
					<xsl:copy-of select="$resource"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
  <xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[text() = 'tiff']">
    <xsl:if test="contains(../../gmd:linkage/gmd:URL, '/download/')">
      <xsl:variable name="resource">
        <p>
          <b><xsl:text>Download: </xsl:text></b>
          <a href="{../../gmd:linkage/gmd:URL}">
            <xsl:value-of select="../../gmd:linkage/gmd:URL"/>
          </a>
        </p>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
          <!-- do nothing -->
        </xsl:when>
        <xsl:otherwise>
          <xsl:copy-of select="$resource"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
  </xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[text() = 'landingpage']">
		<xsl:if test="contains(../../gmd:linkage/gmd:URL, '/download/')">
			<xsl:variable name="resource">
				<p>
					<b><xsl:text>Download: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
					<!-- do nothing -->
				</xsl:when>
				<xsl:otherwise>
					<xsl:copy-of select="$resource"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		<xsl:if test="contains(../../gmd:linkage/gmd:URL, '/viewer/')">
			<xsl:variable name="resource">
				<p>
					<b><xsl:text>Viewer: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
					<!-- do nothing -->
				</xsl:when>
				<xsl:otherwise>
					<xsl:copy-of select="$resource"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[text() = 'landingpage']">
		<xsl:if test="contains(../../gmd:linkage/gmd:URL, '/download/')">
			<xsl:variable name="resource">
				<p>
					<b><xsl:text>Download: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
					<!-- do nothing -->
				</xsl:when>
				<xsl:otherwise>
					<xsl:copy-of select="$resource"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		<xsl:if test="contains(../../gmd:linkage/gmd:URL, '/viewer/')">
			<xsl:variable name="resource">
				<p>
					<b><xsl:text>Viewer: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
					<!-- do nothing -->
				</xsl:when>
				<xsl:otherwise>
					<xsl:copy-of select="$resource"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL[starts-with(., 'https://www.geoportaaloverijssel.nl/metadata/') or starts-with(., 'https://intern.geoportaaloverijssel.nl/metadata/')]">
		<xsl:variable name="resource">
			<xsl:if test="starts-with(., 'https://www.geoportaaloverijssel.nl/metadata/dataset/') or starts-with(., 'https://intern.geoportaaloverijssel.nl/metadata/dataset/')">
				<p>
					<b><xsl:text>Dataset metadata url: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:if>
			<xsl:if test="starts-with(., 'https://www.geoportaaloverijssel.nl/metadata/service/') or starts-with(., 'https://intern.geoportaaloverijssel.nl/metadata/service/')">
				<p>
					<b><xsl:text>Service metadata url: </xsl:text></b>
					<a href="{../../gmd:linkage/gmd:URL}">
						<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
					</a>
				</p>
			</xsl:if>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
				<!-- do nothing -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="$resource"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[starts-with(text(), 'OGC')]">
		<xsl:variable name="resource">
			<p>
				<b><xsl:value-of select="."/>: </b>
				<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
			</p>

			<xsl:if test=". = 'OGC:WMS'">
				<xsl:variable name="service_name_public" select="substring-before(substring-after(../../gmd:linkage/gmd:URL, 'https://services.geodataoverijssel.nl/geoserver/'), '/wms')"/>
				<xsl:variable name="service_name_secure" select="substring-before(substring-after(../../gmd:linkage/gmd:URL, 'https://secure-services.geodataoverijssel.nl/geoserver/'), '/wms')"/>

				<xsl:if test="$service_name_public != ''">
					<p>
						<b>ArcGIS Rest: </b>
						<a href="https://arcgisrest.geodataoverijssel.nl/arcgis/rest/services/{$service_name_public}/FeatureServer">
							https://arcgisrest.geodataoverijssel.nl/arcgis/rest/services/<xsl:value-of select="$service_name_public"/>/FeatureServer
						</a>
					</p>
				</xsl:if>

				<xsl:if test="$service_name_secure != ''">
					<p>
						<b>ArcGIS Rest: </b>
						<a href="https://secure-arcgisrest.geodataoverijssel.nl/arcgis/rest/services/{$service_name_secure}/FeatureServer">
							https://secure-arcgisrest.geodataoverijssel.nl/arcgis/rest/services/<xsl:value-of select="$service_name_secure"/>/FeatureServer
						</a>
					</p>
				</xsl:if>
			</xsl:if>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
				<!-- do nothing -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="$resource"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[starts-with(text(), 'OGC')]">
		<xsl:variable name="resource">
			<p>
				<b><xsl:value-of select="."/>: </b>
				<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
			</p>

			<xsl:if test=". = 'OGC:WMS'">
				<xsl:variable name="service_name_public" select="substring-before(substring-after(../../gmd:linkage/gmd:URL, 'https://services.geodataoverijssel.nl/geoserver/'), '/wms')"/>
				<xsl:variable name="service_name_secure" select="substring-before(substring-after(../../gmd:linkage/gmd:URL, 'https://secure-services.geodataoverijssel.nl/geoserver/'), '/wms')"/>

				<xsl:if test="$service_name_public != ''">
					<p>
						<b>ArcGIS Rest: </b>
						<a href="https://arcgisrest.geodataoverijssel.nl/arcgis/rest/services/{$service_name_public}/FeatureServer">
							https://arcgisrest.geodataoverijssel.nl/arcgis/rest/services/<xsl:value-of select="$service_name_public"/>/FeatureServer
						</a>
					</p>
				</xsl:if>

				<xsl:if test="$service_name_secure != ''">
					<p>
						<b>ArcGIS Rest: </b>
						<a href="https://secure-arcgisrest.geodataoverijssel.nl/arcgis/rest/services/{$service_name_secure}/FeatureServer">
							https://secure-arcgisrest.geodataoverijssel.nl/arcgis/rest/services/<xsl:value-of select="$service_name_secure"/>/FeatureServer
						</a>
					</p>
				</xsl:if>
			</xsl:if>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
        <!-- do nothing -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="$resource"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString[text() != 'tiff' and text() != 'landingpage' and not(starts-with(text(), 'OGC')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://www.geoportaaloverijssel.nl/metadata/')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://intern.geoportaaloverijssel.nl/metadata/'))]">
		<xsl:variable name="resource">
			<p>
				<b><xsl:value-of select="."/>: </b>
				<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
			</p>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
				<!-- do nothing -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="$resource"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx:Anchor[text() != 'tiff' and text() != 'landingpage' and not(starts-with(text(), 'OGC')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://www.geoportaaloverijssel.nl/metadata/')) and not(starts-with(../../gmd:linkage/gmd:URL, 'https://intern.geoportaaloverijssel.nl/metadata/'))]">
		<xsl:variable name="resource">
			<p>
				<b><xsl:value-of select="."/>: </b>
				<xsl:value-of select="../../gmd:linkage/gmd:URL"/>
			</p>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test = "not(count(../../../../../../../../gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation[gco:CharacterString = 'Downloadable data']) > 0) and (. = 'download' or . = 'OGC:WFS')">
				<!-- do nothing -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:copy-of select="$resource"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:edition/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Versie: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code">
  		<xsl:if test="gco:CharacterString != ''">
	  		<p>
		  		<b><xsl:text>Unieke identifier: </xsl:text></b>
		  		<xsl:value-of select="gco:CharacterString"/>
		  	</p>
	  	</xsl:if>
      <xsl:if test="gmx:Anchor != ''">
	  		<p>
		  		<b><xsl:text>Unieke identifier: </xsl:text></b>
		  		<xsl:value-of select="gmx:Anchor"/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation/gmd:aggregateDataSetName/gmd:CI_Citation">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Gerelateerde dataset: </xsl:text></b>
		  		<xsl:value-of select="gmd:title/gco:CharacterString/."/>,
		  		<xsl:value-of select="substring(gmd:date/gmd:CI_Date/gmd:date/gco:Date/.,9,2)"/>
  				<xsl:text>-</xsl:text>
  				<xsl:value-of select="substring(gmd:date/gmd:CI_Date/gmd:date/gco:Date/.,6,2)"/>
  				<xsl:text>-</xsl:text>
  				<xsl:value-of select="substring(gmd:date/gmd:CI_Date/gmd:date/gco:Date/.,1,4)"/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode">
 		<xsl:if test=". != ''">
	 		<xsl:choose>
		 		<xsl:when test=". = 'farming'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Landbouw en veeteelt</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'biota'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Biota</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'boundaries'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Grenzen</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'climatologyMeteorologyAtmosphere'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Klimatologie, meteorologie atmosfeer</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'economy'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Economie</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'elevation'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Hoogte</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'environment'">
					<p>
						<b>Onderwerp: </b>
						<xsl:text>Natuur en milieu</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'geoscientificInformation'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Geowetenschappelijke data</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'health'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Gezondheid</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'imageryBaseMapsEarthCover'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Referentie materiaal aardbedekking</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'intelligenceMilitary'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Militair</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'inlandWaters'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Binnenwater</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'location'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Locatie</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'oceans'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Oceanen</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'planningCadastre'">
					<p>
						<b>Onderwerp: </b>
						<xsl:text>Ruimtelijke ordening en kadaster</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'society'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Maatschappij</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'structure'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>(Civiele) structuren</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'transportation'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Transport</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:when test=". = 'utilitiesCommunication'">
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:text>Nutsbedrijven communicatie</xsl:text>
		  			</p>
				</xsl:when>
				<xsl:otherwise>
					<p>
		  				<b>Onderwerp: </b>
		  				<xsl:value-of select="."/>
		  			</p>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords">
    <div class="blok">
      <xsl:if test="gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString != ''">
  	  	<p>
  	  		<b><xsl:text>Thesaurus trefwoorden: </xsl:text></b>
  	  		<xsl:value-of select="gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString"/>
  	  	</p>
    	</xsl:if>
  	  <xsl:if test="gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date != ''">
  	  	<p>
  	  		<xsl:choose>
  	  			<xsl:when test="gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = 'creation'">
  	  				<b><xsl:text>Creatie datum thesaurus: </xsl:text></b>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,9,2)"/>
  	  				<xsl:text>-</xsl:text>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,6,2)"/>
  	  				<xsl:text>-</xsl:text>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,1,4)"/>
  	  			</xsl:when>
  	  			<xsl:when test="gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = 'publication'">
  	  				<b><xsl:text>Publicatie datum thesaurus: </xsl:text></b>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,9,2)"/>
  	  				<xsl:text>-</xsl:text>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,6,2)"/>
  	  				<xsl:text>-</xsl:text>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,1,4)"/>
  	  			</xsl:when>
  	  			<xsl:when test="gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = 'revision'">
  	  				<b><xsl:text>Revisie datum thesaurus: </xsl:text></b>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,9,2)"/>
  	  				<xsl:text>-</xsl:text>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,6,2)"/>
  	  				<xsl:text>-</xsl:text>
  	  				<xsl:value-of select="substring(gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date,1,4)"/>
  	  			</xsl:when>
  	  		</xsl:choose>
  	  	</p>
  	  </xsl:if>
      <xsl:if test="gmd:keyword/gco:CharacterString != ''">
        <xsl:for-each select="gmd:keyword/gco:CharacterString">
          <p>
      			<b><xsl:text>Trefwoord: </xsl:text></b>
    	  		<xsl:value-of select="."/>
      		</p>
        </xsl:for-each>
    	</xsl:if>
    </div>
	</xsl:template>
	<xsl:template match="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode/@codeListValue">
 		<xsl:if test=". != ''">
	  		<xsl:choose>
	  			<xsl:when test=". = 'copyright'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Copyright</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'patent'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Patent</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'patentPending'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Patent in wording</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'trademark'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Merknaam</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'license'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Licentie</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'intellectualPropertyRights'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Intellectueel eigendom</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'restricted'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Niet toegankelijk</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'otherRestrictions'">
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:text>Overige beperkingen</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:otherwise>
	  				<p>
				  		<b><xsl:text>(Juridische) gebruiksrestricties: </xsl:text></b>
				  		<xsl:value-of select="."/>
			  		</p>
	  			</xsl:otherwise>
	  		</xsl:choose>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/@codeListValue">
 		<xsl:if test=". != ''">
	  		<xsl:choose>
	  			<xsl:when test=". = 'copyright'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Copyright</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'patent'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Patent</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'patentPending'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Patent in wording</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'trademark'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Merknaam</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'license'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Licentie</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'intellectualPropertyRights'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Intellectueel eigendom</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'restricted'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Niet toegankelijk</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'otherRestrictions'">
	  				<p>
				  		<b><xsl:text>(Juridische) toegangsrestricties: </xsl:text></b>
				  		<xsl:text>Overige beperkingen</xsl:text>
			  		</p>
	  			</xsl:when>
	  			<xsl:otherwise>
	  				<p>
				  		<b>(Juridische) toegangsrestricties: </b>
				  		<xsl:value-of select="."/>
			  		</p>
	  			</xsl:otherwise>
	  		</xsl:choose>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints">
 		<xsl:if test="gco:CharacterString != ''">
  			<p>
		  		<b><xsl:text>Overige beperkingen: </xsl:text></b>
		  		<xsl:choose>
					<xsl:when test="substring(substring-after(gco:CharacterString,'http'),1,3) = '://'">
						<xsl:value-of select="substring-before(gco:CharacterString,'http://')"/>
						<xsl:text> </xsl:text>
						<a href="http://{substring-after(gco:CharacterString,'http://')}">
							http://<xsl:value-of select="substring-after(gco:CharacterString,'http://')"/>
						</a>
					</xsl:when>
					<xsl:when test="substring(substring-after(gco:CharacterString,'https'),1,3) = '://'">
						<xsl:value-of select="substring-before(gco:CharacterString,'https://')"/>
						<xsl:text> </xsl:text>
						<a href="https://{substring-after(gco:CharacterString,'https://')}">
							https://<xsl:value-of select="substring-after(gco:CharacterString,'https://')"/>
						</a>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="gco:CharacterString"/>
					</xsl:otherwise>
				</xsl:choose>
	  		</p>
  		</xsl:if>
      <xsl:if test="gmx:Anchor != ''">
    			<p>
  		  		<b><xsl:text>Overige beperkingen: </xsl:text></b>
            <xsl:value-of select="gmx:Anchor"/>
            <xsl:text> | </xsl:text>
            <a href="gmx:Anchor/@xlink:href">
              <xsl:value-of select="gmx:Anchor/@xlink:href"/>
            </a>
  	  		</p>
    		</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString">
		<xsl:if test=". != ''">
			<p>
		  		<b>Metadata unieke identifier: </b>
		  		<xsl:value-of select="."/>
	  		</p>
		</xsl:if>
	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:language/gmd:LanguageCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<xsl:choose>
		  		<xsl:when test=". = 'dut'">
					<p>
						<b><xsl:text>Metadata taal: </xsl:text></b>
						<xsl:text>Nederlands</xsl:text>
					</p>
				</xsl:when>
				<xsl:otherwise>
					<p>
						<b><xsl:text>Metadata taal: </xsl:text></b>
						<xsl:value-of select="."/>
					</p>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Metadata karakterset: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<xsl:choose>
		  		<xsl:when test=". = 'dataset'">
					<p>
						<b><xsl:text>Metadata hiërarchieniveau: </xsl:text></b>
						<xsl:text>Dataset</xsl:text>
					</p>
				</xsl:when>
				<xsl:when test=". = 'series'">
					<p>
						<b><xsl:text>Metadata hiërarchieniveau: </xsl:text></b>
						<xsl:text>Series</xsl:text>
					</p>
				</xsl:when>
				<xsl:when test=". = 'featureType'">
					<p>
						<b><xsl:text>Metadata hiërarchieniveau: </xsl:text></b>
						<xsl:text>Feature type</xsl:text>
					</p>
				</xsl:when>
				<xsl:otherwise>
					<p>
						<b><xsl:text>Metadata hiërarchieniveau: </xsl:text></b>
						<xsl:value-of select="."/>
					</p>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:metadataStandardName/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Metadata standaard naam: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:metadataStandardVersion/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Metadata standaard versie: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<xsl:choose>
	  			<xsl:when test=". = 'dut'">
	  				<p>
		  				<b><xsl:text>Taal van de bron: </xsl:text></b>
		  				<xsl:text>Nederlands</xsl:text>
		  			</p>
	  			</xsl:when>
	  			<xsl:otherwise>
					<p>
						<b><xsl:text>Taal van de bron: </xsl:text></b>
						<xsl:value-of select="."/>
					</p>
				</xsl:otherwise>
	  		</xsl:choose>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Karakterset van de bron: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:fees/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
	  			<b><xsl:text>Prijsinformatie: </xsl:text></b>
		  		<xsl:value-of select="."/>
	  		</p>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:orderingInstructions/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
	  			<b><xsl:text>Orderprocedure: </xsl:text></b>
		  		<xsl:value-of select="."/>
	  		</p>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:turnaround/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
	  			<b><xsl:text>Doorlooptijd orderprocedure: </xsl:text></b>
		  		<xsl:value-of select="."/>
	  		</p>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
	  			<b><xsl:text>Leverings-/gebruikseenheid: </xsl:text></b>
		  		<xsl:value-of select="."/>
	  		</p>
  		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:offLine/gmd:MD_Medium/gmd:name/gmd:MD_MediumNameCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<p>
	  			<b><xsl:text>Naam medium: </xsl:text></b>
		  		<xsl:value-of select="."/>
	  		</p>
  		</xsl:if>
  	</xsl:template>

  	<xsl:template match="gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Algemene beschrijving herkomst: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:specificUsage/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Potentieel gebruik: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_CompletenessOmission/gmd:result/gmd:DQ_QuantitativeResult/gmd:value/gco:Record">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Volledigheid: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
		</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_AbsoluteExternalPositionalAccuracy/gmd:result/gmd:DQ_QuantitativeResult/gmd:value/gco:Record">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Geometrische nauwkeurigheid: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode/@codeListValue">
  		<xsl:if test=". != ''">
	  		<xsl:choose>
	  			<xsl:when test=". = 'dataset'">
	  				<p>
		  				<b><xsl:text>Niveau kwaliteitbeschrijving: </xsl:text></b>
		  				<xsl:text>Dataset</xsl:text>
		  			</p>
	  			</xsl:when>
	  			<xsl:when test=". = 'series'">
					<p>
						<b><xsl:text>Niveau kwaliteitbeschrijving: </xsl:text></b>
						<xsl:text>Series</xsl:text>
					</p>
				</xsl:when>
				<xsl:when test=". = 'featureType'">
					<p>
						<b><xsl:text>Niveau kwaliteitbeschrijving: </xsl:text></b>
						<xsl:text>Feature type</xsl:text>
					</p>
				</xsl:when>
	  			<xsl:otherwise>
					<p>
						<b><xsl:text>Niveau kwaliteitbeschrijving: </xsl:text></b>
						<xsl:value-of select="."/>
					</p>
				</xsl:otherwise>
	  		</xsl:choose>
	  	</xsl:if>
  	</xsl:template>
    <xsl:template match="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:series/gmd:CI_Series/gmd:name/gco:CharacterString">
  		<xsl:if test=". != ''">
	  		<p>
		  		<b><xsl:text>Serienaam/-nummer: </xsl:text></b>
		  		<xsl:value-of select="."/>
		  	</p>
	  	</xsl:if>
  	</xsl:template>
  	<xsl:template match="gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep">
  		<xsl:if test="gmd:description/gco:CharacterString != ''">
	  		<div class="blok">
		  		<b><p>Uitgevoerde bewerkingen</p></b>
		  		<p class="inspringen">
		  			<b><xsl:text>Beschrijving: </xsl:text></b>
		  			<xsl:value-of select="gmd:description/gco:CharacterString"/>
		  		</p>
          <xsl:if test="gmd:dateTime/gco:DateTime != ''">
            <p class="inspringen">
  		  			<b><xsl:text>Datum: </xsl:text></b>
  		  			<xsl:value-of select="substring(gmd:dateTime/gco:DateTime,9,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:dateTime/gco:DateTime,6,2)"/>
		  				<xsl:text>-</xsl:text>
		  				<xsl:value-of select="substring(gmd:dateTime/gco:DateTime,1,4)"/>
  		  		</p>
          </xsl:if>
		  	</div>
	  	</xsl:if>
  	</xsl:template>
    <xsl:template match="gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:source/gmd:LI_Source/gmd:description/gco:CharacterString">
      <xsl:if test=". != ''">
        <p>
          <b><xsl:text>Beschrijving brondata: </xsl:text></b>
          <xsl:value-of select="."/>
        </p>
      </xsl:if>
    </xsl:template>
</xsl:stylesheet>
