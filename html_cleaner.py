from bs4 import BeautifulSoup

class HTMLCleaner():
    def remove_extra_attributes(self, element):
        allowed_attributes = ['special-id', 'value', 'type', 'id']
        attributes_to_remove = [attr for attr in element.attrs if attr not in allowed_attributes]
        for attr in attributes_to_remove:
            del element[attr]
        
    def clean_html(self, HTML):
        soup = BeautifulSoup(HTML, 'html.parser')

        for elem in soup(["script", "noscript", "svg", "style", "img"]):
            elem.decompose()

        for tag in soup.find_all(True):
            if len(tag.get_text(strip=True)) == 0 and tag.name not in ['input', 'button']:
                tag.extract()
            self.remove_extra_attributes(tag)


        return str(soup)