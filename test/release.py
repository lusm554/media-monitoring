import sys; sys.path.insert(0, '.')
import scraper_lib as scraper

releases = scraper.CfaReleasesScraper().fetch_and_parse(scraper.Periods.LAST_WEEK)
print(releases)
