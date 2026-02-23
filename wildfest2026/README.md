> [!NOTE]
> We won the [EMP Hackfest 2026](https://emphackfest.org/current-event) with our National Park Guardian AI Project!
> * Repo: [oliviajinwang/wildfest2026](https://github.com/oliviajinwang/emp_hackfest/tree/main/wildfest2026)
> * 1st Place Winner Submission on DevPost: [National Park Guardian AI](https://devpost.com/software/national-park-guardian-ai)

# National Park Guardian AI (project for EMP Hackfest 2026: WildHack)

This is National Park Guardian AI, a small web application that seeks to protect wildlife through using an AI-driven interactive dashboard for managing wildlife in National Parks and brings awareness to wildlife conservation.

According to the Outreach Network for Gene Drive Research, "over half of U.S. national parks are at a risk of biodiversity loss," in which invaive species are to blame. However, there are only management plans for 23% of harmful invasive species, meaning that the remaining 77% of national parks have no plans for retaining biodiversity of their wildlife.

To combat this, we decided on a small web app for park rangers that identifies the flora and fauna with the highest risk of endangerment. Then, park rangers and similar wildlife conservationists may use this information to prioritize habitat restoration in areas with species that are at risk of being endangered or extinct.

## Authors
Olivia Wang, Grade 10 (Class of 2028), International Community School

Yutang Xie, Grade 10 (Class of 2028), International Community School

Both authors are equal contributors of this project.

## Video Demo

[![National Park Guardian AI Dashboard Demo](https://img.youtube.com/vi/OkV3xOn7RiI/0.jpg)](https://www.youtube.com/watch?v=OkV3xOn7RiI)

## Features
- Home page that includes our about-us and our mission
- Interactive map of total number of species per national park
- Interactive map of biodiversity density per national park
- Clicking on nodes in the map will open a side panel on the right with both non-AI and AI information
- Call-to-action page that includes a sign-up area to submit an email
- Filter on the side panel on the left to choose certain species to include in the statistics
- Color theme chooser for user preferences

## Requirements
- Python 3.13+
- A modern browser

## Quick Start
1) Clone the repo
```bash
git clone https://github.com/oliviajinwang/emp_hackfest.git
cd wildfest2026
```

2) Install dependencies
```bash
pip scikit-learn, numpy, streamlit, plotly, folium, pandas
```

3) Start the web application
```bash
streamlit run code/app.py
```

This should start in your browser automatically. If not, open the link provided in the terminal.

4) Navigate

Use the filters, navigate the map by dragging and releasing on the map space. Click on nodes to open a side panel on the right.

## File Structure

```
wildfest2026/                         # everything for the EmP Hackfest 2026
|--- assets/                          # pictures folder
|    |--- homepage_photo.jpg          # national park picture used in home page
|    |--- pglogo3.png                 # non-transparent logo
|    |--- pglogo4.webp                # transparent logo
|    |___ yellowstone2.jpg            # national park picture used in home page
|--- code/                            # code for the website
|    |---tabs/                        # code for each tab of the website
|    |    |--- categories.py          # species analysis by categories
|    |    |--- cta.py                 # call-to-action page where a user can enter their email to join
|    |    |--- homepage.py            # home page of website that contains information about the website
|    |    |___ map.py                 # interactive map
|    |--- ai_predictor.py             # ai module that predicts vulnerability of a species
|    |--- app.py                      # main app that contains the structure of the webapp
|    |--- themes.py                   # contains the code to change color theme
|    |___ utils.py                    # shared utils to load data from csvs
|--- data/                            # data folder for information
|    |--- emails.jsonl                # JSONL file for email storage
|    |--- national-park-species.csv   # Data file for species in national parks
|    |___ national-parks.csv          # Data file for national parks
|___ README.md
```

## Notes
- The AI will take a while to run and infer. When opening the map page, please wait a while. And when waiting for the side panel's AI summary to update, also please wait.
- If you receive any error while trying to run the webapp or you see a message that says something along the lines of "please ensure parks.csv and park-species.csv are in the same folder," ensure that you are currently in the `wildfest2026` directory.
