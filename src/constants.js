
import daniel from './images/daniel.png'
import wu from './images/wu.png'
import lydia from './images/lydia.png'

import prodIkon from './images/prod-ikon.png'
import prodReptile from './images/prod-reptile.png'
import prodSlider from './images/prod-slider.png'

import logoCCS from './images/logo-ccs.jpeg'
import logoCSE from './images/logo-cse.png'
import logoICRISAT from './images/logo-icrisat.png'
import logoIRI from './images/logo-iri.png'
import logoServir from './images/logo-servir.png'
import logoUSAID from './images/logo-usaid.png'

export const sponsors = [logoCCS, logoCSE, logoICRISAT, logoIRI, logoServir, logoUSAID]

export const toolkit = [
  {name: '01. Survey Your Way →', img: prodIkon, alt: 'product ikon', link: '/survey-your-way', subName: 'DATA COLLECTION', desc: 'First, we utilize mobile messaging platforms for accessible and respectful engagement and data collection from local communities', deployed: [{name: 'Noki →', link: 'https://fist-noki.iri.columbia.edu/login'}, {name: 'iKON →', link: 'https://fist-ikonadmin.iri.columbia.edu/login?next=%2Fadmin'}]},
  {name: '02. Reptile →', img: prodReptile, alt: 'product reptile', link: '/reptile', subName: 'DATA VERIFICATION', desc: 'Then, we ensure data accuracy and security using this tool', deployed: [{name: 'Ethiopia →', link: 'https://fist-cleandat.iri.columbia.edu/com'}, {name: 'Zambia →', link: 'https://fist-cleandat.iri.columbia.edu/comzambia'}, {name: 'Congo →', link: 'http://ec2-18-117-152-17.us-east-2.compute.amazonaws.com/'}]},
  {name: '03. Sliders →', img: prodSlider, alt: 'product slider', link: '/sliders', subName: 'DATA VISUALIZATION', desc: 'Now finally, though this web platform, policy makers can access and utilize data to make informed decisions', deployed: [{name: 'Senegal →', link: 'https://columbia-desdr.github.io/Sliders-senegal/config'}, {name: 'Ethiopia →', link: 'https://columbia-desdr.github.io/Sliders-ethiopia/config'}, {name: 'Zambia →', link: 'https://columbia-desdr.github.io/Sliders-zambia/'}, {name: 'Nigeria →', link: 'https://columbia-desdr.github.io/Sliders-nigeria/config'}, {name: 'Congo →', link: 'https://columbia-desdr.github.io/Sliders-drc/Two%20Column'},{name: 'Bangladesh →', link: 'https://columbia-desdr.github.io/Sliders-bangladesh/config'},{name: 'Mozambique →', link: 'https://columbia-desdr.github.io/Sliders-mozambique/config'},{name: 'Rwanda →', link: 'https://columbia-desdr.github.io/Sliders-rwanda/config'}]}
]

export const principalInvestigators = [
  {name: '01. Daniel Osgood →', img: daniel, college: 'IRI, Columbia University', link: 'https://iri.columbia.edu/contact/staff-directory/daniel-osgood/'},
  {name: '02. Eugene Wu →', img: wu, college: 'CS, Columbia University', link: 'https://www.cs.columbia.edu/~ewu/'},
  {name: '03. Lydia Chilton →', img: lydia, college: 'CS, Columbia University', link: 'https://www.cs.columbia.edu/~chilton/chilton.html'}
]

export const members = ["Dieter Joubert", "Ritika Ganesh Deshpande", "Tanisha Bisht", "Miranda Zhou", "Aaron Zhu", "Amina Isayeva", "Kshitij D Gupta", "Ajit Sharma Kasturi", "Phoebe Adams","Emnet Tsegaye","Azam Khan","Jasper Sands","Lilita Yenew","Jongho Bae","Kenny Frias","Justine Pui Ying Mach"]

//export const publications = [ 
//  {name: 'Playing to Adapt: Crowdsourcing Historical Climate Data with Gamification to Improve Farmer Risk Management Instruments', authors: 'Juan Nicolas Aguilera, Max Mauerman, Daniel Osgood', link: 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3639580'},
//  {name: 'Reptile: Aggregation-level Explanations for Hierarchical Data', authors: 'Zachary Huang, Eugene Wu - SIGMOD 2022', link: 'https://arxiv.org/abs/2103.07037'},
//  {name: 'Using Tech to Help African Farmers Collect Index Insurance Payouts', authors: 'News Article Aug 2022', link: 'https://www.engineering.columbia.edu/news/using-tech-help-african-farmers-collect-payouts'},
//  {name: 'Voices of CS: Zachary Huang', authors: 'Columbia CS Newsletter', link: 'https://www.cs.columbia.edu/2022/voices-of-cs-zachary-huang/'},
//  {name: 'In New Project, Millions of Farmers Will Help to Improve Insurance Against Climate Disasters', authors: 'Columbia Climate School newsletter 2021', link: 'https://iri.columbia.edu/news/in-new-project-millions-of-farmers-will-help-to-improve-insurance-against-climate-disasters/'},
//  {name: 'iKON: Playing to Adapt', authors: 'Columbia Climate School newsletter 2021', link: 'https://iri.columbia.edu/news/ikon-playing-to-adapt/'},
//  {name: 'Context-Aware Climate Intelligence: Integrating Community Data into AI Disaster Models', authors: 'Justine Mach, Kenny Frias', link: 'https://docs.google.com/presentation/d/1I2cEKmiWuY7YXb3qqvKoSku3tUseWDVscvjdbWMvv2g/edit?usp=sharing'},
//]
//


export const publications = [
  {
    name: 'In New Project, Millions of Farmers Will Help to Improve Insurance Against Climate Disasters',
    authors: 'Columbia Climate School Newsletter — 2021',
    link: 'https://iri.columbia.edu/news/in-new-project-millions-of-farmers-will-help-to-improve-insurance-against-climate-disasters/',
  },
  {
    name: 'iKON: Playing to Adapt',
    authors: 'Columbia Climate School Newsletter — 2021',
    link: 'https://iri.columbia.edu/news/ikon-playing-to-adapt/',
  },
  {
    name: 'PI2: End-to-end Interactive Visualization Interface Generation from Queries',
    authors: 'Yiru Chen, Eugene Wu',
    link: 'https://arxiv.org/abs/2107.08203'
  },
  {
    name: 'View Composition Algebra for Ad Hoc Comparisons',
    authors: 'Eugene Wu — TVCG 2022',
    link: 'https://arxiv.org/abs/2202.07836',
  },
  {
    name: 'Playing to Adapt: Crowdsourcing Historical Climate Data with Gamification to Improve Farmer Risk Management Instruments',
    authors: 'Juan Nicolas Aguilera, Max Mauerman, Daniel Osgood',
    link: 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3639580',
  },
  {
    name: 'Reptile: Aggregation-level Explanations for Hierarchical Data',
    authors: 'Zachary Huang, Eugene Wu — SIGMOD 2022',
    link: 'https://arxiv.org/abs/2103.07037',
  },
  {
    name: 'Using Tech to Help African Farmers Collect Index Insurance Payouts',
    authors: 'News Article — Aug 2022',
    link: 'https://www.engineering.columbia.edu/news/using-tech-help-african-farmers-collect-payouts',
  },
  {
    name: 'NL2INTERFACE: Interactive Visualization Interface Generation from Natural Language Queries',
    authors: 'Yiru Chen, Ryan Li, Austin Mac, Tianbao Xie, Tao Yu, Eugene Wu — VIS NLVis Workshop 2022',
    link: 'https://arxiv.org/abs/2209.08834',
  },
  {
    name: 'Voices of CS: Zachary Huang',
    authors: 'Columbia CS Newsletter — 2022',
    link: 'https://www.cs.columbia.edu/2022/voices-of-cs-zachary-huang/',
  },
  {
    name: 'Demonstration of PI2: Interactive Visualization Interface Generation for SQL Analysis in Notebook',
    authors: 'Jeffrey Tao, Yiru Chen, Eugene Wu',
    link: 'https://doi.org/10.1145/3514221.3520153'
  },
  {
    name: 'DIG: The Data Interface Grammar',
    authors: 'Yiru Chen, Jeffrey Tao, Eugene Wu — HILDA @ SIGMOD 2023',
    link: 'https://www.dropbox.com/s/bhwikxq8932dsg5/dig-hilda23-cr.pdf?dl=0',
  },
  {
    name: 'Design-Specific Transformations in Visualization',
    authors: 'Eugene Wu, Remco Chang — BELIV @ IEEE VIS 2024',
    link: 'https://arxiv.org/abs/2407.06404',
  },
  {
    name: 'LEAP Summer Lecture in Climate Data Science webinar featuring Dr. Joshua DeVincenzo, where he discussed "Climate, Mental Models, and Data for Disaster Preparedness"',
    authors: 'Joshua DeVincenzo — LEAP Summer Lecture — July 2024',
    link: 'https://www.eventbrite.com/e/leap-summer-2024-lecture-in-climate-data-science-joshua-devincenzo-tickets-755889344377',
  },
  {
    name: 'Database Theory in Action: Database Visualization',
    authors: 'Eugene Wu — ICDT Database Theory in Action 2025',
    link: 'https://drops.dagstuhl.de/storage/00lipics/lipics-vol328-icdt2025/LIPIcs.ICDT.2025.35/LIPIcs.ICDT.2025.35.pdf',
  },
  {
    name: 'Insurance for Climate Change in the Global South',
    authors: 'Daniel Osgood — Class — Spring 2025',
  },
  {
    name: 'What questions need to be asked for monitoring and evaluation of agricultural insurance to assist smallholder farmers and humanitarian funds?',
    authors: 'SIPA Class — Spring 2025',
    link: 'https://www.sipa.columbia.edu/what-questions-need-be-asked-monitoring-and-evaluation-agricultural-insurance-assist-smallholder',
  },
  {
    name: 'Aggregation Consistency Errors in Semantic Layers and How to Avoid Them',
    authors: 'Zezhou Huang, Pavan Kalyan Damalapati, Eugene Wu',
    link: 'https://dl.acm.org/doi/10.1145/3597465.3605224' 
  },
  {
    name: 'Can generative AI help strengthen disaster preparedness and resilience among youth?',
    authors: 'State of the Planet Blog — Dec 2025',
    link: 'https://news.climate.columbia.edu/2025/12/16/proposing-a-genai-chatbot-framework-for-youth-disaster-risk-reduction/',
  },
  {
    name: '2025 was one of the three hottest years on record, scientists say',
    authors: 'Andrew Kruczkiewicz — AP News — Dec 2025',
    link: 'https://apnews.com/article/climate-world-weather-attribution-year-end-extreme-1e9028da87e518382482e21fef3cfeee',
  },
  {
    name: 'It\'s been one year since wildfires devastated Los Angeles. What have we learned?',
    authors: 'Jeff Schlegelmilch — State of the Planet Blog — Jan 2026',
    link: 'https://news.climate.columbia.edu/2026/01/12/its-been-one-year-since-wildfires-devastated-los-angeles-what-have-we-learned/',
  },
  {
    name: 'Imagining Anticipatory Action',
    authors: 'NCDP — World Food Programme Exercise — Jan 27, 2026',
  },
  {
    name: 'Field testing with farmers in the coffee regions of Colombia',
    authors: 'Yale Center for Geospatial Solutions, Yale School of the Environment — Featured Video — Jan 2026',
    link: 'https://ncdp.columbia.edu/video-media-items/field-testing-the-ikon-game-in-colombia/',
  },
  {
    name: 'Capacity Building with the Ethiopian Meteorological Institute',
    authors: 'NCDP — NCDP Perspectives Blog — Jan 2026',
    link: 'https://ncdp.columbia.edu/ncdp-perspectives/capacity-building-with-the-ethiopian-meteorological-institute/',
  },
  {
    name: 'Community Participation and Planning Guides for Local Climate Action',
    authors: 'NCDP — Strengthening Capacities and Civic Participation for Climate-Resilient Communities in Chile — Jan 2026',
    link: 'https://academiccommons.columbia.edu/doi/10.7916/vsms-hm95',
  },
  {
    name: 'Context-Aware Climate Intelligence: Integrating Community Data into AI Disaster Models',
    authors: 'Justine Mach, Kenny Frias',
    link: 'https://docs.google.com/presentation/d/1I2cEKmiWuY7YXb3qqvKoSku3tUseWDVscvjdbWMvv2g/edit?usp=sharing',
  },
];

