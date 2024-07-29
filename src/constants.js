
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
  {name: '03. Sliders →', img: prodSlider, alt: 'product slider', link: '/sliders', subName: 'DATA VISUALIZATION', desc: 'Now finally, though this web platform, policy makers can access and utilize data to make informed decisions', deployed: [{name: 'Senegal →', link: 'https://columbia-desdr.github.io/Sliders-senegal/config'}, {name: 'Ethiopia →', link: 'https://columbia-desdr.github.io/Sliders-ethiopia/config'}, {name: 'Zambia →', link: 'https://github.com/Columbia-DESDR/Sliders-refactor-zambia'}, {name: 'Nigeria →', link: 'https://columbia-desdr.github.io/Sliders-nigeria/config'}, {name: 'Congo →', link: 'https://columbia-desdr.github.io/Sliders-drc/Two%20Column'}]}
]

export const principalInvestigators = [
  {name: '01. Daniel Osgood →', img: daniel, college: 'IRI, Columbia University', link: 'https://iri.columbia.edu/contact/staff-directory/daniel-osgood/'},
  {name: '02. Eugene Wu →', img: wu, college: 'CS, Columbia University', link: 'https://www.cs.columbia.edu/~ewu/'},
  {name: '03. Lydia Chilton →', img: lydia, college: 'CS, Columbia University', link: 'https://www.cs.columbia.edu/~chilton/chilton.html'}
]

export const members = ["Dieter Joubert", "Ritika Ganesh Deshpande", "Tanisha Bisht", "Miranda Zhou", "Dieter Joubert", "Aaron Zhu", "Amina Isayeva", "Kshitij D Gupta", "Ajit Sharma Kasturi", "Phoebe Adams"]

export const publications = [
  {name: 'Playing to Adapt: Crowdsourcing Historical Climate Data with Gamification to Improve Farmer Risk Management Instruments', authors: 'Juan Nicolas Aguilera, Max Mauerman, Daniel Osgood', link: 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3639580'},
  {name: 'Reptile: Aggregation-level Explanations for Hierarchical Data', authors: 'Zachary Huang, Eugene Wu - SIGMOD 2022', link: 'https://arxiv.org/abs/2103.07037'},
  {name: 'Using Tech to Help African Farmers Collect Index Insurance Payouts', authors: 'News Article Aug 2022', link: 'https://www.engineering.columbia.edu/news/using-tech-help-african-farmers-collect-payouts'},
  {name: 'Voices of CS: Zachary Huang', authors: 'Columbia CS Newsletter', link: 'https://www.cs.columbia.edu/2022/voices-of-cs-zachary-huang/'},
  {name: 'In New Project, Millions of Farmers Will Help to Improve Insurance Against Climate Disasters', authors: 'Columbia Climate School newsletter 2021', link: 'https://iri.columbia.edu/news/in-new-project-millions-of-farmers-will-help-to-improve-insurance-against-climate-disasters/'},
  {name: 'iKON: Playing to Adapt', authors: 'Columbia Climate School newsletter 2021', link: 'https://iri.columbia.edu/news/ikon-playing-to-adapt/'},
]