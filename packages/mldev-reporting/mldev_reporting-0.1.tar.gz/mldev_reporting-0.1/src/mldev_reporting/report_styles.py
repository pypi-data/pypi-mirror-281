import os
import shutil
import subprocess
import math

from datetime import datetime
from jinja2 import Template
from bs4 import BeautifulSoup

class ReportStyles:
    def __init__(self, res_dir, theme, lang):
        self.__corrent_dir = os.path.dirname(os.path.abspath(__file__))
        self.__res_dir = res_dir
        self.__theme = theme
        self.__lang = lang

      
    def copy_assets(self):
        assets_main = os.path.join(self.__corrent_dir, "assets/styles.min.css")
        assets_core = os.path.join(self.__corrent_dir, "assets/core.min.css")
        assets_theme = os.path.join(self.__corrent_dir, f"assets/{self.__theme}.min.css")
        shutil.copy(assets_main, self.__res_dir)
        shutil.copy(assets_core, self.__res_dir)
        shutil.copy(assets_theme, self.__res_dir)


    def get_data_from_subprocess(self, comand):
        res = subprocess.run(comand, stdout=subprocess.PIPE)       
        data = res.stdout.strip().decode()

        return data


    def render_from_html_template(self, url, repo):
        with open(os.path.join(self.__corrent_dir, url), 'r') as template:
            template_text = Template(template.read(), trim_blocks=True)

        res = template_text.render(repo)
        return res

    
    def render_link(self, link):
        return self.render_from_html_template("assets/link.html", { "link": f"#{link}", "text": link })

      
    def render_header(self):
        git_commit = self.get_data_from_subprocess(["git", "rev-parse", "HEAD"])
        return self.render_from_html_template("assets/header.html", {"git_commit": f"#{git_commit}"})


    def render_footer(self):
        footer_repo = {}
        footer_repo["git_username"] = self.get_data_from_subprocess(["git", "config", "user.name"])
        footer_repo["git_email"] = self.get_data_from_subprocess(["git", "config", "user.email"])
        footer_repo["data"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        return self.render_from_html_template(f"assets/footer.{self.__lang}.html", footer_repo)


    def render_nav(self, html):
        soup=BeautifulSoup(html,'html.parser')
        items=soup.select('div.section')
        rendered_links = []

        for link in items:
           rendered_links.append(self.render_link(link.get("id")))

        return self.render_from_html_template("assets/nav.html", { "links": '\n'.join(rendered_links)})


    def get_page_title(self, html):
        soup=BeautifulSoup(html,'html.parser')
        title=soup.select('h1.title')[0]

        return title.contents[0]


    def split_cards(self, html):
        soup=BeautifulSoup(html,'html.parser')
        items=soup.select('div.section') 

        divider =  math.ceil(len(items) / 2)
        
        res = {
            "col1": "\n".join(map(lambda x : str(x),items[0:divider])),
            "col2": "\n".join(map(lambda x : str(x),items[divider:])),
        }

        for item in items:
            item.clear()
        
        res["main"] = soup

        return res



    def render_result(self, html):
      repo = {
          "main": html, 
          "theme": self.__theme 
      }
      repo["header"] = self.render_header()
      repo["footer"] = self.render_footer()
      repo["nav"] = self.render_nav(html)
      repo["title"] = self.get_page_title(html)
      repo["columns"] = self.split_cards(html)

      res_html_file = "assets/res.cards.html" if self.__theme == "cards" else "assets/res.html"

      with open(os.path.join(self.__corrent_dir, res_html_file), 'r') as res_template:
          res_text = Template(res_template.read(), trim_blocks=True)

      res = res_text.render(repo)
      return res

