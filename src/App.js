import mainImg from './images/main.png'
import sponsor1 from './images/sponsor1.png'
import daniel from './images/daniel.png'
import wu from './images/wu.png'
import lydia from './images/lydia.png'
import { PrimaryBtn, SecondaryDarkBtn } from './components'

const sponsors = [sponsor1, sponsor1, sponsor1, sponsor1, sponsor1]
const principalInvestigators = [
  {name: '01. Daniel Osgood →', img: daniel, college: 'IRI, Columbia University', link: 'https://iri.columbia.edu/contact/staff-directory/daniel-osgood/'},
  {name: '02. Eugene Wu →', img: wu, college: 'CS, Columbia University', link: 'https://www.cs.columbia.edu/~ewu/'},
  {name: '03. Lydia Chilton →', img: lydia, college: 'CS, Columbia University', link: 'https://www.cs.columbia.edu/~chilton/chilton.html'}
]
const members = ["Dieter Joubert →", "Ritika Deshpande →", "Tanisha Bisht →", "Aaron Zhu →", "Dieter Joubert →", "Aaron Zhu →"]
const publications = [
  {name: 'Playing to Adapt: Crowdsourcing Historical Climate Data with Gamification to Improve Farmer Risk Management Instruments', authors: 'Juan Nicolas Aguilera, Max Mauerman, Daniel Osgood', link: 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3639580'},
  {name: 'Reptile: Aggregation-level Explanations for Hierarchical Data', authors: 'Zachary Huang, Eugene Wu - SIGMOD 2022', link: 'https://arxiv.org/abs/2103.07037'},
  {name: 'Using Tech to Help African Farmers Collect Index Insurance Payouts', authors: 'News Article Aug 2022', link: 'https://www.engineering.columbia.edu/news/using-tech-help-african-farmers-collect-payouts'},
  {name: 'Voices of CS: Zachary Huang', authors: 'Columbia CS Newsletter', link: 'https://www.cs.columbia.edu/2022/voices-of-cs-zachary-huang/'},
  {name: 'In New Project, Millions of Farmers Will Help to Improve Insurance Against Climate Disasters', authors: 'Columbia Climate School newsletter 2021', link: 'https://iri.columbia.edu/news/in-new-project-millions-of-farmers-will-help-to-improve-insurance-against-climate-disasters/'},
  {name: 'iKON: Playing to Adapt', authors: 'Columbia Climate School newsletter 2021', link: 'https://iri.columbia.edu/news/ikon-playing-to-adapt/'},
]

function App() {
  return (
    <div className="App">

      <div className='hero'>
        <div className='hero__col_left'>
          <img className='hero__img' src={mainImg} alt='hero' />
        </div>
        <div className='hero__col_right'>
          <h1 className='hero__title'>Open Insurance Toolkit</h1>
          <p className='hero_desc'>Traditional disaster risk management often relies on satellite data, which might not fully reflect the realities faced by vulnerable communities. DESDR (Decision Engine for Socioeconomic Disaster Risk) transforms this approach by integrating firsthand information from those most affected, enhancing accuracy and insight into disaster risks</p>
          <PrimaryBtn onClick={() => console.log('call to action')} id={'#toolkit-section'}>EXPLORE OUR TOOLKIT</PrimaryBtn>
        </div>
      </div>

      <div className='sponsors'>
        {sponsors.map((sponsor,k) => <img key={k} src={sponsor} alt='sponsor' />)}
      </div>

      <div className='toolkit' id='toolkit-section'>
        <h1 className='toolkit__title'>DESDR Toolkit</h1>
        <div className='toolkit__row'>

          <div className='toolkit__col'>
            <div className='div_secondary_light'>01. Survey Your Way →</div>
            <p className='toolkit__subtitle'>DATA COLLECTION</p>
            <p className='toolkit__desc'>Utilizes mobile messaging platforms for accessible and respectful engagement with local communities.</p>
            <div className='div_secondary_light'>Senegal →</div>
          </div>

          <div className='toolkit__col'>
            <div className='div_secondary_light'>02. Reptile →</div>
            <p className='toolkit__subtitle'>DATA VERIFICATION</p>
            <p className='toolkit__desc'>Implements advanced tools to ensure data accuracy and security.</p>
            <div className='div_secondary_light'>Ethiopia →</div>
            <div className='div_secondary_light'>Zambia →</div>
            <div className='div_secondary_light'>Congo →</div>
            <div className='div_secondary_light'>Nigeria →</div>
          </div>

          <div className='toolkit__col'>
            <div className='div_secondary_light'>01. Survey Your Way →</div>
            <p className='toolkit__subtitle'>DATA COLLECTION</p>
            <p className='toolkit__desc'>Utilizes mobile messaging platforms for accessible and respectful engagement with local communities.</p>
            <div className='div_secondary_light'>Ethiopia →</div>
            <div className='div_secondary_light'>Zambia →</div>
            <div className='div_secondary_light'>Nigeria →</div>
          </div>

        </div>
      </div>

      <div className='important'>
        <p className='important_desc'>DESDR will be released as open-source software, free for use by various organizations. This initiative not only aims to improve disaster relief efforts but also empowers the most affected communities by giving them a significant role in the solution-making process.</p>
        <SecondaryDarkBtn id={'#toolkit-section'}>EXPLORE OUR TOOLKIT</SecondaryDarkBtn>
      </div>

      <div className='team'>
        <h1>Principal Investigators</h1>
        <div className='team__row'>
          {principalInvestigators.map((mem,k) => <div key={k} className='team__col' onClick={() => window.open(mem.link, '_blank')}>
            <div className='div_secondary_light'>{mem.name}</div>
            <img className='team__img' src={mem.img} alt={mem.name} />
            <p>{mem.college}</p>
          </div>)}
        </div>

        <h1>Meet our Team</h1>
        <div className='team__grid'>
          {members.map((member,k) => <div key={k} className='div_secondary_light'>{member}</div>)}
        </div>
      </div>

      <div className='publication'>
        <h1 className='publication__title'>Publications</h1>
        {publications.map((publication,k) => <div className='div_secondary_dark' onClick={() => window.open(publication.link, '_blank')}>
          <h3 className='publication__name'>{publication.name}</h3>
          <p className='publication__authors'>{publication.authors}</p>
        </div>)}
      </div>

    </div>
  );
}

export default App;
