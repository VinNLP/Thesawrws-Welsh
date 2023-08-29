*[Read this in English](README.en.md)*

# Thesawrws Ar-lein Cymraeg Cyfoes (ThACC) / Welsh Online Thesaurus

Mae'r ystorfa hon yn cyflwyno thesawrws Cymraeg ar-lein sy'n fynediad agored ac yn hawdd ei ddefnyddio. Nod y prosiect oedd cyfoethogi adnoddau digidol yn y Gymraeg. Gan fanteisio ar ddatblygiadau ym maes Prosesu Iaith Naturiol (NLP), mae ein dull yn cyfuno mewnblaniadau geiriau sy'n bodoli eisioes, tagiwr semanteg Cymraeg, a gwerthusiadau gan fodau dynol er mwyn dod o hyd i gyfystyron.

This repo introduces an open-access, user-friendly online thesaurus for the Welsh language, aimed at enriching digital resources for Welsh speakers and learners. Utilising advances in Natural Language Processing (NLP), our approach combines pre-existing word embeddings, a Welsh semantic tagger, and human evaluation to establish related terms. 

## Gosodiad / Installation
I osod y wefan Flask hon, agorwch eich terfynell a gweithredwch y gorchmynion canlynol:
To install this Flask website, open your terminal and execute the following commands:
```bash
$ git clone https://github.com/Nouran-Khallaf/Thesawrws-website.git
$ sudo apt-get install python3 python3-venv
$ cd Thesawrws-website
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
# To install FastText
$ git clone https://github.com/facebookresearch/fastText.git
$ cd fastText
$ pip install .
```
## Dechrau gwefan y Thesawrws / Start the Thesawrws website
Gweithredwch y gorchmynion canlynol:
Execute the following commands:
```bash
$ cd Thesawrws-website
$ export FLASK_APP=main.py
$ flask run --host=0.0.0.0
```
## I ddefnyddio'r RESTful API / To use the RESTful API 
Llinell Orchymyn:
Command line:
```bash
$ curl "http:/148.88.72.60:8010/api/synonyms?word=pobl"
```
neu sgript Python
or Python script 
```bash
$ import requests
$ import json
$ response = requests.get('http://148.88.72.60:8010/api/synonyms', params={'word': 'school'})
$ data = response.json()
$ print(json.dumps(data, indent=2))
```

_Os defnyddiwch unrhyw un o'r corpora yn eich gwaith, cyfeiriwch at y papur hwn:_
_If you use any of these corpora in your work, please cite this paper:_

```

@inproceedings{,
    title = "Open-Source Thesaurus Development for Under-Resourced Languages: a Welsh Case Study",
    author = "Nouran Khallaf, Elin Arfon, Mo El-Haj, Jonathan Morris, Dawn Knight, Paul Rayson,Tymaa Hammouda3 and Mustafa Jarrar",
    month = sep.,
    year = "2023",
    publisher = "The 4th Conference on Language, Data and Knowledge Conference (LDK 2023), Vienna, Austria.",
    url = "",
    pages = "",
}
```

### Cysylltiadau / Contacts
- [Nouran Khallaf](https://github.com/Nouran-Khallaf)
- [Mahmoud El-Haj](https://github.com/drelhaj)
- [Jonathan Morris](MorrisJ17@cardiff.ac.uk)
- [Elin Afron](arfone@cardiff.ac.uk)
- [Dawn Knight](https://github.com/DawnKnight-Cardiff)


<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
- This work with all the accompanying resources is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
