TRUSTED_DOMAINS = ",".join([
    "reuters.com",
    "apnews.com",
    "bloomberg.com",
    "ft.com",
    "wsj.com",
    "economist.com",
    "cnbc.com",
    "fortune.com",
    "forbes.com",
    "businessinsider.com",
    "nytimes.com",
    "theguardian.com",
    "washingtonpost.com",
    "bbc.co.uk",
    "theatlantic.com",
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "arstechnica.com",
    "venturebeat.com",
    "thenextweb.com",
    "technologyreview.com",
    "infoworld.com",
    "computerworld.com",
    "sdtimes.com",
    "infoq.com",
    "stackoverflow.blog",
    "github.blog",
])

SIGNAL_TOPICS = {

    "workforce_reduction": {
        "description": "Concrete layoff and headcount cut events in engineering orgs",
        "match_units": [
            '"engineering layoffs"',
            '"developer layoffs"',
            '"engineering headcount"',
            '"software engineering" AND "layoffs"',
            '"software engineer" AND "job cuts"',
            '"developers" AND "laid off"',
            '"engineering team" AND "headcount reduction"',
            '"engineering team" AND "workforce reduction"',
            '"developer workforce" AND "reduction"',
            '"software" AND "reduction in force"',
        ],
    },

    "ai_displacement": {
        "description": "AI framed as directly replacing or removing need for engineers",
        "match_units": [
            '"replace software engineers"',
            '"replace developers"',
            '"replacing programmers"',
            '"AI replaces coders"',
            '"AI" AND "fewer engineers"',
            '"AI" AND "fewer developers"',
            '"no longer need developers"',
            '"code without engineers"',
            '"AI" AND "one engineer"',
        ],
    },

    "hiring_contraction": {
        "description": "Reduced or frozen hiring for engineering roles",
        "match_units": [
            '"hiring freeze" AND "engineers"',
            '"hiring freeze" AND "developers"',
            '"pause hiring" AND "developers"',
            '"not hiring" AND "software engineers"',
            '"fewer engineering jobs"',
            '"shrinking engineering"',
        ],
    },

    "junior_displacement": {
        "description": "Entry-level and junior roles — the canary signal",
        "match_units": [
            '"junior developer" AND "AI"',
            '"junior engineer" AND "AI"',
            '"entry-level job" AND "software" AND "AI"',
            '"new graduate" AND "software engineer"',
            '"coding bootcamp" AND "jobs"',
            '"internship" AND "software engineer" AND "AI"',
        ],
    },

    "ai_productivity": {
        "description": "AI raising developer output — VADER scores the framing",
        "match_units": [
            '"developer productivity" AND "AI"',
            '"engineering productivity" AND "AI"',
            '"AI coding assistant"',
            '"GitHub Copilot" AND "productivity"',
            '"AI pair programmer"',
            '"software velocity" AND "AI"',
        ],
    },

    "corporate_restructuring": {
        "description": "Earnings call language citing AI as reason to cut engineering",
        "match_units": [
            '"AI" AND "reduce headcount" AND "engineering"',
            '"AI" AND "efficiency" AND "engineering team"',
            '"generative AI" AND "workforce"',
            '"AI" AND "restructuring" AND "software"',
        ],
    },

    "talent_demand": {
        "description": "Demand for engineers increasing",
        "match_units": [
            '"engineer shortage"',
            '"developer shortage"',
            '"AI engineer" AND "hiring"',
            '"demand" AND "software engineers"',
            '"engineering talent" AND "demand"',
        ],
    },
}
