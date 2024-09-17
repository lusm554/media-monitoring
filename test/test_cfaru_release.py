import sys; sys.path.insert(0, '.')
import scraper_lib as scraper

releases = scraper.CfaReleasesScraper().fetch_and_parse(scraper.Periods.LAST_WEEK, add_pdf_text=True)
print(len(releases))
for r in releases:
  if r.pdf_text:
    print(len(r.pdf_text))
    if len(r.pdf_text) < 100:
      print(r.pdf_text)
  else:
    print(None)



