import os, codecs

class PageGenerator:
	def __init__(self, inputdir, outputdir):
		self._inputdir = inputdir
		self._outputdir = outputdir

		self.FixedHeader = [
'''<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="http://2018.igem.org/Template:Rotterdam_HR/css/main?action=raw&ctype=text/css">
	<style>
''',
'''
	</style>
</head>
<body>
''',
'''
<div id="navbar" style="position: -webkit-sticky;position: sticky;top: -2px; width: 100%; z-index: 100; margin-bottom: 100px;"></div>
'''
		]

		self.FixedFooter = '''
<div id="footer"></div>
<script src="http://2018.igem.org/Template:Rotterdam_HR/js/main?action=raw&ctype=text/javascript"></script>
</body>
</html>
'''

	def GeneratePages(self):
		for page in self.GetPages():
			header  = self.generateHeader(page)
			content = self.GetPageContent(page)
			footer  = self.FixedFooter

			if page.Name == 'Index':
				page.Name = page.Name.lower() # the home page must be index with lower cases

			with codecs.open(self._outputdir + page.Name + '.html', 'w') as f:
				print('Writing page: {0}'.format(page.Name))
				f.write(header + content + footer)

	def GetPages(self):
		pageList = list()

		for pageUrl in os.listdir(self._inputdir):
			# Check if the page has content
			if os.stat(self._inputdir + pageUrl).st_size == 0: pageHasContent = False
			else: pageHasContent = True

			# Get the name and category for the page from the filename
			page = pageUrl[:-5].split('-')
			pageName = page[1]
			pageCategory = page[0]
			pageList.append(Page(pageUrl, pageName, pageCategory, pageHasContent))
		# returns a list of Page objects containing page information
		return pageList
	
	def generateHeader(self, page):
		# First header part (pre-generated)
		header = self.FixedHeader[0]
		# Second header part (css for the navigation menu)
		header = header + '''
		.menu #{0}, .menu #{1} {{
			color: goldenrod;
		}}
		'''.format(page.Name.lower(), page.Category.lower() + '-category')
		# Third header part (css for the under construction pages)
		if not page.HasContent:
			header = header + '''
			.under-construction {
				margin: 30px auto;
				width: 100%;
				display: flex;
				flex-direction: column;
				align-items: center;
			}
			'''
		
		# Fourth header part (pre-generated)
		header = header + self.FixedHeader[1] + self.GenerateBanner(page) + self.FixedHeader[2]

		return header
	
	def GenerateBanner(self, page):
		# Dedicated banner backgrounds for specific pages 
		pageBanners = {
			'index'          : "http://2018.igem.org/wiki/images/e/ef/T--Rotterdam_HR--team-heads.jpg",
			'team'           : "http://2018.igem.org/wiki/images/e/ef/T--Rotterdam_HR--team-heads.jpg",
			'human_practices': "http://2018.igem.org/wiki/images/3/3a/T--Rotterdam_HR--Human_practices-banner.jpeg",
			'software'       : "http://2018.igem.org/wiki/images/c/cc/T--Rotterdam_HR--Software-banner.jpeg",
			'safety'         : "http://2018.igem.org/wiki/images/c/c9/T--Rotterdam_HR--Safety-banner.jpeg",
			'notebook'       : "http://2018.igem.org/wiki/images/3/3e/T--Rotterdam_HR--Notebook-banner.jpeg",
			'experiments'    : "http://2018.igem.org/wiki/images/a/a3/T--Rotterdam_HR--Experiments-banner.jpeg",
			'hardware'       : "http://2018.igem.org/wiki/images/1/11/T--Rotterdam_HR--Hardware-banner.jpeg"
		}

		# Get the dedicated banner. If it cannot find any, set it to the default homepage banner.
		banner = pageBanners.get(page.Name.lower())
		if banner == None: banner = pageBanners.get('index')

		return '''
<style>
	.header::before {{
		background: black url({0}) no-repeat left;
  	background-size: 100%;
	}}
</style>

<div class="header">
  <div>
		<div id="icon"></div>
		<script> $('#icon').load("{2}?action=raw&ctype=text/html"); </script>
    <h1 style="background: none;">{1}</h1>
  </div>
</div>
'''.format(banner, 'Home' if page.Name.replace('_', ' ').title() == 'Index' else page.Name.replace('_', ' ').title(), page.Icon)
	
	def GetPageContent(self, page):
		if page.HasContent:
			return open(self._inputdir + page.Url).read()
		else:
				return '''
	<div class="under-construction">
	<h1>{0}</h1>
	<p>This page has no content yet.</p>
	</div>
				'''.format(page.Name)


# Object for storing page information
class Page:
	def __init__(self, url, name, category, hasContent):
		self.Url = url
		self.Name = name.title()
		self.Category = category
		self.HasContent = hasContent
		self.Icon = "http://2018.igem.org/Template:Rotterdam_HR/icon/{0}".format(self.Name.lower())