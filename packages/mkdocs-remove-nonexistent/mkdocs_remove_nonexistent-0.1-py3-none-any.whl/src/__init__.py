from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation, Section

class RemoveNonExistentPagesPlugin(BasePlugin):

    def on_nav(self, nav: Navigation, config, files):
        new_nav = []
        docs_dir = self.config.get('docs_dir', 'docs')  # Default to 'docs' if not specified
        for item in nav.items:
            if isinstance(item, Section):  # Check if the item is a section (dict)
                section_items = item.children
                new_children = []
                for child_item in section_items:
                    if self.section_or_page_exists(child_item, files):
                        new_children.append(child_item)
                if new_children:
                    item.children = new_children
                    new_nav.append(item)
            else:  # If the item is not a section, assume it's a single page entry
                page_path = item.url
                if self.page_exists(page_path, files):
                    new_nav.append(item)

        nav.items = new_nav
        return nav

    def section_or_page_exists(self, item, files):
        if isinstance(item, Section):  # Check if the item is a section
            new_children = []
            for child_item in item.children:
                if self.section_or_page_exists(child_item, files):
                    new_children.append(child_item)
            item.children = new_children
            return bool(new_children)  # Return True if any child exists
        elif getattr(item, "url"):  # Check if the item is a page
            page_path = item.url
            return self.page_exists(page_path, files)
        return False

    def page_exists(self, page_path, files):
        # Check if the page exists in the files list
        page_path = page_path.removesuffix("/")
        for file in files:
            path = file.abs_src_path.split(".")
            path = '.'.join(path[:-1])
            if path.endswith(page_path):
                print("found", page_path)
                return True
        return False

