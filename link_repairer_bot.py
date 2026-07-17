#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hindi Wikipedia Link Repairer Bot
This bot scans external references in articles, identifies dead links (404/500/etc.),
queries the Wayback Machine, and automatically replaces broken links with archived versions.
"""

import pywikibot
from pywikibot import pagegenerators
import urllib.request
import json

# --- CONFIGURATION SETTINGS ---
DRY_RUN = True  # Set to False to write actual edits to Wikipedia
# ------------------------------

class LinkRepairerBot:
    def __init__(self):
        """Initializes connection to Hindi Wikipedia."""
        self.site = pywikibot.Site('hi', 'wikipedia')
        self.site.login()

    def is_link_dead(self, url):
        """Verifies if an HTTP link is active or returns an error (404/500/Timeout)."""
        try:
            # Send request with a standard browser User-Agent to avoid blocks
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                return response.status in [404, 410, 500, 502, 503, 504]
        except Exception:
            # If connection fails or times out, treat it as dead/unreachable
            return True

    def get_wayback_archive(self, url):
        """Queries the Internet Archive API to find a preserved snapshot of the URL."""
        archive_api = f"https://archive.org/wayback/available?url={url}"
        try:
            req = urllib.request.Request(
                archive_api, 
                headers={'User-Agent': 'AalekhakBotLinkRepairer/1.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                snapshots = data.get("archived_snapshots", {})
                if "closest" in snapshots and snapshots["closest"]["available"]:
                    archive_url = snapshots["closest"]["url"]
                    timestamp = snapshots["closest"]["timestamp"]
                    # Format timestamp from YYYYMMDDhhmmss to YYYY-MM-DD
                    formatted_date = f"{timestamp[0:4]}-{timestamp[4:6]}-{timestamp[6:8]}"
                    return archive_url, formatted_date
        except Exception as error:
            pywikibot.error(f"Archive.org query failed for {url}: {error}")
        return None, None

    def repair_links_in_text(self, text):
        """Scans and replaces dead links in the page markup text."""
        import re
        # Find external links enclosed in brackets e.g., [http://example.com Page Title]
        # or plain HTTP URLs
        urls = re.findall(r'https?://[^\s\]|<>"]+', text)
        updated_text = text
        changes_made = 0

        for url in set(urls):
            # Clean up trailing characters commonly found in wiki markup
            clean_url = url.strip().rstrip('}')
            
            # Skip checking Wikipedia internal links and Archive.org links themselves
            if "wikipedia.org" in clean_url or "archive.org" in clean_url:
                continue

            pywikibot.output(f"🌐 Verifying URL status: {clean_url}")
            if self.is_link_dead(clean_url):
                pywikibot.output(f"   ⚠️ Link is dead. Searching Wayback Machine...")
                archive_url, archive_date = self.get_wayback_archive(clean_url)
                
                if archive_url:
                    pywikibot.output(f"   ✅ Snapshot found: {archive_url}")
                    # Replace the dead link with archive format in Hindi Wikipedia syntax
                    # We inject archive parameters or replace the plain URL
                    new_ref_format = f"{clean_url} | आर्काइव-यूआरएल = {archive_url} | आर्काइव-तिथि = {archive_date}"
                    updated_text = updated_text.replace(clean_url, new_ref_format)
                    changes_made += 1
                else:
                    pywikibot.output(f"   ❌ No snapshot available on Archive.org")
                    
        return updated_text, changes_made

    def run(self, category_name):
        """Starts scanning articles in the specified Category."""
        category = pywikibot.Category(self.site, category_name)
        generator = pagegenerators.CategorizedPageGenerator(category, recurse=False, total=50)

        for page in generator:
            if page.isRedirectPage():
                continue

            try:
                pywikibot.output(f"\n📂 Checking Article: [[{page.title()}]]")
                original_text = page.text
                new_text, modifications = self.repair_links_in_text(original_text)

                if modifications > 0:
                    if DRY_RUN:
                        pywikibot.output(f"--- [DRY RUN]: {modifications} dead link(s) found and repaired. No save executed. ---")
                    else:
                        page.text = new_text
                        page.save(
                            summary=f"बॉट: {modifications} मृत कड़ियों (dead links) को आर्काइव कड़ियों से बदला गया",
                            minor=True,
                            botflag=True
                        )
                        pywikibot.output(f"   💾 Saved updates successfully on [[{page.title()}]]!")
                else:
                    pywikibot.output("   ✨ No broken links detected.")

            except Exception as e:
                pywikibot.error(f"Error handling [[{page.title()}]]: {e}")

def main():
    bot = LinkRepairerBot()
    # Test on a specific category of interest, e.g., articles with broken references
    # You can change this to any Hindi Category containing general articles
    target_category = "श्रेणी:हल्के लेख"  
    bot.run(target_category)

if __name__ == "__main__":
    main()
