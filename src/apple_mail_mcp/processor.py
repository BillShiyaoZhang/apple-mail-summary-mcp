from bs4 import BeautifulSoup
import re
from typing import List, Dict

class PaperProcessor:
    def __init__(self):
        pass

    def extract_links(self, html_content: str) -> List[Dict[str, str]]:
        """
        Extracts paper links from Google Scholar Alert HTML.
        Returns a list of dicts with 'title' and 'url'.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        papers = []
        
        # Heuristic: Google Scholar alerts usually have <h3> for titles
        # or specific anchor tags. 
        # We will look for <a> tags that look like paper links.
        
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link['href']
            title = link.get_text(strip=True)
            
            # Simple filters for academic domains or PDF links
            if self._is_academic_link(href) and len(title) > 10:
                # Avoid "PDF" or "HTML" labels being the title
                if title.lower() in ['pdf', 'html', 'full view', 'view as html']:
                    continue
                    
                papers.append({
                    "title": title,
                    "url": href
                })
                
        # Deduplicate by URL
        unique_papers = {p['url']: p for p in papers}.values()
        return list(unique_papers)

    def _is_academic_link(self, url: str) -> bool:
        keywords = [
            'arxiv.org', 'nature.com', 'science.org', 'ieee.org', 
            'acm.org', 'springer.com', 'sciencedirect.com', 
            'biorxiv.org', 'medrxiv.org', 'scholar.google.com'
        ]
        return any(k in url for k in keywords)
