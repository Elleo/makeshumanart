toml_template = """
baseURL = "https://%s.%s/"
languageCode = "en-us"
title = "%s"
theme = "%s"
sectionPagesMenu = "main"
"""

page_template = """+++
title = "%s"
menus = "main"
draft = false
+++\n"""
